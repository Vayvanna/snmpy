import threading
import time
import subprocess
from flask import current_app
from db.models import Site,SiteLogs # Import your SQLAlchemy model and session object
from app.extensions import db
import datetime
from utils.telegram_alert import send_alert
import json
from datetime import datetime
from core.helpersofsn import snmp_get
from db.models import SNMPMetricLog, SNMPCurrent  # if not already
import threading
import time
import subprocess
import json
from datetime import datetime, timedelta





def ping_site(ip):
    """Pings a site using ICMP."""
    try:
        subprocess.check_output(["ping", "-c", "1", "-W", "3", ip], stderr=subprocess.DEVNULL)
        return "up"
    except subprocess.CalledProcessError:
        return "down"

def poll_sites(app):
    """Continuously poll all sites and update their status in the DB."""
    with app.app_context():
        while True:
            sites = Site.query.all()  # Get all sites from the DB

            for site in sites:
                # result = ping_site(site.ip_address)
                # site.status = result  # Update the site row

                # # ✅ Create new log entry
                # log = SiteLogs(
                #     site_id=site.id,
                #     status=result  # or leave out if model default is set
                # )
                # db.session.add(log)
                old_status = site.status
                result = ping_site(site.ip_address)
                new_status = result

                if old_status != new_status:
                    msg = f"🚨 Site {site.name} changed status: {old_status.upper()} → {new_status.upper()}"
                    send_alert(msg, site_id=site.id, status=new_status)

                site.status = result  # Now update
                log = SiteLogs(site_id=site.id, status=result)
                db.session.add(log)

                # 4. SNMP POLLING (only if site is up)
                # 4. SNMP POLLING (only if site is up)w

                with open('config/snmp_oids.json')as f: # open the oids json on config/snmp_oids.json
                    SNMP_OIDS= json.load(f)

                    
                    if new_status == "up": # if the newstatus=)current one is up, try the following:
                        for entry in SNMP_OIDS: #for each oid in json
                            label = entry["label"]#label gets its new label
                            oid = entry["oid"] # oid gets its new oid
                            value = snmp_get(site.ip_address, site.snmp_community, oid)# value of this oid is sent using snmp_get from helpersofsn.py

                            if value is None:# if no value, continue act as its unreachable., so SKIP to next entry.
                                print ("⚪⚪⚪ the value is none, so uncreachable, snmpy/core/poller.py")
                                continue  # skip unreachable SNMP

                            # Log into SNMPMetricLog    #if value is actually not None, then log it as metric then down below update the LIVE table.
                            db.session.add(SNMPMetricLog(
                                site_id=site.id,
                                timestamp=datetime.utcnow(),
                                oid=oid,
                                label=label,
                                value=value
                            ))

                            # Upsert into SNMPCurrent
                            current = SNMPCurrent.query.filter_by(site_id=site.id, label=label).first()
                            if current: # if current we got is there, exists.
                                print ("⚪🔵🟣 the current value exists already, snmpy/core/poller.py")
                                print (f"⚪🔵🟣 site name: {site.name}")
                                print (f"⚪🔵🟣 site id: {site.id}")
                                print (f"⚪🔵🟣 current value: {value}")
                                print (f"⚪🔵🟣 oid: {oid}")
                                print (f"⚪🔵🟣 label: {label}")
                                current.value = value # update its value
                                current.oid = oid # update its oid
                                default_time = lambda: datetime.utcnow() + timedelta(hours=1)
                                current.last_updated = default_time()
                            else: # if it doesn't exist, then create it & update it.
                                print ("⚪🟢🔵 the current value doesn't exist, gonna create it, snmpy/core/poller.py")
                                db.session.add(SNMPCurrent(
                                    site_id=site.id,
                                    label=label,
                                    oid=oid,
                                    value=value
                                ))



            db.session.commit()  # Save both status update + logs
            time.sleep(15)  # Next polling round

def start_background_thread(app):
    thread = threading.Thread(target=poll_sites, args=(app,))
    thread.daemon = True
    thread.start()

# Explanation:
# - We've removed usage of full_site_status and site_status
# - Everything is now stored and queried from PostgreSQL
# - This makes your app persistent and production-ready
# - Ping status is dynamically updated in the DB every 15 seconds


import threading
import time
import subprocess
from flask import current_app
from db.models import * # Import your SQLAlchemy model and session object
from app.extensions import db
from utils.telegram_alert import send_alert
import json
from datetime import datetime
from core.helpersofsn import snmp_get
from db.models import SNMPMetricLog, SNMPCurrent, default_time  # if not already
from datetime import datetime, timedelta


import re

def ping_site(ip, max_attempts=4):
    for attempt in range(max_attempts):
        try:
            output = subprocess.check_output(
                ["ping", "-c", "1", "-W", "3", ip],
                stderr=subprocess.DEVNULL,
                text=True
            )
            # Extract latency from the output: e.g. "time=12.345 ms"
            match = re.search(r'time=(\d+\.?\d*)\s*ms', output)
            latency = float(match.group(1)) if match else None
            return "up", latency
        except subprocess.CalledProcessError:
            time.sleep(0.2)  # short pause before retry

    return "down", None

from datetime import datetime, timedelta, timezone

def default_time():
    return datetime.now(timezone.utc)

def poll_sites(app):
    """Continuously poll all sites and update their status in the DB."""
    with app.app_context():
        while True:
            sites = Site.query.all()

            for site in sites:
                old_status = site.status
                result, latency = ping_site(site.ip_address)
                new_status = result

                if result == "up":
                    print(f"[✓] {site.name} responded in {latency} ms")
                else:
                    print(f"[✗] {site.name} is down")

                now = default_time()

                # ✅ Only proceed if the status has changed
                if old_status != new_status:
                    threshold = now - timedelta(seconds=220)

                    print(f"[DEBUG] now: {now} (tzinfo: {now.tzinfo})")
                    print(f"[DEBUG] threshold (now - 220 sec): {threshold} (tzinfo: {threshold.tzinfo})")

                    # ✅ Look for any alert for the same site and new status within the threshold window
                    recent_alert = Alert.query.filter(
                        Alert.site_id == site.id,
                        Alert.status == new_status,
                        Alert.prev_status == old_status,
                        Alert.timestamp >= threshold
                    ).order_by(Alert.timestamp.desc()).first()

                    if not recent_alert:
                        msg = f"🚨 Site {site.name} changed status: {old_status.upper()} → {new_status.upper()}"
                        send_alert(msg, site_id=site.id, status=new_status)

                        db.session.add(Alert(
                            site_id=site.id,
                            status=new_status,
                            prev_status=old_status,
                            message=msg,
                            timestamp=now  # ⏰ explicitly set timestamp
                        ))
                        db.session.commit()  # ✅ Commit now to make sure it's stored
                    else:
                        print(f"[⚠️] Skipping duplicate alert for {site.name} - already sent recently.")

                # Update current site status regardless
                site.status = new_status

                # Site status log
                db.session.add(SiteLogs(site_id=site.id, status=new_status, latency=latency))

                # SNMP polling only if site is up
                if new_status == "up":
                    for entry in site.snmp_oids:
                        label = entry.label or "no-label"
                        oid = entry.oid
                        port = entry.port or 161
                        community = site.snmp_community or "public"

                        value = snmp_get(site.ip_address, community, oid, port)

                        if value is None:
                            print("⚪", end='', flush=True)
                            continue

                        db.session.add(SNMPMetricLog(
                            site_id=site.id,
                            timestamp=default_time(),
                            oid=oid,
                            label=label,
                            value=value
                        ))

                        with db.session.no_autoflush:
                            current = SNMPCurrent.query.filter_by(site_id=site.id, label=label).first()
                            if current:
                                print("🟢", end='', flush=True)
                                current.value = value
                                current.oid = oid
                                current.last_updated = default_time()
                            else:
                                print("🟣", end='', flush=True)
                                db.session.merge(SNMPCurrent(
                                    site_id=site.id,
                                    label=label,
                                    oid=oid,
                                    value=value,
                                    last_updated=default_time()
                                ))

            # ✅ Final commit for status + SNMP logs
            db.session.commit()
            time.sleep(15)




def start_background_thread(app):
    thread = threading.Thread(target=poll_sites, args=(app,))
    thread.daemon = True
    thread.start()

# Explanation:
# - We've removed usage of full_site_status and site_status
# - Everything is now stored and queried from PostgreSQL
# - This makes your app persistent and production-ready
# - Ping status is dynamically updated in the DB every 15 seconds


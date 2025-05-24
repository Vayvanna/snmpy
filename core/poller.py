import threading
import time
import subprocess
from flask import current_app
from db.models import Site,SiteLogs # Import your SQLAlchemy model and session object
from app.extensions import db
import datetime
from utils.telegram_alert import send_alert

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
                    msg = f"🚨 Site *{site.name}* changed status: {old_status.upper()} → {new_status.upper()}"
                    send_alert(msg, site_id=site.id)

                site.status = result  # Now update
                log = SiteLogs(site_id=site.id, status=result)
                db.session.add(log)




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
































































# import threading
# import time
# import subprocess
# import json
# from pathlib import Path

# # Path to the sites.json file
# site_file = Path("config/sites.json")

# # we imported Path from pathlib & we're going to use that file for information about the sites, including IDs...

# # Load and parse the sites.json file
# with open(site_file) as f:
#     sites_data = json.load(f)   ## we are opening and loading what's inside of sites.json into sites_data

# # Dictionary: {89: "163.136.123.234"}
# # this will end up extracting from sites_data and putting in sites in this format: {89 : "163.136.123.234"}
# sites = {site["id"]: site["ip"] for site in sites_data["sites"]}

# # Holds the site id + status: {"89": "up", ...}
# site_status = {}

# # Holds the full site info with status added, ready to be consumed by API
# # e.g. {"89": {"name": "Tunis", "ip": "...", "lat": ..., "lon": ..., "status": "up"}}
# full_site_status = {}

# def ping_site(ip):
#     try:
#         # Send 1 ICMP ping with 3 second timeout, suppress output
#         subprocess.check_output(["ping", "-c", "1", "-W", "3", ip], stderr=subprocess.DEVNULL)
#         return "up"
#     except subprocess.CalledProcessError:
#         return "down"
    

# full_site_status={}


# def poll_sites():
#     while True:
#         for site in sites_data["sites"]:
#             site_id = site["id"]
#             ip = site["ip"]

#             status = ping_site(ip)
#             site_status[site_id] = status

#             # build full data object including status
#             full_site_status[site_id] = {
#                 "name": site["name"],
#                 "ip": ip,
#                 "lat": site["lat"],
#                 "lon": site["lon"],
#                 "status": status
#             }
            
#         # for site in full_site_status.values():
#         #     print()            # separate each site with an empty line
#         #     print(site)        # print the full dictionary for this site

#         time.sleep(15)

# def start_background_thread():
#     thread = threading.Thread(target=poll_sites)
#     thread.daemon = True  # thread will stop when main program exits
#     thread.start()

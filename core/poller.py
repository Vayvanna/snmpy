import threading
import time
import subprocess
import json
from pathlib import Path

# Path to the sites.json file
site_file = Path("config/sites.json")

# we imported Path from pathlib & we're going to use that file for information about the sites, including IDs...

# Load and parse the sites.json file
with open(site_file) as f:
    sites_data = json.load(f)   ## we are opening and loading what's inside of sites.json into sites_data

# Dictionary: {89: "163.136.123.234"}
# this will end up extracting from sites_data and putting in sites in this format: {89 : "163.136.123.234"}
sites = {site["id"]: site["ip"] for site in sites_data["sites"]}

# Holds the site id + status: {"89": "up", ...}
site_status = {}

# Holds the full site info with status added, ready to be consumed by API
# e.g. {"89": {"name": "Tunis", "ip": "...", "lat": ..., "lon": ..., "status": "up"}}
full_site_status = {}

def ping_site(ip):
    try:
        # Send 1 ICMP ping with 3 second timeout, suppress output
        subprocess.check_output(["ping", "-c", "1", "-W", "3", ip], stderr=subprocess.DEVNULL)
        return "up"
    except subprocess.CalledProcessError:
        return "down"
full_site_status={}
def poll_sites():
    while True:
        for site in sites_data["sites"]:
            site_id = site["id"]
            ip = site["ip"]

            status = ping_site(ip)
            site_status[site_id] = status

            # build full data object including status
            full_site_status[site_id] = {
                "name": site["name"],
                "ip": ip,
                "lat": site["lat"],
                "lon": site["lon"],
                "status": status
            }
            
        # for site in full_site_status.values():
        #     print()            # separate each site with an empty line
        #     print(site)        # print the full dictionary for this site

        time.sleep(15)

def start_background_thread():
    thread = threading.Thread(target=poll_sites)
    thread.daemon = True  # thread will stop when main program exits
    thread.start()

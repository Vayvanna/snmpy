# core/init_sites.py

import json
from db.models import Site
from app.extensions import db
from pathlib import Path

def sync_sites_from_json():
    json_path = Path("config/sites.json")
    if not json_path.exists():
        print("⚠️ sites.json not found!")
        return

    with open(json_path) as f:
        data = json.load(f)

    added = 0
    skipped = 0
    modified = 0

    for s in data["sites"]:
        site_id = int(s["id"])
        existing = Site.query.get(site_id)

        if existing:
            # check if any field changed
            if (
                existing.name == s["name"] and
                existing.ip_address == s["ip"] and
                existing.latitude == s["lat"] and
                existing.longitude == s["lon"] and
                existing.snmp_community == s["snmp_community"]
            ):
                skipped += 1
                continue
            # apply changes
            existing.name = s["name"]
            existing.ip_address = s["ip"]
            existing.latitude = s["lat"]
            existing.longitude = s["lon"]
            existing.snmp_community = s["snmp_community"]
            modified += 1
            continue

        # if not exists, create new site
        site = Site(
            id=site_id,
            name=s["name"],
            ip_address=s["ip"],
            latitude=s["lat"],
            longitude=s["lon"],
            location="Unknown",
            snmp_community="public",
            status="unknown"
        )
        db.session.add(site)
        added += 1

    db.session.commit()
    print(f"✅ Synced sites.json: {added} new, {skipped} skipped, {modified} modified")

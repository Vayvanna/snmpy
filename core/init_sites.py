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

    for s in data["sites"]:
        existing = Site.query.get(int(s["id"]))
        if existing:
            skipped += 1
            continue  # Don't overwrite, just skip

        site = Site(
            id=int(s["id"]),
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
    print(f"✅ Synced sites.json: {added} new, {skipped} skipped")

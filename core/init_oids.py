# core/init_oids.py
import json
from db.models import Site, SNMPOID
from app.extensions import db

def sync_snmp_oids():
    try:
        with open("config/snmp_oids.json") as f:
            site_oid_map = json.load(f)
    except FileNotFoundError:
        print("⚠️ config/snmp_oids.json not found!")
        return

    total_inserted = 0
    for site_id_str, oids in site_oid_map.items():
        site_id = int(site_id_str)
        SNMPOID.query.filter_by(site_id=site_id).delete()  # Clear old OIDs

        for entry in oids:
            db.session.add(SNMPOID(
                site_id=site_id,
                oid=entry["oid"],
                label=entry.get("label", "no-label"),
                port=entry.get("port", 161)
            ))
            total_inserted += 1

    db.session.commit()
    print(f"✅ SNMP OIDs synced: {total_inserted} inserted across {len(site_oid_map)} sites")

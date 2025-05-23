import json
from db.models import Site
from app import create_app, db

app=create_app()
with app.app_context():
    with open ('config/sites.json') as f:
        data=json.load(f)

    for s in data["sites"]:
        site = Site(
            id=int(s["id"]),
            name=s["name"],
            ip_address=s["ip"],
            latitude=s["lat"],
            longitude=s["lon"],
            location="Unknown",  # Optional: extend JSON or update later
            snmp_community="public",  # Optional
            status="unknown"
        )
        db.session.add(site)
    
    db.session.commit()
    print("Sites from json have been loaded into db.")
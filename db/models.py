# defines the db tables, using sqlalchemy.
# This is where you describe, in Python, the shape of your data
# This is where you describe, in Python, the shape of your data
# This is where you describe, in Python, the shape of your data:


# basically here, this models.py is the translator of the ORM(object relational M smth) which is SQLAlchemy cuz raw sql is annoying.

# the stuff is creating two tables.
import datetime
from app.extensions import db
# from datetime import datetime
from datetime import datetime, timedelta, timezone
from sqlalchemy.types import DateTime
from sqlalchemy.dialects.postgresql import TIMESTAMP
tz_utc_plus_1 = timezone(timedelta(hours=1))
# timestamp = db.Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz_utc_plus_1))

class Site(db.Model):
    __tablename__ = 'sites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location = db.Column(db.String(100))
    snmp_community = db.Column(db.String(50))
    status = db.Column(db.String(10))  # compute live

    def __repr__(self):
        return f"<Site {self.name}>"

    def __str__(self):  # ✅ Flask-Admin uses this!
        return self.name

    
default_time = lambda: datetime.utcnow() + timedelta(hours=1)

class SiteLogs(db.Model):
    __tablename__ = 'sitelogs'  # ✅ corrected typo

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'))
    # timestamp = db.Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(tz_utc_plus_1))
    timestamp = db.Column(db.DateTime, default=default_time)

    status = db.Column(db.String(10))

    site = db.relationship('Site', backref='logs')

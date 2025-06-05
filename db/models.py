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
    snmp_community = db.Column(db.String(50), default="public")
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
    latency = db.Column(db.Float, nullable=True)  # ping response time in ms


    site = db.relationship('Site', backref='logs')



class SNMPMetricLog(db.Model):
    __tablename__ = 'snmp_metric_log'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey("sites.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=default_time, index=True)

    oid = db.Column(db.String(128), nullable=False)        # Full OID
    label = db.Column(db.String(64), nullable=False)       # e.g. sysUpTime, ifDescr.1
    value = db.Column(db.String(256), nullable=False)      # Always stored as string

    site = db.relationship("Site", backref="snmp_logs")


class SNMPCurrent(db.Model):
    __tablename__ = 'snmp_current'

    site_id = db.Column(db.Integer, db.ForeignKey("sites.id"), primary_key=True)
    label = db.Column(db.String(64), primary_key=True)     # Composite key with site_id
    oid = db.Column(db.String(128), nullable=False)        # Full OID
    value = db.Column(db.String(256), nullable=False)
    last_updated = db.Column(db.DateTime, default=default_time)

    site = db.relationship("Site", backref="snmp_current")


class SNMPOID(db.Model):
    __tablename__ = 'snmp_oids'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)
    oid = db.Column(db.String(128), nullable=False)
    label = db.Column(db.String(64), nullable=True)
    port = db.Column(db.Integer, nullable=False, default=161)

    site = db.relationship('Site', backref='snmp_oids')

    def __repr__(self):
        return f"<SNMPOID site_id={self.site_id} oid={self.oid} port={self.port}>"


class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=default_time)
    status = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)

    site = db.relationship("Site", backref="alerts")
    

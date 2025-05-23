# defines the db tables, using sqlalchemy.
# This is where you describe, in Python, the shape of your data
# This is where you describe, in Python, the shape of your data
# This is where you describe, in Python, the shape of your data:


# basically here, this models.py is the translator of the ORM(object relational M smth) which is SQLAlchemy cuz raw sql is annoying.

# the stuff is creating two tables.
from app.extensions import db

class Site(db.Model):
    __tablename__ = 'sites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location = db.Column(db.String(100))
    snmp_community = db.Column(db.String(50))
    status = db.Column(db.String(10))  # optional, or compute live

# class Logs(db.Model):
#     __talbename__ ='Logs'
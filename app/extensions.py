# app/extensions.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#instead of creating the db in __init__, u create it here to avoid circular imports
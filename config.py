import os

from flask import app

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://nms_user:vayvanna@localhost/nms_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# This file just holds your connection URL (and maybe other settings):



    # Add your custom settings here
    USE_AUTH = True
    LOGIN_USERNAME = 'admin'
    LOGIN_PASSWORD = 'secret'
    SECRET_KEY = 'supersecretkey'  # Flask session secret
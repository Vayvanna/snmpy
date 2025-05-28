from datetime import timedelta
import os

from flask import app

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://nms_user:vayvanna@db:5432/nms_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=600) 


# This file just holds the connection URL (and maybe other settings):



    # Add your custom settings here
    USE_AUTH = True
    
    # LOGIN_USERNAME = 'admin'
    LOGIN_USERNAME= os.getenv("LOGIN_USERNAME")
    # LOGIN_PASSWORD = 'secret'
    LOGIN_PASSWORD= os.getenv("LOGIN_PASSWORD")
    # SECRET_KEY = 'supersecretkey'  # Flask session secret
    SECRET_KEY = os.getenv("SECRET_KEY")  # Flask session secret



    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    TELEGRAM_CHAT_ID2 = os.getenv("TELEGRAM_CHAT_ID2")

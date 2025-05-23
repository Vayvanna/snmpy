# this app is responsible for creating the Flask web app & loads its config from ../config/settings.json
# it gets called from run.py.
from flask import Flask # importing the core app.
from app.routes import main_bp ##  importing the main: the mini-app blueprint object.

from flask_sqlalchemy import SQLAlchemy # importing sqlalchemy.
from config import Config # importing config.py at root level.
from app.extensions import db  # ✅ Now cleanly imports db
from core.init_sites import sync_sites_from_json
from app.admin import init_admin  #####importing the init_admin function that attaches the the app & 
# db = SQLAlchemy() 

def create_app():  ## this function is to configure the Flask app.
    app = Flask(__name__) ## instance of app Flask

    app.config.from_object(Config) # 
    db.init_app(app) ## binding db to the app. This connects your Flask app to the database via SQLAlchemy

    ###we have the PostgreSQL running its engine in the linux env, and here we are linking it to be the db of our app. which we are creating atm.
    # the configuration of the connection of these are in snmpy/config.py


    app.register_blueprint(main_bp) ## registering our main mini-app inside the app.
    
    with app.app_context():
        sync_sites_from_json()           # ✅ auto-import on startup # to disable tempo
        from core.poller import start_background_thread
        start_background_thread(app)

        #####this is the part for the flask_Admin
        init_admin(app)
    return app
    
#     return app ## returning the configured app instance.


# from core.poller import start_background_thread
# start_background_thread()
# We move the start_background_thread() inside app.app_context() to avoid errors where Flask context is not ready.

# ✅ Summary of __init__.py
# Creates Flask app

# Loads settings (including DB URL)

# Initializes DB with SQLAlchemy

# Registers routes

# Starts the background ping thread
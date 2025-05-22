# this app is responsible for creating the Flask web app & loads its config from ../config/settings.json
# it gets called from run.py.
from flask import Flask # importing the core app.
from app.routes import main_bp ##  importing the main: the mini-app blueprint object.
def create_app():  ## this function is to configure the Flask app.
    app = Flask(__name__) ## instance of app Flask
    app.register_blueprint(main_bp) ## registering our main mini-app inside the app.
    return app ## returning the configured app instance.


from core.poller import start_background_thread
start_background_thread()

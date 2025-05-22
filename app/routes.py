# handles the pages(like html pages) and APIs endpoints within the site
# e.g: @app.route("/")
#    : @app.route("/api/sites")

# it'll have functions that react to when someone opens a specific url.

# app/routes.py
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/status')
def status():
    # temporary dummy data
    devices = [
        {'name': 'Router 1', 'status': 'UP'},
        {'name': 'Switch 2', 'status': 'DOWN'},
        {'name': 'Firewall 3', 'status': 'UP'}
    ]
    return render_template('status.html', devices=devices)

## handles the pages(like html pages) and APIs endpoints within the site
## e.g: @app.route("/")
##    : @app.route("/api/sites")

## it'll have functions that react to when someone opens a specific url.

## app/routes.py

from flask import Blueprint, render_template
## Blueprint can be used to split app in modulars. 
## render_template is here to load HTML files.

main_bp = Blueprint('main',__name__)
## Blueprint creates a mini-app inside our app, called main.
@main_bp.route('/') ## defines a route for when someone visits localhost:5000/ <-
def index():  ## when that happens, this function(index) runs.
    ## gonna stuff it now with hard values, no api no actual data.
    stats = {
        'sites_up': 87,
        'sites_down': 13
    }
    return render_template('index.html',stats=stats) ## we pass to index.html some values using jinga(flask templating engine)

@main_bp.route('/map')
def map():
    sites_locations = [
        {"name": "Tunis - Direction IT","lat":36.8065, "lon": 10.1815, 'status': 'UP'}, ##direction IT
        {"name": "Siege","lat": 33.8869, "lon": 9.5375, 'status': 'UP'}, ##siege
        {"name": "Sfax ", "lat": 34.7390, "lon": 10.7603, 'status': 'DOWN'},  # Sfax
    ]
    return render_template('map.html', locations=sites_locations)
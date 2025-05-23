## handles the pages(like html pages) and APIs endpoints within the site
## e.g: @app.route("/")
##    : @app.route("/api/sites")

## it'll have functions that react to when someone opens a specific url.

## app/routes.py

from flask import Blueprint, jsonify, render_template
## Blueprint can be used to split app in modulars. 
## render_template is here to load HTML files.
import subprocess # for pings

from core.poller import full_site_status
from snmpy.db.models import Site




main_bp = Blueprint('main',__name__)
## Blueprint creates a mini-app inside our app, called main.
@main_bp.route('/') ## defines a route for when someone visits localhost:5000/ <-
def index():  ## when that happens, this function(index) runs.
    ## gonna stuff it now with hard values, no api no actual data.
    number_sites=len(full_site_status)
    number_sites_up=giveNumberSitesUp()
    number_sites_down=number_sites-number_sites_up
    stats = {
        'sites': number_sites,
        'sites_up': number_sites_up,
        'sites_down': number_sites_down
    }
    return render_template('index.html',stats=stats) ## we pass to index.html some values using jinga(flask templating engine)



def giveNumberSitesUp():
    sum=0
    for site_id in full_site_status:
        if full_site_status[site_id]["status"].lower()=='up':    
            sum+=1
    return sum

def ping_host(ip):
    try:
        # 1 ping & 3 sec wait.
        output= subprocess.run(['ping','-c','1','-W','3',ip],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL) ## we are doing a ping -c 1 on that ip and waiting 3 sec for response, and directing stdoout & error to devnull.
        return output.returncode== 0   # 0 for success # if success return 0
    except Exception as e: # if not success then raise exception
        print(f"Error pinging {ip}: {e}")
        return False





# @main_bp.route('/map')
# def map():
#     # sites = [
#     #     {"name": "Tunis - Direction IT","lat":36.8144, "lon": 10.1759, 'ip': '8.8.8.8'}, ##direction IT 
#     #     {"name": "Siege","lat": 36.8219, "lon": 10.1942, 'ip': '192.168.100.0'}, ##siege 
#     #     {"name": "Sfax ", "lat": 34.7390, "lon": 10.7603, 'ip': '1.1.1.1'},  # Sfax
#     #     {"name": "Hammamet ", "lat": 36.4058, "lon": 10.6047, 'ip': '8.8.4.4'},  # Hammamet 
#     # ]

#     # sites_locations=[]
#     # for site in sites:
#     #     is_up = ping_host(site["ip"])
#     #     status= "UP" if is_up else "DOWN"
#     #     sites_locations.append({
#     #         "name":site["name"],
#     #         "lat":site["lat"],
#     #         "lon":site["lon"],
#     #         "status":status,
#     #     }
#     #     )
#     locations=list(full_site_status)
#     print(full_site_status)
#     print(list(locations))

#     return render_template('map.html', locations=locations)

@main_bp.route('/map')
def map():
    sites = Site.query.all() # goes to Site in db.models and queries everything, and puts it in sites, 
    # Convert to dict for frontend
    locations = {     #creates list: locations as following, while pulling from sites which we got from Site.models.db.
        str(site.id): {
            "name": site.name,
            "lat": site.latitude,
            "lon": site.longitude,
            "status": site.status
        }
        for site in sites
    }
    return render_template("map.html", locations=locations)





# @main_bp.route('/api/sites_status')
# def api_sites_status():
#     return jsonify(full_site_status)

@main_bp.route('/api/sites_status')
def api_sites_status():
    sites = Site.query.all() # goes to Site in db.models and queries everything, 
    data = {    #creates list: data as following, while pulling from Site in db.models.
        str(site.id): {
            "name": site.name,
            "lat": site.latitude,
            "lon": site.longitude,
            "status": site.status
        }
        for site in sites
    }
    return jsonify(data)

# this is the part that listens to Http requests.


from flask import Blueprint, current_app, jsonify, render_template, request
from db.models import Site, SiteLogs  # SQLAlchemy model representing the 'sites' table in PostgreSQL
from app.extensions import db
from utils.auth import login_required
main_bp = Blueprint('main', __name__)# creates blueprint object called main_bp




from flask import render_template, request, redirect, session, url_for, flash

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    session.permanent = True
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        if (
            u == current_app.config['LOGIN_USERNAME'] and
            p == current_app.config['LOGIN_PASSWORD']
        ):
            session['logged_in'] = True
            flash("Logged in successfully!", "success")
            next_page = request.args.get('next') or url_for('main.index')
            return redirect(next_page)
        else:
            flash("Invalid credentials", "error")
    return render_template('login.html')

@main_bp.route('/logout')
def logout():
    session.clear()
    flash("You’ve been logged out.")
    return redirect(url_for('main.login'))


# @main_bp.after_request
# def expire_session(response):
#     session.pop('logged_in', None)
#     return response


@main_bp.route('/')
def index():
    # Query the number of total sites from the DB
    total_sites = Site.query.count()
    # Count how many sites are up
    up_sites = Site.query.filter_by(status='up').count()
    # Down sites is the difference
    down_sites = total_sites - up_sites

    stats = {
        'sites': total_sites,
        'sites_up': up_sites,
        'sites_down': down_sites
    }
    return render_template('index.html', stats=stats)

@main_bp.route('/map')#default to listenings to GET requests.
def map():
    # Pull all site records from DB
    sites = Site.query.all()

    # Convert each site to a dictionary for frontend
    locations = {
        str(site.id): {
            "name": site.name,
            "lat": site.latitude,
            "lon": site.longitude,
            "status": site.status
        } for site in sites
    }
    return render_template("map.html", locations=locations)

@main_bp.route('/api/sites_status')
def api_sites_status():
    # Return the same structure as /map but as JSON API
    sites = Site.query.all()
    data = {
        str(site.id): {
            "name": site.name,
            "lat": site.latitude,
            "lon": site.longitude,
            "status": site.status
        } for site in sites
    }
    return jsonify(data)

# Removed old hardcoded ping and status code using full_site_status
# All dynamic status and info is now pulled from PostgreSQL via SQLAlchemy



@main_bp.route('/charts')
def charts():
    logs = SiteLogs.query.order_by(SiteLogs.timestamp.desc()).limit(500).all()
    return render_template('charts.html', logs=logs)






from flask import jsonify
from sqlalchemy import func
from db.models import Site, SiteLogs
from app.extensions import db
from app.routes import main_bp

@main_bp.route('/api/stats')
def api_stats():
    total_sites = Site.query.count()
    up_sites = Site.query.filter_by(status='up').count()
    down_sites = total_sites - up_sites
    return jsonify({
        'sites': total_sites,
        'sites_up': up_sites,
        'sites_down': down_sites
    })

@main_bp.route('/api/logs_summary')
def api_logs_summary():
    results = (
        db.session.query(func.extract('hour', SiteLogs.timestamp).label('hour'), func.count())
        .group_by('hour')
        .order_by('hour')
        .all()
    )
    hours = [f"{int(row[0]):02d}" for row in results]
    counts = [row[1] for row in results]
    return jsonify({'hours': hours, 'counts': counts})



@main_bp.route('/logs')
@login_required
def logsphere():
    return render_template('logs.html')

@main_bp.route('/api/logs')
def api_logs():
    site_name= request.args.get('site')
    status = request.args.get('status')

    query=db.session.query(SiteLogs).join(Site)

    if site_name:
        query = query.filter(Site.name.ilike(f'%{site_name}%'))

    if status:
        query = query.filter(SiteLogs.status == status.lower())


    logs = query.order_by(SiteLogs.timestamp.desc()).limit(200).all()
 
    return jsonify([
        {
            "timestamp": log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "site": log.site.name,
            "status": log.status
        }
        for log in logs
    ])













































# ## handles the pages(like html pages) and APIs endpoints within the site
# ## e.g: @app.route("/")
# ##    : @app.route("/api/sites")

# ## it'll have functions that react to when someone opens a specific url.

# ## app/routes.py

# from flask import Blueprint, jsonify, render_template
# ## Blueprint can be used to split app in modulars. 
# ## render_template is here to load HTML files.
# import subprocess # for pings

# from core.poller import full_site_status
# from snmpy.db.models import Site




# main_bp = Blueprint('main',__name__)
# ## Blueprint creates a mini-app inside our app, called main.
# @main_bp.route('/') ## defines a route for when someone visits localhost:5000/ <-
# def index():  ## when that happens, this function(index) runs.
#     ## gonna stuff it now with hard values, no api no actual data.
#     number_sites=len(full_site_status)
#     number_sites_up=giveNumberSitesUp()
#     number_sites_down=number_sites-number_sites_up
#     stats = {
#         'sites': number_sites,
#         'sites_up': number_sites_up,
#         'sites_down': number_sites_down
#     }
#     return render_template('index.html',stats=stats) ## we pass to index.html some values using jinga(flask templating engine)



# def giveNumberSitesUp():
#     sum=0
#     for site_id in full_site_status:
#         if full_site_status[site_id]["status"].lower()=='up':    
#             sum+=1
#     return sum

# def ping_host(ip):
#     try:
#         # 1 ping & 3 sec wait.
#         output= subprocess.run(['ping','-c','1','-W','3',ip],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL) ## we are doing a ping -c 1 on that ip and waiting 3 sec for response, and directing stdoout & error to devnull.
#         return output.returncode== 0   # 0 for success # if success return 0
#     except Exception as e: # if not success then raise exception
#         print(f"Error pinging {ip}: {e}")
#         return False





# # @main_bp.route('/map')
# # def map():
# #     # sites = [
# #     #     {"name": "Tunis - Direction IT","lat":36.8144, "lon": 10.1759, 'ip': '8.8.8.8'}, ##direction IT 
# #     #     {"name": "Siege","lat": 36.8219, "lon": 10.1942, 'ip': '192.168.100.0'}, ##siege 
# #     #     {"name": "Sfax ", "lat": 34.7390, "lon": 10.7603, 'ip': '1.1.1.1'},  # Sfax
# #     #     {"name": "Hammamet ", "lat": 36.4058, "lon": 10.6047, 'ip': '8.8.4.4'},  # Hammamet 
# #     # ]

# #     # sites_locations=[]
# #     # for site in sites:
# #     #     is_up = ping_host(site["ip"])
# #     #     status= "UP" if is_up else "DOWN"
# #     #     sites_locations.append({
# #     #         "name":site["name"],
# #     #         "lat":site["lat"],
# #     #         "lon":site["lon"],
# #     #         "status":status,
# #     #     }
# #     #     )
# #     locations=list(full_site_status)
# #     print(full_site_status)
# #     print(list(locations))

# #     return render_template('map.html', locations=locations)

# @main_bp.route('/map')
# def map():
#     sites = Site.query.all() # goes to Site in db.models and queries everything, and puts it in sites, 
#     # Convert to dict for frontend
#     locations = {     #creates list: locations as following, while pulling from sites which we got from Site.models.db.
#         str(site.id): {
#             "name": site.name,
#             "lat": site.latitude,
#             "lon": site.longitude,
#             "status": site.status
#         }
#         for site in sites
#     }
#     return render_template("map.html", locations=locations)





# # @main_bp.route('/api/sites_status')
# # def api_sites_status():
# #     return jsonify(full_site_status)

# @main_bp.route('/api/sites_status')
# def api_sites_status():
#     sites = Site.query.all() # goes to Site in db.models and queries everything, 
#     data = {    #creates list: data as following, while pulling from Site in db.models.
#         str(site.id): {
#             "name": site.name,
#             "lat": site.latitude,
#             "lon": site.longitude,
#             "status": site.status
#         }
#         for site in sites
#     }
#     return jsonify(data)

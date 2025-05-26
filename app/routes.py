# this is the part that listens to Http requests.


from flask import Blueprint, current_app, jsonify, render_template, request
from db.models import Site, SiteLogs, SNMPMetricLog, SNMPCurrent, SNMPOID   # SQLAlchemy model representing the 'sites' table in PostgreSQL
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

@main_bp.route("/api/snmp_logs")
def api_snmp_logs():
    logs = SNMPMetricLog.query.order_by(SNMPMetricLog.timestamp.desc()).limit(50).all()
    return jsonify({
        "logs": [
            {
                "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "site_name": log.site.name,
                "label": log.label,
                "value": log.value
            }
            for log in logs
        ]
    })


@main_bp.route('/snmp')
@login_required
def snmp_monitor():
    sites = Site.query.all()
    return render_template('snmp.html', sites=sites)

@main_bp.route('/api/snmp_current')
def api_snmp_current():
    site_id = request.args.get('site_id')
    query = SNMPCurrent.query.join(Site)
    
    if site_id:
        query = query.filter(SNMPCurrent.site_id == site_id)
    
    current_data = query.order_by(SNMPCurrent.last_updated.desc()).limit(100).all()
    
    return jsonify([{
        "site": data.site.name,
        "label": data.label,
        "value": data.value,
        "last_updated": data.last_updated.strftime("%Y-%m-%d %H:%M:%S")
    } for data in current_data])

from flask import session, redirect, url_for, request, current_app, flash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_app.config.get('USE_AUTH', False):
            return f(*args, **kwargs)
        if session.get('logged_in'):
            return f(*args, **kwargs)
        flash("Please log in to access this page.")
        return redirect(url_for('main.login', next=request.path))
    return decorated_function

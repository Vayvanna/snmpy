# app/admin.py 

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.extensions import db
from db.models import Site
from db.models import SiteLogs
admin= Admin(name='SNMPy Admin', template_mode='bootstrap3')
from flask import session, redirect, url_for, request, flash
from flask_admin import expose

# Custom view for Site
class SiteAdmin(ModelView):
    form_columns = ['name', 'ip_address', 'latitude', 'longitude', 'location', 'snmp_community', 'status']

    def is_accessible(self):
        # Optional: skip auth if USE_AUTH is False
        from flask import current_app
        print("USE_AUTH:", current_app.config.get("USE_AUTH"))
        print("session logged_in:", session.get("logged_in"))
        if not current_app.config.get("USE_AUTH"):
            return True
        return session.get("logged_in", False)

    def inaccessible_callback(self, name, **kwargs):
        flash("You must be logged in to access the admin panel.", "error")
        return redirect(url_for("main.login", next=request.path))

# Custom view for SiteLogs
class SiteLogsAdmin(ModelView):
    column_list = ['id', 'site', 'timestamp', 'status']
    form_columns = ['site', 'timestamp', 'status']

    def scaffold_form(self):
        form_class = super().scaffold_form()
        form_class.site.query_factory = lambda: Site.query.all()
        return form_class

    def is_accessible(self):
        from flask import current_app
        print("USE_AUTH:", current_app.config.get("USE_AUTH"))
        print("session logged_in:", session.get("logged_in"))

        if not current_app.config.get("USE_AUTH"):
            return True
        return session.get("logged_in", False)

    def inaccessible_callback(self, name, **kwargs):
        flash("You must be logged in to access the admin panel.", "error")
        return redirect(url_for("main.login", next=request.path))


admin = Admin(name='SNMPy Admin', template_mode='bootstrap3')

# from utils.auth import login_required
def init_admin(app):
    # @login_required
    admin.init_app(app)
    admin.add_view(SiteAdmin(Site,session=db.session))
    admin.add_view(SiteLogsAdmin(SiteLogs,session=db.session))



# This:

#     Creates an Admin instance

#     Registers the Site model

#     Connects it to your db.session (PostgreSQL)
# app/admin.py 

from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request, flash, current_app
from app.extensions import db
from db.models import Site, SiteLogs

# Custom AdminIndexView
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_app.config.get("USE_AUTH") and not session.get("logged_in"):
            flash("You must be logged in to access the admin panel.", "error")
            return redirect(url_for('main.login', next=request.url))
        return super().index()

# Custom model views
class SiteAdmin(ModelView):
    form_columns = ['name', 'ip_address', 'latitude', 'longitude', 'location', 'snmp_community', 'status']

    def is_accessible(self):
        if not current_app.config.get("USE_AUTH"):
            return True
        return session.get("logged_in", False)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("main.login", next=request.path))

class SiteLogsAdmin(ModelView):
    column_list = ['id', 'site', 'timestamp', 'status']
    form_columns = ['site', 'timestamp', 'status']

    def scaffold_form(self):
        form_class = super().scaffold_form()
        form_class.site.query_factory = lambda: Site.query.all()
        return form_class

    def is_accessible(self):
        if not current_app.config.get("USE_AUTH"):
            return True
        return session.get("logged_in", False)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("main.login", next=request.path))

# Admin object (no app passed yet)
# admin = Admin(name='SNMPy Admin', template_mode='bootstrap3', index_view=MyAdminIndexView(), base_template='admin/custom_master.html')
admin = Admin(
    name='SNMPy Admin',
    template_mode='bootstrap3',
    index_view=MyAdminIndexView()
    # base_template='admin/custom_master.html'  # ✅ just the relative path
)

# Hook called from app factory
def init_admin(app):
    admin.init_app(app)
    admin.add_view(SiteAdmin(Site, db.session))
    admin.add_view(SiteLogsAdmin(SiteLogs, db.session))




# This:

#     Creates an Admin instance

#     Registers the Site model

#     Connects it to your db.session (PostgreSQL)

# note for tmrw:
# So basically, tomorrow I'm gonna try to fix this issue about the... I think I added a way to get to the index from the admin, and that fucked up, so hopefully tomorrow I fix that. And then move on to do other things.

# u can try to remove what u added, those links in admin.py or its <admin=..> definition.
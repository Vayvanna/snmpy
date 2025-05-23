# app/admin.py 

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.extensions import db
from db.models import Site
from db.models import SiteLogs
admin= Admin(name='SNMPy Admin', template_mode='bootstrap3')

# Custom view for Site
class SiteAdmin(ModelView):
    form_columns = ['name', 'ip_address', 'latitude', 'longitude', 'location', 'snmp_community', 'status']

# Custom view for SiteLogs
class SiteLogsAdmin(ModelView):
    column_list = ['id', 'site', 'timestamp', 'status']  # display Site relationship, not site_id
    form_columns = ['site', 'timestamp', 'status']       # use site relationship, not site_id

    def scaffold_form(self):
        form_class = super().scaffold_form()
        form_class.site.query_factory = lambda: Site.query.all()  # dropdown will show all Sites
        return form_class

admin = Admin(name='SNMPy Admin', template_mode='bootstrap3')

def init_admin(app):
    admin.init_app(app)
    admin.add_view(SiteAdmin(Site,session=db.session))
    admin.add_view(SiteLogsAdmin(SiteLogs,session=db.session))



# This:

#     Creates an Admin instance

#     Registers the Site model

#     Connects it to your db.session (PostgreSQL)
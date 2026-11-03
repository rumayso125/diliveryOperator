from sqladmin import Admin

from mysite.admin.views import OrderAdmin, ProductAdmin, UserAdmin
from mysite.database.db import engine


def setup_admin(app):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(OrderAdmin)
    return admin

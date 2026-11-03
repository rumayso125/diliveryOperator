
from sqladmin import ModelView

from mysite.database.models import Order, Product, UserProfile


class UserAdmin(ModelView, model=UserProfile):
    column_list = [
        UserProfile.id,
        UserProfile.username,
        UserProfile.email,
        UserProfile.phone_number,
        UserProfile.registered_date,
    ]
    column_searchable_list = [
        UserProfile.username,
        UserProfile.email,
    ]
    form_excluded_columns = [UserProfile.password]


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id,
        Product.category,
        Product.store,
        Product.product_name,
        Product.price,
        Product.created_date,
    ]
    column_searchable_list = [Product.product_name]


class OrderAdmin(ModelView, model=Order):
    column_list = [
        Order.id,
        Order.user_id,
        Order.product_id,
        Order.order_status,
        Order.created_date,
    ]
    column_sortable_list = [
        Order.id,
        Order.created_date,
    ]

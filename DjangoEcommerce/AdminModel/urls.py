from django.urls import path
from .views import *
urlpatterns = [
    path("", all_esite_details),
    path("get_users_name/", get_users_name),
    path("get_orders/", get_order_by_trns_id),
    path("get_deliverd_or_pending/", get_deliverd_or_pending),
    path("get_address_for_popup/", get_address_forpopup),
    path("cust_detail/<int:id>/", cust_detail, name="cust_detail"),
    path("get_reviews_onstars/", get_reviews_onstars)
]

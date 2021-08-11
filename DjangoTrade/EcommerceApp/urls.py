from django.urls import path,include
from .views import paithani,semi_paithani,silk_wear,traditional_wear,western_wear,product_details,searched_products


urlpatterns = [
    path("paithani/", paithani,name="paithani"),
    path("semi_paithani/", semi_paithani,name="semi_paithani"),
    path("silk_saree/", silk_wear,name="silk_saree"),
    path("traditional_wear/", traditional_wear,name="traditional_wear"),
    path("western_wear/", western_wear, name="western_wear"),
    path("product_details/<int:pk>/", product_details, name="product_details"),
    path("searhced_products/",searched_products,name="searched_products")
]
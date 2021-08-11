"""EcommerceProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from EcommerceApp.views import *
from django.conf.urls.static import static
from django.conf import settings


from django.views.static import serve
from django.urls import re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', store, name="store"),
    path("cart/", cart, name="cart"),
    path("signup/", signupForm, name="signup"),
    path("logout/",logoutUser,name="logout"),
    path('login/', loginPage, name="login"),
    path("wears/", include("EcommerceApp.urls")),
    path("update/", update_item, name="update"),
    path("cart/", cart, name="cart"),
    path("chekcout/", checkout, name="checkout"),
    path("process_order/", processOrder, name="process_order"),
    path("update_address/", updateAddress, name="updateAddress"),
    path("update_review/", update_review, name="update_review"),
    path("activate_email/<uidb64>/<token>/", activateEmailAccount, name="activate_email"),
    path("request_reset_email/", RequestResetPasswordView.as_view(), name="request_reset_email"),
    path("set_new_password/<uidb64>/<token>/", SetNewPasswordView.as_view(), name="set_new_password"),
    path("username_validation/", UserNameValidation.as_view(), name="username_validation"),
    path("useremail_validation/", UserEmailValidation.as_view(), name="useremail_validation"),
    path("postalcode_validation/",PostalCodeValidation.as_view(),name="postalcode_validation"),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),

    path("AdminModel/",include('AdminModel.urls'))
    
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT) 

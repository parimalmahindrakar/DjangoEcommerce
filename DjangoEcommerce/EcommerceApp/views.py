import re
from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
import json
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .forms import ShippingAddressForm, CreateUserForm, CheckPincode
from .utils import cartData, token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random
from django.db.models import Q
import requests
from django.views.generic import View
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template import RequestContext


def handler404(request, exception):
    return render(request, "404.html")


# THIS IS THE CREDENTIALS SYSTEM ***************************************************


def activateEmailAccount(request, uidb64, token):

    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if not token_generator.check_token(user, token):
            return redirect("login")
        if user.is_active:
            return redirect("login")
        user.is_active = True
        user.save()
        messages.success(request, "Account activated successfully !")
        return redirect("login")
    except:
        pass
    return redirect("login")


def validate_email(email):
    if len(email) > 6:
        if re.match("\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b", email) != None:
            return True
    return False


def some():
    print("fuck")


class RequestResetPasswordView(View):
    def get(self, request):
        return render(request, "password_reset/request_reset_email.html")

    def post(self, request):
        email = request.POST.get("email")
        if validate_email(email):
            messages.error(request, "Please enter the valid emailid")
            return render(request, "password_reset/request_reset_email.html")
        user = User.objects.filter(email=email)

        if user.exists():
            user = user[0]
            current_site = get_current_site(request)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            msg = render_to_string(
                "password_reset/request_reset_password.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": uidb64,
                    "token": PasswordResetTokenGenerator().make_token(user),
                },
            )

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            email = EmailMessage(
                "[Reset your password]", msg, email_from, recipient_list
            )
            email.send()

            messages.success(
                request,
                "We have sent you an email with instructions on how to reset your password",
            )
            return render(request, "password_reset/request_reset_email.html")
        else:
            messages.error(
                request, "User does not exists corresponding to this email.")
            return render(request, "password_reset/request_reset_email.html")


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {"uidb64": uidb64, "token": token}
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Password reset link is invalid !")
                return redirect("login")
        except:
            pass
        return render(request, "password_reset/set_new_password.html", context)

    def post(self, request, uidb64, token):
        context = {"uidb64": uidb64, "token": token}
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords don't match. Enter again !")
            return render(request, "password_reset/set_new_password.html", context)

        SpecialSym = ["$", "@", "#", "%"]
        if len(password1) < 6:
            messages.error(
                request, "You should use atlease 8 characters. Enter again !"
            )
            return render(request, "password_reset/set_new_password.html", context)

        if not any(char.isdigit() for char in password1):
            messages.error(
                request, "Password should have at least one numeral !")
            return render(request, "password_reset/set_new_password.html", context)

        if not any(char.isupper() for char in password1):
            messages.error(
                request, "Password should have at least one uppercase letter !"
            )
            return render(request, "password_reset/set_new_password.html", context)

        if not any(char.islower() for char in password1):
            messages.error(
                request, "Password should have at least one lowercase letter"
            )
            return render(request, "password_reset/set_new_password.html", context)

        if not any(char in SpecialSym for char in password1):
            messages.error(
                request, "Password should have at least one of the symbols $@#"
            )
            return render(request, "password_reset/set_new_password.html", context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            user.set_password(password1)
            user.save()
            messages.success(request, "Password was reset.")
            return redirect("login")
        except:
            messages.error(request, "Something went wrong !")
            return render(request, "password_reset/set_new_password.html", context)
        return render(request, "password_reset/set_new_password.html", context)


class UserNameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]
        if not str(username).isalnum():
            return JsonResponse(
                {
                    "UsernameError": "Username should contain only alphabates and numbers."
                }
            )
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"UsernameError": "Username is already taken. Enter a new one."}
            )
        return JsonResponse({"UsernameSuccess": True})


class UserEmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        useremail = data["useremail"]
        if User.objects.filter(email=useremail).exists():
            return JsonResponse({"UserEmailError": "Emailid is already registered."})
        return JsonResponse({"UserEmailSuccess": True})


class PostalCodeValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        postalcode = data["postalcode"]
        url = "http://127.0.0.1:4545/%d/" % (int(postalcode))
        data = requests.get(url)
        data = data.json()
        if data["data"]["is_available"] == False:
            return JsonResponse({"POSTAL_CODE": False})
        else:
            return JsonResponse({"POSTAL_CODE": True, "area_info": data})


def signupForm(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            print("before username")
            username = form.cleaned_data.get("username")
            print("after username : "+username)
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            link = reverse(
                "activate_email",
                kwargs={"uidb64": uidb64,
                        "token": token_generator.make_token(user)},
            )
            # activate_url = "http://"+domain+link
            activate_url = "http://35.238.237.157" + link
            email = form.cleaned_data.get("email")
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            msg = (
                "Please use following email to activate your account !\n" + activate_url
            )
            email = EmailMessage(
                "Activate your account !", msg, email_from, recipient_list
            )
            email.send()

            name = (
                form.cleaned_data.get("first_name")
                + " "
                + form.cleaned_data.get("last_name")
            )
            phone = form.cleaned_data.get("phone")
            address = form.cleaned_data.get("address")
            city = form.cleaned_data.get("city")
            zipcode = form.cleaned_data.get("zipcode")
            state = form.cleaned_data.get("state")
            email = form.cleaned_data.get("email")
            Customer.objects.create(user=user, name=name, email=email)
            customer = Customer.objects.get(user=user)
            ShippingAddress.objects.create(
                customer=customer,
                phone=phone,
                address=address,
                city=city,
                zipcode=zipcode,
                state=state,
            )
            messages.success(
                request,
                "Account was created for "
                + username
                + ". Please verify your email id to login !",
            )
            return redirect("login")

    context = {"form": form}
    return render(request, "EcommerceApp/signup.html", {"form": form})


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("store")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("store")
            else:
                messages.info(request, "username or password is incorrect.")
                return render(request, "EcommerceApp/login.html")

        context = {}
        return render(request, "EcommerceApp/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


# THIS IS THE CREDENTIALS SYSTEM ***************************************************


# THIS IS THE STORE SYSTEM ***************************************************
@login_required(login_url="login")
def cart(request):

    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "EcommerceApp/cart.html", context)


def store(request):

    paithanis = Product.objects.filter(category__iexact="paithani")[:12]
    semi_paithanis = Product.objects.filter(
        category__iexact="semi_paithani")[:12]
    westerns = Product.objects.filter(category__iexact="western")[:12]
    traditionals = Product.objects.filter(category__iexact="traditional")[:12]
    silk_saree = Product.objects.filter(category__iexact="silk_saree")[:12]

    data = cartData(request)
    cartItems = data["cartItems"]
    context = {
        "paithanis": paithanis,
        "semi_paithanis": semi_paithanis,
        "westerns": westerns,
        "traditionals": traditionals,
        "silk_saree": silk_saree,
        "cartItems": cartItems,
    }
    return render(request, "EcommerceApp/store.html", context)


def paithani(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    paithanis = Product.objects.filter(category__iexact="paithani")
    context = {
        "paithanis": paithanis,
        "cartItems": cartItems,
    }
    return render(request, "wears/paithani.html", context)


def semi_paithani(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    semi_paithanis = Product.objects.filter(category__iexact="semi_paithani")
    context = {
        "semi_paithanis": semi_paithanis,
        "cartItems": cartItems,
    }
    return render(request, "wears/semi_paithani.html", context)


def western_wear(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    westerns = Product.objects.filter(category__iexact="western")
    context = {
        "westerns": westerns,
        "cartItems": cartItems,
    }
    return render(request, "wears/western_wear.html", context)


def traditional_wear(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    traditionals = Product.objects.filter(category__iexact="traditional")
    context = {
        "traditionals": traditionals,
        "cartItems": cartItems,
    }
    return render(request, "wears/traditional_wear.html", context)


def silk_wear(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    silk_saree = Product.objects.filter(category__iexact="silk_saree")
    context = {
        "silk_sarees": silk_saree,
        "cartItems": cartItems,
    }
    return render(request, "wears/silk_wear.html", context)


context_for_searched_products = {}


def searched_products(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    if request.method == "POST":
        data = json.loads(request.body)
        product_name = data["name"]
        products = Product.objects.filter(
            Q(category__icontains=product_name) | Q(
                name__icontains=product_name)
        )
        context_for_searched_products.clear()
        context_for_searched_products.update({"products": products})
        return JsonResponse("message captured", safe=False)
    context_for_searched_products.update({"cartItems": cartItems})
    return render(
        request, "wears/searched_products.html", context_for_searched_products
    )


def product_details(request, pk):
    product = Product.objects.get(id=pk)
    all_slider_products = Product.objects.all()
    all_slider_products_list = random.choices(all_slider_products, k=8)
    x = datetime.datetime.now()

    # this is the pincode verification start
    form = CheckPincode()
    if request.method == "POST":
        form = CheckPincode(request.POST)
        if form.is_valid():
            pincode = form.cleaned_data["Postal_Code"]
            url = "http://127.0.0.1:4545/%d/" % (pincode)
            data = requests.get(url)
            data = data.json()
            if data["data"]["is_available"] == False:
                messages.info(
                    request, "Service is closed for this pincode : " +
                    str(pincode)
                )
            elif data["data"]["is_available"] == True:
                messages.info(
                    request, "We are reachable for pincode : " + str(pincode))
    # this is the pincode verification end

    year = x.year
    month = x.strftime("%B")
    date = x.strftime("%d")
    data = cartData(request)
    cartItems = data["cartItems"]
    product_reviews = product.productreview_set.all()
    context = {
        "product": product,
        "year": year,
        "month": month,
        "date": date,
        "all_slider_products_list": all_slider_products_list,
        "cartItems": cartItems,
        "images": product.imagesURL,
        "product_reviews": product_reviews,
        "form": form,
    }
    return render(request, "wears/product_details.html", context)


# THIS IS THE STORE SYSTEM ***************************************************


# THIS IS THE PROCESSING SYSTEM ***************************************************


@login_required(login_url="login")
def checkout(request):

    customer = request.user.customer
    shippingaddress = customer.shippingaddress_set.all()
    form = ShippingAddressForm(instance=shippingaddress[0])
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    recent_orders = customer.order_set.filter(complete=True)

    recent_orders_dict = {}
    if recent_orders.exists():
        for i in recent_orders:
            recent_orders_dict.update({
                i: {
                    'product': [(j.product, j.quantity) for j in i.orderitem_set.filter(order=i)],
                    'is_deliverd': i.is_deliverd,
                    'date_ordered': i.date_ordered,
                    'date_deliverd': i.date_deliverd,
                    'transaction_id': i.transaction_id
                }
            })
    context = {"items": items, "order": order, "cartItems": cartItems,
               "form": form, "recent_orders_dict": recent_orders_dict}
    return render(request, "EcommerceApp/checkout.html", context)


@login_required(login_url="login")
def updateAddress(request):
    customer = request.user.customer
    shippingaddress = customer.shippingaddress_set.all()
    form = ShippingAddressForm(instance=shippingaddress[0])
    if request.method == "POST":
        form = ShippingAddressForm(request.POST, instance=shippingaddress[0])
        if form.is_valid():
            form.save()
            return redirect("/chekcout")
    return render(request, "EcommerceApp/update_address.html", {"form": form})


@login_required(login_url="login")
def update_review(request):
    data = json.loads(request.body)
    customer = request.user.customer
    product = Product.objects.get(id=data["productid"])
    review = data["review"]
    stars = data["stars"]
    ProductReview.objects.create(
        customer=customer, product=product, review=review, stars=stars
    )

    return JsonResponse(" review was aadded from python !", safe=False)


@login_required(login_url="login")
def update_item(request):
    data = json.loads(request.body)
    productid = data["productid"]
    action = data["action"]
    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse(" item was aadded !", safe=False)


@login_required(login_url="login")
def processOrder(request):
    date_ordered = datetime.datetime.now()
    transaction_id = datetime.datetime.now().timestamp()
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    order.transaction_id = transaction_id
    order.date_ordered = date_ordered
    print()
    total = order.get_cart_total
    order.complete = True
    order.save()
    orderitems = order.orderitem_set.all()
    shippingaddress = customer.shippingaddress_set.all()[0]
    username = customer.name
    message = f"""
    Username : {username}
    Mobile num : {shippingaddress.phone}
    Address : {shippingaddress.address}
    City : {shippingaddress.city}
    State: {shippingaddress.state}
    zipcode: {shippingaddress.zipcode}
    \n"""

    orderitems_list = []
    for i in orderitems:
        strings = (
            str(i.product)
            + " => "
            + str(i.product.price)
            + " => "
            + str(i.quantity)
            + "\n"
        )
        message += strings
    message += "\nThe total is : " + str(total) + "\n"

    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["parimalm4653@gmail.com"]
    email = EmailMessage("About sarees order", message,
                         email_from, recipient_list)
    email.send()
    messages.success(
        request,
        "Order is confirmed for "
        + str(username)
        + ". Please check your mail and be ready with your cash !",
    )
    return redirect("/")


# THIS IS THE PROCESSING SYSTEM ***************************************************

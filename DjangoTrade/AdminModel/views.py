from django.shortcuts import render, redirect
from EcommerceApp.models import *
from django.db.models import Q
from django.http import JsonResponse
import json


def all_esite_details(request):
    if request.user.is_superuser:
        users = Customer.objects.all()
        orders = Order.objects.filter(complete=True)

        delivered_orders = orders.filter(
            Q(is_deliverd=True) &
            Q(complete=True)
        ).count()

        pending_orders = orders.filter(
            Q(is_deliverd=False) &
            Q(complete=True)
        ).count()

        recent_orders = Order.objects.filter(complete=True)

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
        context = {
            'users': users,
            'total_orders': orders.count(),
            'delivered_orders': delivered_orders,
            'pending_orders': pending_orders,
            'orders': orders,
            'recent_orders_dict': recent_orders_dict
        }
        return render(request, "AdminModel/all_esite_details.html", context)
    else:
        return render(request, "404.html")


def get_users_name(request):
    if request.user.is_superuser:
        data = json.loads(request.body)
        name = data.get('name')
        custs = Customer.objects.filter(name__icontains=name)
        list_ = []
        for i in custs:
            list_.append(
                {
                    "id": i.id,
                    "name": i.name,
                    "date_created": str(i.date_created.strftime("%d"))+" "+str(i.date_created.strftime("%b"))+" "+str(i.date_created.strftime("%Y")),
                }
            )
        return JsonResponse({"data": list_})
    else:
        return render(request, "404.html")


def get_order_by_trns_id(request):
    if request.user.is_superuser:
        data = json.loads(request.body)
        id = data.get("id")
        recent_orders = Order.objects.filter(transaction_id=id)
        recent_orders_dict = {}
        if recent_orders.exists():
            for i in recent_orders:
                recent_orders_dict.update({
                    "cc": {
                        'product': [(str(j.product.name), str(j.quantity)) for j in i.orderitem_set.filter(order=i)],
                        'customer': i.customer.name,
                        'is_deliverd': i.is_deliverd,
                        'date_ordered': str(i.date_ordered.strftime("%d"))+" " + str(i.date_ordered.strftime("%b"))+" "+str(i.date_ordered.strftime("%Y")),
                        'date_deliverd': str(i.date_deliverd.strftime("%d"))+" " + str(i.date_deliverd.strftime("%b")) + " " + str(i.date_deliverd.strftime("%Y")) if i.is_deliverd else "None",
                    }
                })
        return JsonResponse({"data": recent_orders_dict})
    else:
        return render(request, "404.html")


def get_deliverd_or_pending(request):
    if request.user.is_superuser:
        data = json.loads(request.body)
        recent_orders = Order.objects.filter(
            Q(is_deliverd=data.get("status")) &
            Q(complete=True)
        )
        recent_orders_list = []
        if recent_orders.exists():
            for i in recent_orders:
                recent_orders_list.append(
                    {
                        'product': [(str(j.product.name), str(j.quantity)) for j in i.orderitem_set.filter(order=i)],
                        'transaction_id': i.transaction_id,
                        'is_deliverd': i.is_deliverd,
                        'date_ordered': str(i.date_ordered.strftime("%d"))+" " + str(i.date_ordered.strftime("%b"))+" "+str(i.date_ordered.strftime("%Y")),
                        'date_deliverd': str(i.date_deliverd.strftime("%d"))+" " + str(i.date_deliverd.strftime("%b")) + " " + str(i.date_deliverd.strftime("%Y")) if i.is_deliverd else "None",
                    }
                )
        recent_orders_list = recent_orders_list[::-1]
        return JsonResponse({"data": recent_orders_list})
    else:
        return render(request, "404.html")


def get_address_forpopup(request):
    if request.user.is_superuser:
        data = json.loads(request.body)
        if data.get("trns_id"):
            order = Order.objects.get(transaction_id=data.get("trns_id"))
            cust = order.customer
            address = cust.shippingaddress_set.get()
            city = cust.shippingaddress_set.get().city
            state = cust.shippingaddress_set.get().state
            pincode = cust.shippingaddress_set.get().zipcode
            return JsonResponse({"data": {
                "customer": str(cust),
                "address": str(address),
                "city": str(city),
                "state": str(state),
                "zipcode": str(pincode)
            }})

        return JsonResponse({"data": data})
    else:
        return render(request, "404.html")


def cust_detail(request, id):
    if request.user.is_superuser:
        customer = Customer.objects.get(id=id)
        username = str(customer.user)
        name = str(customer)
        email = str(customer.email)
        was_created = customer.date_created
        is_active = str(customer.user.is_active)
        address = str(customer.shippingaddress_set.get())
        location = str(customer.shippingaddress_set.get().city) + "-" + str(
            customer.shippingaddress_set.get().zipcode) + ", " + str(customer.shippingaddress_set.get().state) + "."
        related_reviews = customer.productreview_set.all()
        related_reviews = related_reviews[::-1]
        context = {
            "username": username,
            "name": name,
            "email": email,
            "was_created": was_created,
            "is_active": is_active,
            "address": address,
            "location": location,
            "related_reviews": related_reviews,
            "id_": customer.user.id
        }
        return render(request, "AdminModel/cust_detail.html", context)
    else:
        return render(request, "404.html")


def get_reviews_onstars(request):
    if request.user.is_superuser:
        data = json.loads(request.body)
        userid = int(data.get("userid"))
        stars = int(data.get("stars"))
        user = User.objects.get(id=userid).customer
        reviews = user.productreview_set.filter(stars=stars)
        context = {}
        if reviews:
            context = {
                "product": [str(i.product) for i in reviews],
                "review": [str(i.review) for i in reviews],
                "date_written": [str(i.date.strftime("%d")+" "+i.date.strftime("%b")+" "+i.date.strftime("%Y")) for i in reviews],
                "stars": [str(i.stars) for i in reviews],
                "count": reviews.count()
                # ""
            }
        print(context)
        return JsonResponse({"msg": context})
    else:
        return render(request, "404.html")


# {'product': ['paithani1', 'paithani1'], 'review': ['this is the awesome saree, every one must buy it.', 'this was very nice saree, '], 'date_written': ['2021-01-14 09:25:28.088135+00:00', '2021-01-14 09:33:09.372108+00:00'], 'stars': ['5', '5']}

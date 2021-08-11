from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField

CHOICES = (
    ("paithani", "paithani"),
    ("semi_paithani", "semi_paithani"),
    ("silk_saree", "silk_saree"),
    ("traditional", "traditional"),
    ("western", "western"),
)

IS_AVAILABLE = (("YES", "YES"), ("NO", "NO"))


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):

    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    phone = models.CharField(max_length=200)
    address = models.TextField()
    zipcode = models.IntegerField()
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField()
    image1 = models.ImageField(null=True,blank=True)
    image2 = models.ImageField(null=True,blank=True)
    image3 = models.ImageField(null=True,blank=True)
    image4 = models.ImageField(null=True,blank=True)
    image5 = models.ImageField(null=True,blank=True)
    image6 = models.ImageField(null=True,blank=True)
    image7 = models.ImageField(null=True,blank=True)
    image8 = models.ImageField(null=True,blank=True)
    image9 = models.ImageField(null=True,blank=True)
    image10 = models.ImageField(null=True,blank=True)
    category = models.CharField(max_length=20, choices=CHOICES)
    is_avaible = models.BooleanField(default=True)
    fabric = models.CharField(max_length=256, blank=True, null=True)
    pattern = models.CharField(max_length=256, blank=True, null=True)
    color = models.CharField(max_length=256, blank=True, null=True)
    style = models.CharField(max_length=256, blank=True, null=True)
    in_the_pack = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def imageurl(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url
    
    @property
    def imagesURL(self):
        images_list = []
        try:
            images_list.append(self.image1.url)
        except:
            return images_list
        try:
            images_list.append(self.image2.url)
        except:
            return images_list
        try:
            images_list.append(self.image3.url)
        except:
            return images_list
        try:
            images_list.append(self.image4.url)
        except:
            return images_list
        try:
            images_list.append(self.image5.url)
        except:
            return images_list
        try:
            images_list.append(self.image6.url)
        except:
            return images_list
        try:
            images_list.append(self.image7.url)
        except:
            return images_list
        try:
            images_list.append(self.image8.url)
        except:
            return images_list
        try:
            images_list.append(self.image9.url)
        except:
            return images_list
        try:
            images_list.append(self.image10.url)
        except:
            return images_list
        return images_list



        
class ProductReview(models.Model):
    
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.CharField(max_length=256,null=True,blank=True)
    stars = models.PositiveIntegerField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return str(self.customer.name)+" : "+ str(self.product.name)

class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_deliverd = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200)
    is_deliverd = models.BooleanField(default=False,blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_ordered = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


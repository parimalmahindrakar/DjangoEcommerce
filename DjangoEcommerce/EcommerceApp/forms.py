from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Customer
from django import forms
import requests

class CreateUserForm(UserCreationForm):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = forms.CharField(validators=[phone_regex], max_length=17)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=50)
    zipcode = forms.IntegerField()
    state = forms.CharField(max_length=80)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "phone",
            "address",
            "city",
            "zipcode",
            "state",
        ]
    def clean_zipcode(self):
        url = "http://127.0.0.1:4545/%d/" % (self.cleaned_data['zipcode'])
        data = requests.get(url)
        data = data.json()
        if data['data']['is_available'] == False:
            raise forms.ValidationError("We are unreachable for pincode : " + str(self.cleaned_data['zipcode']))
        else:
            return self.cleaned_data['zipcode']
        



        
class ShippingAddressForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = forms.CharField(validators=[phone_regex], max_length=17)
    class Meta:
        model = ShippingAddress
        fields = [
            'address',
            'phone',
            'city',
            'state',
            'zipcode'
        ]
    def clean_zipcode(self):
        url = "http://127.0.0.1:4545/%d/" % (self.cleaned_data['zipcode'])
        data = requests.get(url)
        data = data.json()
        if data['data']['is_available'] == False:
            raise forms.ValidationError("We are unreachable for pincode : " + str(self.cleaned_data['zipcode']))
        else:
            return self.cleaned_data['zipcode']


        
class CheckPincode(forms.Form):
    Postal_Code = forms.IntegerField()

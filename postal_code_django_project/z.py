import os,json
import django
django.setup()
from PostalCodesApp.models import PostalCodes
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PostalCodesProject.settings')

     

file = open("jsons/west-delhi.json")
file_dict = json.load(file)
for i, j in file_dict.items():
    PostalCodes.objects.create(area=i,code=int(j),city="West Delhi",state="Delhi")


# export DJANGO_SETTINGS_MODULE=PostalCodesProject.settings
# import django
# django.setup()                 order is compulsory like this
# from crudApp.models import Employee
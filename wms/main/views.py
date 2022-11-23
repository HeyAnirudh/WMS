
from django.shortcuts import render,HttpResponse, loader
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.shortcuts import render, HttpResponse, loader

import datetime
from datetime import date

# from django.conf import settings
# settings.configure()

credJson = credentials.Certificate("wms/service_key.json")
firebase_admin.initialize_app(credJson)
db = firestore.client()
db.collection('admin-data').document('s3').set({"Date":"23112022","Quantity":10})
k=db.collection('admin-data').document('s3').set({"Date":"23112022","Quantity":10})
print(k)


def index(request):

    context = {}
    html_template = loader.get_template("landing.html")

    return HttpResponse(html_template.render(context, request))


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def admin(request):
    storage=request.POST.get("storage_id")
    print(storage)
    quantity= request.POST.get("quantity")
    today=date.today()
    db.collection('admin-data').document(str(storage)).set({"Date":str(today),"Quantity":quantity})
    return render(request, "admin.html")


def dashboard(request):
    return render(request, "dashboard.html")


# Create your views here.

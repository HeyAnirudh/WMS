from django.shortcuts import render, HttpResponse, loader
from django.http import HttpResponseRedirect

# import pyrebase4
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.shortcuts import render, HttpResponse, loader
from transactions.deploy import deploy

import datetime
from datetime import date
import os

user = ""

# from django.conf import settings
# settings.configure()


def pH_Calc(pH):
    return 10 if pH == 7 else int(10 - (abs(pH - 7) / 0.5) * 2)


# turbidity calculation
def turb_Calc(turb):
    if turb > 0 and turb < 0.4:
        return 10
    elif turb > 0.4 and turb < 0.6:
        return 8
    elif turb > 0.6 and turb < 0.8:
        return 4
    elif turb > 0.8 and turb < 1.0:
        return 2
    else:
        return 0


# temperature calculation
def temp_Calc(temp):
    if temp in range(18, 35):
        return 10
    elif temp in range(35, 45) or temp in range(0, 18):
        return 8
    elif temp in range(45, 55):
        return 6
    elif temp in range(55, 65):
        return 4
    else:
        return 2


credJson = credentials.Certificate("wms/service_key.json")
firebase_admin.initialize_app(credJson)
db = firestore.client()
# db.collection("admin-data").document("s3").set({"Date": "23112022", "Quantity": 10})
# k = db.collection("admin-data").document("s3").set({"Date": "23112022", "Quantity": 10})
# print(k)


def index(request):

    context = {}
    html_template = loader.get_template("landing.html")

    return HttpResponse(html_template.render(context, request))


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def admin(request):
    context = {}
    flat = []
    quant = []
    flatno = request.POST.get("flatno")
    email = request.POST.get("email")
    print(flatno, email)
    today = date.today()
    if email:
        doc = db.collection("user-request").document(str(email))
        data = doc.get()
        data = data.to_dict()
        quantity = data["quantity"]
        data["email"] = email
        db.collection("user-request").document(str(email)).delete()
        db.collection("storage").document(str(email)).set(data)
        doc = db.collection("storage-facilites").document("s1")
        data = doc.get()
        data = data.to_dict()
        data["available"] = data["available"] + quantity
        print("data", data)
        db.collection("storage-facilites").document("s1").set(data)

        txn = {
            "hash": "0x60fa00aabaa02d42a8fa6773752ed6f86433492cb387d9cc8d7b090dfdadfdf3",
            "status": "Req Approved",
        }
        doc = db.collection("transactions").document(email)
        data = doc.get()
        data = data.to_dict()["transactions"]
        data.append(txn)
        db.collection("transactions").document(email).set({"transactions": data})

    data = db.collection("user-request").get()
    for doc in data:
        a = doc.to_dict()
        flat.append(a["flatno"])
        quant.append(a["quantity"])
        print(a)
    context["set"] = zip(flat, quant)

    print(context)

    return render(request, "admin.html", context)


def approveRequest(request):
    email = request.POST.get("email")


def dashboard(request):
    return render(request, "dashboard.html")


def invoice(request):
    print("user", user)
    return render(request, "invoice.html")


def trial(request):
    return render(request, "trial.html")


def waterTower(request):
    context = {}
    doc = db.collection("storage-facilites").document("s1")
    data = doc.get()
    data = data.to_dict()

    context = data

    return render(request, "waterTower.html", context)


def signup(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    metamask = request.POST.get("metamask")
    flat = request.POST.get("flat")
    society = request.POST.get("society")
    user = email
    db.collection("user-registration").document(str(email)).set(
        {
            "email": email,
            "password": password,
            "metamask": metamask,
            "flat": flat,
            "society": society,
        }
    )
    return render(request, "landing.html")


def signin(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    doc_ref = db.collection("user-registration").document(str(email))
    doc = doc_ref.get()
    if doc.exists:
        doc = doc.to_dict()
        if password == doc["password"]:
            context = {"user": email}
            user = email
            return render(request, "dashboard.html", context)
        else:
            print("Wrong Password")
            return render(request, "login.html")
    else:
        print("No such user!")
        return render(request, "register.html")


def deployContract(request):
    # sender = request.POST.get("sender")
    # receiver = request.POST.get("receiver")
    email = request.POST.get("email")
    sender = os.getenv("STORAGE_ADDR")
    receiver = os.getenv("USER_ADDR")
    quality = 80
    doc_ref = db.collection("storage").document(str(email))
    data = doc_ref.get()
    quantity = data.to_dict()["quantity"]
    # quantity = 28
    print(sender)
    txnhash = deploy(sender, receiver, quantity, quality)
    txn = {"hash": txnhash, "status": "To User"}

    doc = db.collection("transactions").document(email)
    data = doc.get()
    data = data.to_dict()["transactions"]
    data.append(txn)
    db.collection("transactions").document(email).set({"transactions": data})

    db.collection("storage").document(str(email)).delete()

    return HttpResponseRedirect("/storage/")


def deployContract2(request):
    # sender = request.POST.get("sender")
    # receiver = request.POST.get("receiver")
    sender = os.getenv("TOWER_ADDR")
    receiver = os.getenv("STORAGE_ADDR")
    quality = int(request.POST.get("quality"))
    quantity = int(request.POST.get("quantity"))
    email = "avishjain0@gmail.com"
    print(quality, quantity)
    txnhash = deploy(sender, receiver, quantity, quality)

    txn = {"hash": txnhash, "status": "Storage Facility"}

    db.collection("storage-facilites").document("s1").set(
        {
            "capacity": 10000,
            "available": 0,
        }
    )
    doc = db.collection("transactions").document(email)
    data = doc.get()
    data = data.to_dict()["transactions"]
    data.append(txn)
    db.collection("transactions").document(email).set({"transactions": data})

    doc = db.collection("storage-facilites").document("s2")
    data = doc.get()
    data = data.to_dict()
    print(data)
    newData = {
        "capacity": data["capacity"],
        "available": data["available"] + quantity,
    }
    db.collection("storage-facilites").document("s2").set(newData)

    return HttpResponseRedirect("/watertower/")


def storage(request):
    # login starts

    context = {}
    flat = []
    quant = []
    email = []
    data = db.collection("storage").get()
    print(data)
    for doc in data:
        a = doc.to_dict()
        flat.append(a["flatno"])
        quant.append(a["quantity"])
        email.append(a["email"])
        print(a)
    context["set"] = zip(flat, quant, email)
    print(context)

    return render(request, "storage.html", context)


def calculate(request):
    context = {}
    print(request.POST.get("temp"))
    print(request.POST.get("turbi"))
    print(request.POST.get("ph"))

    doc = db.collection("storage-facilites").document("s1")
    data = doc.get()
    data = data.to_dict()
    context = data

    context["temp"] = request.POST.get("temp")
    context["ph"] = request.POST.get("ph")
    context["turbi"] = request.POST.get("turbi")
    ph_cal = pH_Calc(int(context["ph"]))
    turb_cal = turb_Calc(float(context["turbi"]))
    temp_cal = temp_Calc(int(context["temp"]))
    if ph_cal < 5 or turb_cal < 5 or temp_cal < 3:
        context["ans"] = 10
    else:
        context["ans"] = (
            (
                pH_Calc(int(context["ph"]))
                + turb_Calc(float(context["turbi"]))
                + temp_Calc(int(context["temp"]))
            )
            // 3
        ) * 10
    print(context["ans"])
    data = db.collection("admin-data").get()
    print(data)
    return render(request, "waterTower.html", context)


def calculate2(request):
    context = {}
    print(request.POST.get("temp"))
    print(request.POST.get("turbi"))
    print(request.POST.get("ph"))

    context["temp"] = request.POST.get("temp")
    context["ph"] = request.POST.get("ph")
    context["turbi"] = request.POST.get("turbi")
    ph_cal = pH_Calc(int(context["ph"]))
    turb_cal = turb_Calc(float(context["turbi"]))
    temp_cal = temp_Calc(int(context["temp"]))
    if ph_cal < 5 or turb_cal < 5 or temp_cal < 3:
        context["ans"] = 10
    else:
        context["ans"] = (
            (
                pH_Calc(int(context["ph"]))
                + turb_Calc(float(context["turbi"]))
                + temp_Calc(int(context["temp"]))
            )
            // 3
        ) * 10
    print(context["ans"])
    data = db.collection("admin-data").get()
    print(data)
    return render(request, "storage.html", context)


def show_request(request):
    data = db.collection("admin-data").get()
    print(data)

    return render(request, "storage.html")


def requestwater(request):
    email = request.POST.get("email")
    quantity = request.POST.get("qua")
    doc = db.collection("user-registration").document(str(email))
    data = doc.get()
    flatno = int(data.to_dict()["flat"])
    db.collection("user-request").document(str(email)).set(
        {"quantity": int(quantity), "flatno": flatno}
    )
    txn = {
        "hash": "0xd6984f6afb52e82599035f5aab6398204abff47aa80e057df429c9b541684d97",
        "status": "Request Sent",
    }
    doc = (
        db.collection("transactions").document(str(email)).set({"transactions": [txn]})
    )
    return render(request, "invoice.html")


# Create your views here.

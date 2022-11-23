from django.shortcuts import render, HttpResponse, loader

# import pyrebase4
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from django.shortcuts import render, HttpResponse, loader
from transactions.deploy import deploy

import datetime
from datetime import date

# from django.conf import settings
# settings.configure()

def pH_Calc(pH):
    return 10 if pH == 7 else int(10-(abs(pH - 7)/0.5)*2) 

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
    if temp in range(18,35):
        return 10
    elif temp in range(35,45) or temp in range(0,18):
        return 8
    elif temp in range(45,55):
        return 6
    elif temp in range(55,65):
        return 4
    else:
        return 2


credJson = credentials.Certificate("wms/service_key.json")
firebase_admin.initialize_app(credJson)
db = firestore.client()
db.collection("admin-data").document("s3").set({"Date": "23112022", "Quantity": 10})
k = db.collection("admin-data").document("s3").set({"Date": "23112022", "Quantity": 10})
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
    storage = request.POST.get("storage_id")
    print(storage)
    quantity = request.POST.get("quantity")
    today = date.today()
    db.collection("admin-data").document(str(storage)).set(
        {"Date": str(today), "Quantity": quantity}
    )
    return render(request, "admin.html")


def dashboard(request):
    return render(request, "dashboard.html")


def invoice(request):
    return render(request, "invoice.html")


def trial(request):
    return render(request, "trial.html")


def deployContract(request):
    deploy()
    return render(request,"admin.html")



def storage(request):
    # login starts

    context = {}
    # context["temp"]=request.POST.get("storage_id")
    # context["ph"]=request.POST.get("storage_id")
    # context["turbi"]=request.POST.get("storage_id")
    # ph_cal=pH_Calc(context["ph"])
    # turb_cal= turb_Calc(context["turbi"])
    # temp_cal=temp_Calc(context["temp"])
    # if ph_cal < 5 or turb_cal < 5 or temp_cal < 3 :
    #     context["ans"]=10
    # else:
    #     context["ans"] = ((pH_Calc(context["ph"]) + turb_Calc(context["turbi"]) + temp_Calc(context["temp"]))//3)*10
    # print(context["ans"])
    # db.collection('testSensor').document().set(context)
    html_template = loader.get_template( 'storage.html' )
    return HttpResponse(html_template.render(context, request))

def calculate(request):
    context = {}
    print(request.POST.get("temp"))
    print(request.POST.get("turbi"))
    print(request.POST.get("ph"))

    context["temp"]=request.POST.get("temp")
    context["ph"]=request.POST.get("ph")
    context["turbi"]=request.POST.get("turbi")
    ph_cal=pH_Calc(int(context["ph"]))
    turb_cal= turb_Calc(float(context["turbi"]))
    temp_cal=temp_Calc(int(context["temp"]))
    if ph_cal < 5 or turb_cal < 5 or temp_cal < 3 :
        context["ans"]=10
    else:
        context["ans"] = ((pH_Calc(int(context["ph"])) + turb_Calc(float(context["turbi"])) + temp_Calc(int(context["temp"])))//3)*10
    print(context['ans'])
    return render(request,"storage.html",context)



def signup(request):
    message = {}
    name=request.POST.get("name")
    sch_id= request.POST.get("Student_id")
    state=request.POST.get("State")
    city=request.POST.get("City")
    user=request.POST.get("user")
    metamask=request.POST.get('metamask')
    flat=request.POST.get('flat')
  
    email=request.POST.get("email")
    passw = request.POST.get("password")
    print(name,email,passw,city,state,metamask,flat,user)
    # if sch_name != None or sch_id != None or email != None or passw!=None:
    #     data = db.collection('Userdb').get()
    #     email_ids = []
    #     for doc in data:
    #         a= doc.to_dict()
    #         email_ids.append(a["email"])
    #     print(email_ids)
    #     if email not in email_ids:    
    #         db.collection('Userdb').document(email).set({"school_name":sch_name,"school_id":sch_id,"email":email,"Password":passw,"state":state,"city":city})
    #         user=auth.create_user_with_email_and_password(email,passw)
    #         # uid = user['localId']
    #         # idtoken = request.session['uid']
    #         message["messages"] = 1
    #     else:
    #         message["messages"] = 2
    return render(request,"login.html")


# Create your views here.

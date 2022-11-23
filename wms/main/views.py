from django.shortcuts import render,HttpResponse, loader
# from django.conf import settings
# settings.configure()


def index(request):

    context={}
    html_template = loader.get_template( 'landing.html' )


    return HttpResponse(html_template.render(context, request))


def login(request):
    return render(request,'login.html')


def register(request):
    return render(request,'register.html')



def dashboard(request):
    return render(request,"dashboard.html")
# Create your views here.

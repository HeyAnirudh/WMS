from django.shortcuts import render,HttpResponse
# from django.conf import settings
# settings.configure()


def index(request):
    return HttpResponse("heelo bitch")

# Create your views here.

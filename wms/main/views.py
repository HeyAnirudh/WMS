from django.shortcuts import render,HttpResponse
# from django.conf import settings
# settings.configure()


def index(request):
    return HttpResponse("heelo eli")

# Create your views here.

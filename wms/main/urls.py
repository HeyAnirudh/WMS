from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("admin-main/", views.admin, name="admin"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("trial/", views.trial, name="trial"),
    path("deploy/", views.deployContract, name="deploy"),
    path("pushreq/", views.admin, name="adminreq"),
]

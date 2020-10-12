from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.worlddashboard,name="world_dashboard"),
    path('/country',views.countrydashboard,name="country_dashboard")
]

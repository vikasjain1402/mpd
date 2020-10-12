from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.indiadashboard,name="india_dashboard"),
    path('/state',views.indiastatedashboard,name="india_state_dashboard"),
    path('/district',views.indiadistrictdashboard,name="india_district_dashboard"),
    path('/districtdetail',views.indiadistrictdetaildashboard,name="india_district_detail_dashboard")


]

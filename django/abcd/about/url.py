from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.search,name="search"),
    path('/about',views.about,name="about"),
    path('/TermsAndCondition',views.tac,name="TermsAndCondition"),

]

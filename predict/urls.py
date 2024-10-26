
from django.contrib import admin
from django.urls import path, include
from . import views


# Create your views here.


urlpatterns = [
    path('', views.index, name='index'),
]

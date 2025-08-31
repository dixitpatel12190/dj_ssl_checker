"""
URL configuration for django_ssl_checker project.
"""


from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cert/', views.cert, name='cert'),
]

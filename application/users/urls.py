from django.urls import path

from .api import *

urlpatterns = [
    path('login', user_login),
    path('register', user_register)
]

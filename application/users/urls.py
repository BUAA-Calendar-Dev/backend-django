from django.urls import path

from .api import *

urlpatterns = [
    path('login', user_login),
    path('register', user_register),
    path('', get_now_user_info),
    path('<int:id>/info', get_user_info),
    path('modify', update_user)
]

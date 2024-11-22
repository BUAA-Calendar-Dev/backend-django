from django.urls import path

from .api import *

urlpatterns = [
    path('', get_messages),
    path('<int:id>/read', read_message)
]

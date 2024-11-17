from django.urls import path

from .api import *

urlpatterns = [
    path('', get_tasks_related),
    path('create', creat_task)
]

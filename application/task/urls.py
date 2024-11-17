from django.urls import path

from .api import *

urlpatterns = [
    path('', get_tasks_related),
    # TODO：对event进行对接
    path('create', creat_task),
]

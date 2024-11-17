from django.urls import path

from .api import *

urlpatterns = [
    path('public', get_activities_all),
    path('<int:id>/detail', get_activity_detail),
    path('<int:id>/<str:status>', user_inout_activity),
]

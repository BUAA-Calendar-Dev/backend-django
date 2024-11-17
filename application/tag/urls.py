from django.urls import path

from .api import *

urlpatterns = [
    path('', get_tags),
    path('<int:id>/modify', update_tag),
    path('delete/<int:id>',delete_tag),
    path('new',creat_tag)
]

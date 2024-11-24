from django.urls import path

from .api import *

urlpatterns = [
    # 查询个人全路标签
    path('', get_tags),
    # 新建个人标签
    path('new', creat_tag),
    # 删除非固定个人标签
    path('<int:id>/delete', delete_tag),
    # 修改个人标签
    path('<int:id>/modify', modify_tag),
]

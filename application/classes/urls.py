from django.urls import path

from .api import *

urlpatterns = [
    # 创建班级
    path('create', create_class),
    # 批量添加老师
    path('<int:id>/teacher', add_teachers),
    # 批量移除老师
    path('<int:id>/teacher/delete', remove_teachers),
    # 批量添加学生
    path('<int:id>/student', add_students),
    # 批量移除学生
    path('<int:id>/student/delete', remove_students),
    # 查询自己的班级
    path('info', get_class_info_list)
]

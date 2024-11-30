from django.urls import path

from .api import *

urlpatterns = [
    # 创建班级
    path('create', create_class),
    # 批量添加老师
    path('<int:id>/teacher/add', add_teachers),
    # 批量移除老师
    path('<int:id>/teacher/delete', remove_teachers),
    # 批量添加学生
    path('<int:id>/student/add', add_students),
    # 批量移除学生
    path('<int:id>/student/delete', remove_students),
    # 查询自己的班级
    path('info', get_class_info_list),
    # 查询班级信息
    path('<int:id>', get_class_info),
    # 查询班级学生
    path('<int:id>/student', get_students),
    # 查询班级老师
    path('<int:id>/teacher', get_teachers),
    # 查询班级任务
    path('<int:id>/task', get_tasks),
    # 更新班级信息
    path('<int:id>/modify', update_class),
]

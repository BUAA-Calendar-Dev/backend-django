from django.urls import path

from .api import *

urlpatterns = [
    # 查询用户相关的task
    path('', get_related_tasks),
    # 设置任务完成百分比
    path('<int:id>/percentage', set_percentage),
    # 设置任务提醒
    path('<int:id>/alarm', set_alarms),
    # 绑定tag
    path('<int:id>/tag', add_tag),
    # 移除tag
    path('<int:id>/tag/delete', remove_tag),
    # 创建任务
    path('create', creat_task),
    # 修改任务信息
    path('<int:id>/modify', modify_task),
    # 向学生布置任务
    path('<int:id>/user', assign_to_student),
    # 向班级布置任务
    path('<int:id>/class', assign_to_class),
    # 向全校布置任务
    path('<int:id>/school', assign_to_school),
]

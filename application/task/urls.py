from django.urls import path

from .api import *

urlpatterns = [
    # 查询用户相关的task
    path('info', get_related_tasks),
    # 设置任务完成百分比
    path('<int:id>/percentage', set_percentage),
    path('<int:id>/finish', finish_task),
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
    
    # 获取任务数量
    path('count', get_task_count),
    # 各类完成情况：库中的所有任务
    path('completion', get_task_all_completion),
    # 个人的完成情况
    path('self/completion', get_task_stu_completion),
    # 班级的完成情况
    path('class/<int:class_id>/completion', get_class_completion),
    # 近7天的任务完成率
    path('completion/7days', get_task_completion_7days),
]

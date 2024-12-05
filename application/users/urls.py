from django.urls import path

from .api import *

urlpatterns = [
    path('login', user_login),
    path('logout', user_logout),
    path('register', user_register),

    # 批量创建用户
    path('create', create_users),
    # 提权为老师
    path('impower', impower_user),
    # 重置学生密码
    path('<int:id>/reset-password', reset_password),
    # 用户重置密码
    path('reset_password', change_password),

    # 获取当前用户的信息
    path('info', get_current_user_info),
    # 获取id用户的信息
    path('<int:id>/info', get_user_info),
    # 修改当前用户的信息
    path('modify', modify_user_info),
    # 修改头像
    path('avatar', update_avatar),

    # 获取学生列表
    path('students', get_students),
    # 获取教师列表
    path('teachers', get_teachers),
    
    # 获取偏好
    path('preference', get_preference),
    # 修改偏好
    path('preference/update', update_preference),
]

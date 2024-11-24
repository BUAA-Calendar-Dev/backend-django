from django.urls import path

from .api import *

urlpatterns = [
    # 查询信息
    path('', get_messages),
    # 阅读信息
    path('<int:id>/read', read_message),
    # 发送给学生
    path('student/<int:id>', send_to_student),
    # 发送给班级
    path('class/<int:id>', send_to_class),
    # 发送给全校
    path('broadcast', send_to_school)
]

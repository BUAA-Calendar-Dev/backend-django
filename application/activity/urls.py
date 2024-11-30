from django.urls import path

from .api import *

urlpatterns = [
    # 查询公共活动列表
    path('public', get_public_activities),
    # 查询活动详细内容
    path('<int:id>/detail', get_activity_detail),
    # 参退活动
    path('<int:id>/join', user_join_activity),
    path('<int:id>/exit', user_exit_activity),
    # 添加tag
    path('<int:id>/tag', add_tag),
    # 删除tag
    path('<int:id>/tag/delete', remove_tag),
    # 创建公开活动
    path('create', create_activity),
    # 修改活动
    path('<int:id>/modify', modify_activity),
    # 删除活动
    path('<int:id>/delete', delete_activity),

    # 适配event的接口
    # 返回私人创建的活动
    path('e', get_events),
    # 创建私人活动
    path('e/create', create_event)
]

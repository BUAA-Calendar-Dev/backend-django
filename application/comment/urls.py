from django.urls import path
from .api import *

urlpatterns = [
    # 获取评论的回复
    path('<int:id>/replies', get_comment_replies),
    # 发表二级评论
    path('<int:id>/reply', create_reply),
    # 删除以及评论
    path('<int:id>/delete', delete_comment),
]

from django.http import HttpRequest
from django.views.decorators.http import require_GET

from application.activity.models import Activity
from application.activity.models.activity_user_relationship import ActivityUserRelationship
from application.comment.models import Comment
from application.task.models.task import Task
from application.task.models.task_user_relationship import TaskUserRelationship
from application.users.api import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_request
from application.utils.response import *


def _get_comment_info(comment: Comment):
    return {
        "id": comment.id,
        "author": comment.author.name,
        "authorId": comment.author.id,
        "avatar": comment.author.avatar,
        "content": comment.content,
        "time": comment.time.strftime('%Y-%m-%d %H:%M:%S'),
    }


@response_wrapper
@jwt_auth()
@require_GET
def get_comment_replies(request: HttpRequest, id: int):
    """获取指定一级评论下的所有回复"""
    parent_comment = Comment.objects.filter(id=id).first()
    if parent_comment is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "评论不存在或不是一级评论")

    comments = []
    replies = Comment.objects.filter(parent=parent_comment).all()
    for reply in replies:
        comments.append(_get_comment_info(reply))

    print(f"[debug] get replies for comment {id}: {replies}")
    return response({
        "comments": comments
    })

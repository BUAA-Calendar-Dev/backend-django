from django.http import HttpRequest
from django.views.decorators.http import require_GET, require_POST

from application.activity.models import Activity
from application.comment.api.comment_get import _get_comment_info
from application.comment.models import Comment
from application.users.api import jwt_auth
from application.utils.data_process import parse_request
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_GET
def get_comments(request: HttpRequest, id: int):
    activity = Activity.objects.filter(id=id).first()
    if activity is None:
        return response({
            "code": StatusCode.REQUEST_ACTIVITY_ID_NOT_EXIST
        })

    comments = []
    for comment in activity.comments.filter(parent=None).all():
        comments.append(_get_comment_info(comment))
    return response({
        "comments": comments
    })


@response_wrapper
@jwt_auth()
@require_POST
def create_comment(request: HttpRequest, id: int):
    user = request.user
    activity = Activity.objects.filter(id=id).first()
    if activity is None:
        return response({
            "code": StatusCode.REQUEST_ACTIVITY_ID_NOT_EXIST
        })
    request_data = parse_request(request)

    content = request_data.get('content', '')
    comment = Comment(content=content, author=user)
    comment.save()
    
    activity.comments.add(comment)

    return response({
        "message": "成功创建一级评论",
        "comment": _get_comment_info(comment)
    })

from django.http import HttpRequest
from django.views.decorators.http import require_POST

from application.comment.api.comment_get import _get_comment_info
from application.comment.models import Comment
from application.users.api import jwt_auth
from application.utils.data_process import parse_request
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_POST
def create_reply(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)

    parent_comment = Comment.objects.filter(id=id).first()

    content = request_data.get('content', '')
    comment = Comment(content=content, author=user, parent=parent_comment)
    comment.save()

    return response({
        "message": "成功评论活动",
        "comment": _get_comment_info(comment)
    })


@response_wrapper
@jwt_auth()
@require_POST
def delete_comment(request: HttpRequest, id: int):
    user = request.user
    comment = Comment.objects.filter(id=id).first()
    
    if comment.author == user:
      comment.delete()
      return response({
          "message": "成功删除评论"
      })
    return fail_response(ErrorCode.INVALID_REQUEST_ARGS, "不能删除不是自己创建的评论")

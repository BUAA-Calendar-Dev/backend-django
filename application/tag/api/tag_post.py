from datetime import datetime
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from application.tag.models import Tag
from application.task.models import Task
from application.users.api.auth import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_data
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_POST
def creat_tag(request: HttpRequest):
    user = request.user
    post_data = parse_data(request)

    title = post_data.get('title', '新建tag')
    if len(title) > 256:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "tag名过长")
    content = post_data.get('content', '暂时没有内容')
    if len(content) > 1024:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "描述过长")

    tag = Tag(title=title, content=content, create_user=user)
    tag.save()

    return success_response({
        "message": "成功创建tag"
    })


@response_wrapper
@jwt_auth()
@require_POST
def update_tag(request: HttpRequest, id: int):
    user = request.user
    post_data = parse_data(request)

    task = Task.objects.get(id=id)
    if task is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在tag")

    title = post_data.get('title')
    if title:
        if len(title) < 256:
            task.title = title
        else:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "tag名过长")
    content = post_data.get('content')
    if content:
        if len(content) < 1024:
            task.content = content
        else:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "描述过长")

    task.save()
    return success_response({
        "message": "成功修改tag"
    })

from django.http import HttpRequest
from django.views.decorators.http import require_POST

from application.tag.models import Tag
from application.utils.data_process import parse_request
from application.utils.response import *


@response_wrapper
# @jwt_auth()
@require_POST
def creat_tag(request: HttpRequest):
    user = request.user
    request_data = parse_request(request)

    title = request_data.get('title', 'tag-name')
    if len(title) > 256:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "tag名过长")

    content = request_data.get('content', 'tag-content')
    if len(content) > 1024:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "描述过长")

    color = request_data.get('color', '#FFEFDB')

    tag = Tag(title=title, content=content, create_user=user, color=color, fixed=False)
    tag.save()

    return response({
        "message": "成功创建tag",
        "id": tag.id
    })


@response_wrapper
# @jwt_auth()
@require_POST
def modify_tag(request: HttpRequest, id: int):
    request_data = parse_request(request)

    tag = Tag.objects.get(id=id)
    if tag is None or tag.fixed:
        return response({
            "code": StatusCode.REQUEST_TAG_ID_NOT_EXIST
        })

    title = request_data.get('title', '')
    if title:
        if len(title) < 256:
            tag.title = title
        else:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "tag名过长")

    content = request_data.get('content', '')
    if content:
        if len(content) < 1024:
            tag.content = content
        else:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "描述过长")

    color = request_data.get('color', '')
    if color:
        tag.color = color

    tag.save()
    return response({
        "message": "成功修改tag"
    })


@response_wrapper
# @jwt_auth()
@require_POST
def delete_tag(request: HttpRequest, id: int):
    tag = Tag.objects.get(id=id)
    if tag is None:
        return response({
            "code": StatusCode.REQUEST_TAG_ID_NOT_EXIST
        })
    if tag.fixed:
        return response({
            "code": StatusCode.TAG_CANNOT_MODIFY
        })
    tag.delete()
    return response({
        "message": "成功删除tag"
    })

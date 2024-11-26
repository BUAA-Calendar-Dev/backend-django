from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET

from application.tag.models import Tag
from application.task.models import Task, TaskUserRelationship
from application.users.api import jwt_auth
from application.utils.data_process import parse_request
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_POST
def add_tag(request: HttpRequest, id: int):
    request_data = parse_request(request)
    user = request.user

    task = Task.objects.filter(id=id).first()
    if task is None:
        return response({
            "code": StatusCode.REQUEST_TASK_ID_NOT_EXIST
        })
    relationship = TaskUserRelationship.objects.filter(related_user=user, task=task).first()
    if relationship is None:
        return response({
            "code": StatusCode.REQUEST_TASK_ID_NOT_EXIST
        })

    tag_id = request_data.get('tag-id')
    tag = Tag.objects.filter(id=tag_id).first()
    if tag is None:
        return response({
            "code": StatusCode.REQUEST_TAG_ID_NOT_EXIST
        })

    if tag in task.tags.all() or tag in relationship.tags.all():
        relationship.tags.add(tag)
        relationship.save()
    else:
        return response({
            "code": StatusCode.TAG_ALREADY_TIED
        })
    return response({
        "message": "成功为任务绑定tag"
    })


@response_wrapper
@jwt_auth()
@require_POST
def remove_tag(request: HttpRequest, id: int):
    request_data = parse_request(request)
    user = request.user

    task = Task.objects.filter(id=id).first()
    if task is None:
        return response({
            "code": StatusCode.REQUEST_TASK_ID_NOT_EXIST
        })
    relationship = TaskUserRelationship.objects.filter(related_user=user, task=task).first()
    if relationship is None:
        return response({
            "code": StatusCode.REQUEST_TASK_ID_NOT_EXIST
        })

    tag_id = request_data.get('tag-id')
    tag = Tag.objects.filter(id=tag_id).first()
    if tag is None:
        return response({
            "code": StatusCode.REQUEST_TAG_ID_NOT_EXIST
        })

    if tag in task.tags.all():
        return response({
            "code": StatusCode.TAG_CANNOT_MODIFY
        })

    if tag not in relationship.tags.all():
        return response({
            "code": StatusCode.TAG_NOT_TIED
        })

    relationship.tags.remove(tag)
    relationship.save()
    return response({
        "message": "成功为任务绑定tag"
    })

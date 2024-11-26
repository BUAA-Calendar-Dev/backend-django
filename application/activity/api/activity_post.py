from django.http import HttpRequest
from django.views.decorators.http import require_POST
from datetime import datetime

from application.activity.models import Activity
from application.activity.models.activity_user_relationship import ActivityUserRelationship
from application.tag.models import Tag
from application.users.api import jwt_auth
from application.utils.data_process import parse_request
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_POST
def create_activity(request: HttpRequest):
    request_data = parse_request(request)

    title = request_data.get('name')
    content = request_data.get('content')
    time = request_data.get('time')

    activity = Activity(
        is_public=True,
        title=title,
        content=content,
        start_time=datetime.strptime(time, "%Y-%m-%d %H:%M")
    )
    activity.save()

    return response({
        "message": "成功创建活动"
    })


@response_wrapper
@jwt_auth()
@require_POST
def modify_activity(request: HttpRequest, id: int):
    request_data = parse_request(request)
    activity = Activity.objects.filter(id=id).first()
    if activity is None:
        return response({
            "code": StatusCode.REQUEST_ACTIVITY_ID_NOT_EXIST
        })

    title = request_data.get('name', '')
    content = request_data.get('content', '')
    time = request_data.get('time', '')

    if title:
        activity.title = title
    if content:
        activity.content = content
    if time:
        activity.start_time = datetime.strptime(time, "%Y-%m-%d %H:%M")
    activity.save()

    return response({
        "message": "成功修改活动"
    })


@response_wrapper
@jwt_auth()
@require_POST
def delete_activity(request: HttpRequest, id: int):
    activity = Activity.objects.filter(id=id).first()
    if activity is None:
        return response({
            "code": StatusCode.REQUEST_ACTIVITY_ID_NOT_EXIST
        })
    activity.delete()
    return response({
        "message": "成功删除活动"
    })


@response_wrapper
@jwt_auth()
@require_POST
def user_inout_activity(request: HttpRequest, id: int, status: str):
    user = request.user
    activity = Activity.objects.filter(id=id).first()

    if activity is None:
        return response({
            "code": StatusCode.REQUEST_ACTIVITY_ID_NOT_EXIST
        })

    exists = ActivityUserRelationship.objects.filter(task=activity, related_user=user).exists()
    if status == "join":
        if exists:
            return response({
                "code": StatusCode.PARTICIPATE_IN_ACTIVITY_AGAIN
            })
        relationship = ActivityUserRelationship(
            task=activity,
            related_user=user,
            permission=1,
            name=activity.title
        )
        relationship.save()
    elif status == "exit":
        if not exists:
            return response({
                "code": StatusCode.EXIT_ACTIVITY_NOT_IN
            })
        relationship = ActivityUserRelationship.objects.filter(task=activity, related_user=user).first()
        relationship.delete()
    else:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "无效的状态")
    return response({
        "message": f"成功改变用户的{status}"
    })


@response_wrapper
@jwt_auth()
@require_POST
def add_tag(request: HttpRequest, id: int):
    request_data = parse_request(request)

    user = request.user
    activity = Activity.objects.filter(id=id).first()
    if activity is None:
        return response({
            "code": StatusCode.REQUEST_ACTIVITY_ID_NOT_EXIST
        })
    relationship = ActivityUserRelationship.objects.filter(task=activity, related_user=user).first()

    tag_id = request_data.get('tag-id')
    tag = Tag.objects.filter(id=tag_id).first()

    relationship.tags.add(tag)
    relationship.save()

    return response({
        "message": "成功添加tag"
    })


@response_wrapper
@jwt_auth()
@require_POST
def remove_tag(request: HttpRequest, id: int):
    request_data = parse_request(request)

    user = request.user
    activity = Activity.objects.filter(id=id).first()
    if activity is None:
        return response({
            "code": StatusCode.REQUEST_ACTIVITY_ID_NOT_EXIST
        })
    relationship = ActivityUserRelationship.objects.filter(task=activity, related_user=user).first()

    tag_id = request_data.get('tag-id')
    tag = Tag.objects.filter(id=tag_id).first()

    relationship.tags.remove(tag)
    relationship.save()

    return response({
        "message": "成功移除tag"
    })


@response_wrapper
@jwt_auth()
@require_POST
def create_event(request: HttpRequest):
    request_data = parse_request(request)

    title = request_data.get('name')
    content = request_data.get('content')
    time = request_data.get('start')
    end = request_data.get('end')

    activity = Activity(
        is_public=False,
        title=title,
        content=content,
        start_time=datetime.strptime(time, "%Y-%m-%d %H:%M"),
        end_time=datetime.strptime(end, "%Y-%m-%d %H:%M")
    )
    activity.save()

    return response({
        "message": "成功创建活动",
    })

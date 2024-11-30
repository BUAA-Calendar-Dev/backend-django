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
    start_time = request_data.get('start')
    end_time = request_data.get('end')

    activity = Activity(
        is_public=True,
        title=title,
        content=content,
        start_time=datetime.strptime(start_time, "%Y-%m-%d %H:%M"),
        end_time=datetime.strptime(end_time, "%Y-%m-%d %H:%M")
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
    start_time = request_data.get('start', '')
    end_time = request_data.get('end', '')

    if title:
        activity.title = title
    if content:
        activity.content = content
    if start_time:
        activity.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    if end_time:
        activity.end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
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
def user_join_activity(request: HttpRequest, id: int):
    user = request.user
    activity = Activity.objects.filter(id=id).first()

    if activity is None:
        return response({
            "code": StatusCode.REQUEST_ACTIVITY_ID_NOT_EXIST
        })

    relationship_exits = ActivityUserRelationship.objects.filter(activity=activity, related_user=user).exists()
    if relationship_exits:
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

    return response({
        "message": f"成功参加活动"
    })


@response_wrapper
@jwt_auth()
@require_POST
def user_exit_activity(request: HttpRequest, id: int):
    user = request.user
    activity = Activity.objects.filter(id=id).first()

    if activity is None:
        return response({
            "code": StatusCode.REQUEST_ACTIVITY_ID_NOT_EXIST
        })

    relationship_exists = ActivityUserRelationship.objects.filter(activity=activity, related_user=user).exists()
    if not relationship_exists:
        return response({
            "code": StatusCode.EXIT_ACTIVITY_NOT_IN
        })
    relationship = ActivityUserRelationship.objects.filter(activity=activity, related_user=user).first()
    relationship.delete()
    
    return response({
        "message": f"成功退出活动"
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
    relationship = ActivityUserRelationship.objects.filter(activity=activity, related_user=user).first()

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
    relationship = ActivityUserRelationship.objects.filter(activity=activity, related_user=user).first()

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
    user = request.user
    request_data = parse_request(request)

    title = request_data.get('name')
    content = request_data.get('content')
    start_time = request_data.get('start')
    end_time = request_data.get('end')

    activity = Activity(
        is_public=False,
        title=title,
        content=content,
        start_time=datetime.strptime(start_time, "%Y-%m-%d %H:%M"),
        end_time=datetime.strptime(end_time, "%Y-%m-%d %H:%M")
    )
    activity.save()

    relationship = ActivityUserRelationship(activity=activity, related_user=user, name=activity.title, permission=0)
    relationship.save()

    return response({
        "message": "成功创建活动",
    })

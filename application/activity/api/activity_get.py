from django.http import HttpRequest
from django.views.decorators.http import require_GET

from application.activity.models import Activity
from application.activity.models.activity_user_relationship import ActivityUserRelationship
from application.users.api import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_request
from application.utils.response import *


def _check_user_in_activity(user: User, activity: Activity):
    relationship = ActivityUserRelationship.objects.filter(related_user=user, task=activity).first()
    return relationship is not None


def _get_activity_detail(activity: Activity):
    return {
        "id": activity.id,
        "name": activity.title,
        "content": activity.content,
        "place": activity.place,
        "time": activity.start_time,
    }


def _get_activity_tag_list(activity: Activity, user: User):
    tag_list = set()
    relationship = ActivityUserRelationship.objects.filter(related_user=user, task=activity).first()

    # 添加活动的标签
    tag_list.update(activity.tags.all())
    # 如果存在关系，添加关系的标签
    if relationship:
        tag_list.update(relationship.tags.all())
    # 将集合转换为列表返回
    return [tag.id for tag in list(tag_list)]


@response_wrapper
@jwt_auth()
@require_GET
def get_public_activities(request: HttpRequest):
    user = request.user
    activity_list = Activity.objects.filter(is_public=True)

    activity_info_list = []
    for activity in activity_list:
        activity_info_list.append({
            "id": activity.id,
            "name": activity.title,
            "time": activity.start_time,
            # tag是活动自带tag和用户自定义tag的和
            "tags": _get_activity_tag_list(activity, user),
            "signed-in": _check_user_in_activity(user, activity)
        })
    return response({
        "activities": activity_info_list
    })


@response_wrapper
@jwt_auth()
@require_GET
def get_activity_detail(request: HttpRequest, id: int):
    activity = Activity.objects.filter(id=id).first()
    if activity is None:
        return response({
            "code": StatusCode.REQUEST_ACTIVITY_ID_NOT_EXIST
        })
    return response({
        "content": _get_activity_detail(activity)
    })


@response_wrapper
@jwt_auth()
@require_GET
def get_events(request: HttpRequest):
    user = request.user
    activity_list = Activity.objects.filter(is_public=True)

    activity_info_list = []
    for activity in activity_list:
        activity_info_list.append({
            "id": activity.id,
            "name": activity.title,
            "time": activity.start_time,
            # tag是活动自带tag和用户自定义tag的和
            "tags": _get_activity_tag_list(activity, user),
            "signed-in": _check_user_in_activity(user, activity)
        })
    return response({
        "events": activity_info_list,
        "specialHours": []
    })

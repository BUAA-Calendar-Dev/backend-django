from django.http import HttpRequest
from django.views.decorators.http import require_GET

from application.activity.models import Activity
from application.activity.models.activity_user_relationship import ActivityUserRelationship
from application.task.models.task import Task
from application.task.models.task_user_relationship import TaskUserRelationship
from application.users.api import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_request
from application.utils.response import *


def _check_user_in_activity(user: User, relationship: ActivityUserRelationship):
    return relationship is not None


def _get_activity_detail(activity: Activity):
    return {
        "id": activity.id,
        "title": activity.title,
        "content": activity.content,
        "start": activity.start_time.strftime('%Y-%m-%d %H:%M'),
        "end": activity.end_time.strftime('%Y-%m-%d %H:%M'),
        "place": activity.place
    }


def _get_special_hours(relationship: TaskUserRelationship):
    start_date = relationship.task.start_time.date()
    start_hour = relationship.task.start_time.hour
    end_hour = relationship.task.end_time.hour
  
    return {
        "id": relationship.task.id,
        "class": relationship.name,
        "label": relationship.task.content,
        "from": relationship.task.start_time.strftime('%Y-%m-%d %H:%M'),
        "to": relationship.task.end_time.strftime('%Y-%m-%d %H:%M'),
        "title": relationship.task.title,
        "content": relationship.task.content,
        "start": relationship.task.start_time.strftime('%Y-%m-%d %H:%M'),
        "end": relationship.task.end_time.strftime('%Y-%m-%d %H:%M'),
        
        "completed": relationship.percentage == 100,
        
        "day": start_date.weekday(),
        "hours": [start_hour, end_hour],
        "style": {
            "backgroundColor": "#FFC0CB",  # 粉红色背景，可以根据需要自定义
            "opacity": 0.5  # 透明度
        },
    }

def _get_activity_user_detail(relationship: ActivityUserRelationship, user: User):
    return {
        "id": relationship.activity.id,
        "title": relationship.name,
        "content": relationship.activity.content,
        "start": relationship.activity.start_time.strftime('%Y-%m-%d %H:%M'),
        "end": relationship.activity.end_time.strftime('%Y-%m-%d %H:%M'),
        "place": relationship.activity.place,
        # tag是活动自带tag和用户自定义tag的和
        "tags": _get_activity_tag_list(relationship.activity, user),
        "signed-in": relationship is not None
    }


def _get_activity_tag_list(activity: Activity, user: User):
    tag_list = set()
    relationship = ActivityUserRelationship.objects.filter(related_user=user, activity=activity).first()

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
            "start": activity.start_time.strftime('%Y-%m-%d %H:%M'),
            "end": activity.end_time.strftime('%Y-%m-%d %H:%M'),
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
    activity_info_list = []
    task_info_list = []

    # activity_list = Activity.objects.filter(is_public=True)
    # for activity in activity_list:
    #     activity_info_list.append(_get_activity_user_detail(activity, user))

    activity_relationships = ActivityUserRelationship.objects.filter(related_user=user)
    for relationship in activity_relationships:
        activity_info_list.append(_get_activity_user_detail(relationship, user))
        
    task_relationships = TaskUserRelationship.objects.filter(related_user=user)
    for relationship in task_relationships:
        task_info_list.append(_get_special_hours(relationship))
        
    print(f"[debug] activity_info_list is {activity_info_list}")
    print(f"[debug] task_info_list is {task_info_list}")

    return response({
        "events": activity_info_list,
        "specialHours": task_info_list
    })

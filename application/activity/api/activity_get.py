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


def _check_user_in_activity(user: User, activity: Activity):
    return ActivityUserRelationship.objects.filter(related_user=user, activity=activity).exists()


def _get_activity_detail(activity: Activity):
    return {
        "id": activity.id,
        "title": activity.title,
        "content": activity.content,
        "start": activity.start_time.strftime('%Y-%m-%d %H:%M'),
        "end": activity.end_time.strftime('%Y-%m-%d %H:%M'),
        "place": activity.place
    }


def _get_task_tag_list(relationship: TaskUserRelationship):
    return [tag.id for tag in relationship.task.tags.all()] + [tag.id for tag in relationship.tags.all()]


def _get_task_event(relationship: TaskUserRelationship):
    return {
        "id": relationship.task.id,
        "title": relationship.name,
        "content": relationship.task.content,
        "start": relationship.task.start_time.strftime('%Y-%m-%d %H:%M'),
        "end": relationship.task.end_time.strftime('%Y-%m-%d %H:%M'),
        "completed": relationship.percentage == 100,
        "is_task": True,
        "tags": _get_task_tag_list(relationship),
        "color": relationship.color if relationship.color != "" else relationship.related_user.preference["taskColor"]
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
        "signed-in": relationship is not None,
        "is_task": False,
        "color": relationship.color if relationship.color != "" else user.preference["activityColor"]
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
            "content": activity.content,
            "start": activity.start_time.strftime('%Y-%m-%d %H:%M'),
            "end": activity.end_time.strftime('%Y-%m-%d %H:%M'),
            # tag是活动自带tag和用户自定义tag的和
            "tags": _get_activity_tag_list(activity, user),
            "signed_in": _check_user_in_activity(user, activity)
        })
    activity_info_list.sort(key=lambda x: x["start"], reverse=True)
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
        task_info_list.append(_get_task_event(relationship))

    # print(f"[debug] activity_info_list is {activity_info_list}")
    # print(f"[debug] task_info_list is {task_info_list}")

    return response({
        "events": activity_info_list + task_info_list
    })


@response_wrapper
@jwt_auth()
@require_GET
def get_activity_join_info(request: HttpRequest):
    activity_set = set()
    num_dict = {}
    activity_relationships = ActivityUserRelationship.objects.all()
    for relationship in activity_relationships:
        activity_set.add(relationship.activity.title)
        num_dict[relationship.activity.title] = num_dict.get(relationship.activity.title, 0) + 1

    activities = []
    join_nun = []
    for activity in activity_set:
        activities.append(activity)
        join_nun.append(num_dict[activity])

    return response({
        "activity": activities,
        "join": join_nun
    })

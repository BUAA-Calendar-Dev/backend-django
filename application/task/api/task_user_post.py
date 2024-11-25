from django.http import HttpRequest
from django.utils import timezone
from django.views.decorators.http import require_POST
from datetime import datetime

from application.tag.models import Tag
from application.task.models import Task, TaskUserRelationship
from application.task.models.alarm import Alarm
from application.utils.data_process import parse_request
from application.utils.response import *


@response_wrapper
# @jwt_auth()
@require_POST
def creat_task(request: HttpRequest):
    # 创建一个task，同时注册相关关系
    user = request.user
    request_data = parse_request(request)

    title = request_data.get('title', '新建任务')
    if len(title) > 256:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "标题过长")

    content = request_data.get('content', '暂无任务描述')
    if len(content) > 1024:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "内容过长")

    start_time = request_data.get('start', None)
    end_time = request_data.get('end', None)
    # TODO：目前设置如果没有DDL，则结束和创建时间相等
    start_time = timezone.now() if start_time is None else start_time
    end_time = start_time if end_time is None else end_time

    parent_task_id = request_data.get('parent_task_id', None)

    task = Task(title=title,
                content=content,
                start_time=start_time,
                end_time=end_time)
    if parent_task_id is not None:
        task.parent_task = Task.objects.get(parent_task_id)
    task.save()

    relationship = TaskUserRelationship(
        task=task,
        name=task.title,
        percentage=0,
        permission=0,
        related_user=user
    )
    relationship.save()

    return response({
        "message": "成功创建任务"
    })


@response_wrapper
# @jwt_auth()
@require_POST
def set_percentage(request: HttpRequest, id: int):
    request_data = parse_request(request)
    user = request.user

    task = Task.objects.get(id=id)
    if task is None:
        return response({
            "code": StatusCode.REQUEST_TASK_ID_NOT_EXIST
        })

    relationship = TaskUserRelationship.objects.filter(related_user=user, task=task).first()
    if relationship is None:
        return response({
            "code": StatusCode.REQUEST_TASK_ID_NOT_EXIST
        })

    percentage = request_data.get('percentage')
    relationship.percentage = percentage
    relationship.save()

    return response({
        "message": "成功修改完成度"
    })


@response_wrapper
# @jwt_auth()
@require_POST
def set_alarms(request: HttpRequest, id: int):
    request_data = parse_request(request)
    user = request.user

    task = Task.objects.get(id=id)
    if task is None:
        return response({
            "code": StatusCode.REQUEST_TASK_ID_NOT_EXIST
        })

    relationship = TaskUserRelationship.objects.filter(related_user=user, task=task)
    if relationship is None:
        return response({
            "code": StatusCode.REQUEST_TASK_ID_NOT_EXIST
        })

    alarms: list[int] = request_data.get('alamrs')
    for value in alarms:
        alarm = Alarm(value=value)
        alarm.save()
        relationship.alarms.add(alarm)
    relationship.save()

    return response({
        "message": "成功设置任务提醒"
    })


@response_wrapper
# @jwt_auth()
@require_POST
def modify_task(request: HttpRequest, id: int):
    request_data = parse_request(request)
    user = request.user

    task = Task.objects.get(id=id)
    if task is None:
        return response({
            "code": StatusCode.REQUEST_TASK_ID_NOT_EXIST
        })

    title = request_data.get('title', '')
    time = request_data.get('time', '')
    content = request_data.get('content', '')
    tags = request_data.get('tags', [])

    if title:
        task.title = title
    if time:
        task.start_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    if content:
        task.content = content
    if tags:
        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            if tag:
                task.tags.add(tag)
    task.save()

    return response({
        "message": "成功修任务信息"
    })

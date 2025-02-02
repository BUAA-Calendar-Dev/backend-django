from django.http import HttpRequest
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime

from application.classes.models import Class
from application.tag.models import Tag
from application.task.models import Task, TaskUserRelationship
from application.users.api import jwt_auth
from application.users.models import User
from application.users.models.user_value import AUTH_STUDENT
from application.utils.data_process import parse_request
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_POST
def assign_to_student(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)

    student = User.objects.filter(id=id).first()
    if student is None:
        return response({
            "code": StatusCode.REQUEST_USER_ID_NOT_EXIST
        })

    title = request_data.get('title', '')
    start_time = request_data.get('start', '')
    end_time = request_data.get('end', '')
    content = request_data.get('content', '')
    tags = request_data.get('tags', [])

    task = Task(
        title=title,
        start_time=timezone.make_aware(datetime.strptime(start_time, "%Y-%m-%d %H:%M")),
        end_time=timezone.make_aware(datetime.strptime(end_time, "%Y-%m-%d %H:%M")),
        content=content
    )
    if tags:
        for tag_id in tags:
            tag = Tag.objects.filter(id=tag_id).first()
            if tag is not None:
                task.tags.add(tag)
    task.save()

    TaskUserRelationship(task=task, related_user =user, name=task.title, permission=0).save()

    relationship = TaskUserRelationship(task=task, related_user=student, name=task.title, permission=1)
    relationship.save()

    return response({
        "message": "成功向学生布置任务"
    })


@response_wrapper
@jwt_auth()
@require_POST
def assign_to_class(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)

    _class = Class.objects.filter(id=id).first()
    if _class is None:
        return response({
            "code": StatusCode.REQUEST_USER_ID_NOT_EXIST
        })

    title = request_data.get('title', '')
    start_time = request_data.get('start', '')
    end_time = request_data.get('end', '')
    content = request_data.get('content', '')
    tags = request_data.get('tags', [])

    task = Task(
        title=title,
        start_time=timezone.make_aware(datetime.strptime(start_time, "%Y-%m-%d %H:%M")),
        end_time=timezone.make_aware(datetime.strptime(end_time, "%Y-%m-%d %H:%M")),
        content=content
    )
    if tags:
        for tag_id in tags:
            tag = Tag.objects.filter(id=tag_id).first()
            if tag is not None:
                task.tags.add(tag)
    task.save()

    TaskUserRelationship(task=task, related_user =user, name=task.title, permission=0).save()

    _class.tasks.add(task)
    _class.save()
    for student in _class.students.all():
        relationship = TaskUserRelationship(task=task, related_user=student, name=task.title, permission=1)
        relationship.save()
        print(f"[debug] class-task assign to {student.username}")
    return response({
        "message": "成功向班级布置任务"
    })


@response_wrapper
@jwt_auth()
@require_POST
def assign_to_school(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)

    title = request_data.get('title', '')
    start_time = request_data.get('start', '')
    end_time = request_data.get('end', '')
    content = request_data.get('content', '')
    tags = request_data.get('tags', [])

    task = Task(
        title=title,
        start_time=timezone.make_aware(datetime.strptime(start_time, "%Y-%m-%d %H:%M")),
        end_time=timezone.make_aware(datetime.strptime(end_time, "%Y-%m-%d %H:%M")),
        content=content
    )
    if tags:
        for tag_id in tags:
            tag = Tag.objects.filter(id=tag_id).first()
            if tag is not None:
                task.tags.add(tag)
    task.save()

    TaskUserRelationship(task=task, related_user =user, name=task.title, permission=0).save()

    for student in User.objects.filter(identity=AUTH_STUDENT):
        if not TaskUserRelationship.objects.filter(task=task, related_user=student).exists():
            relationship = TaskUserRelationship(
                task=task,
                related_user=student,
                name=task.title,
                permission=1
            )
            relationship.save()
    return response({
        "message": "成功向全校布置任务"
    })

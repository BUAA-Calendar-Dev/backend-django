from datetime import timedelta
from django.http import HttpRequest
from django.views.decorators.http import require_GET
from django.utils import timezone
import pytz

from application.classes.models import Class
from application.task.models.task_user_relationship import TaskUserRelationship
from application.users.api import jwt_auth
from application.users.models import User
from application.users.models.user_value import *
from application.utils.data_process import parse_request
from application.utils.response import *
from application.task.models import Task


@response_wrapper
@jwt_auth()
@require_GET
def get_task_count(request: HttpRequest):
    user = request.user

    count = 0
    finished = 0
    relations = TaskUserRelationship.objects.all()
    for relation in relations:
        if relation.percentage == 100:
            finished += 1
        count += 1

    return response({
        "total": count,
        "done": finished
    })


def _get_student_completion_info(user: User, task: Task):
    relation = TaskUserRelationship.objects.filter(related_user=user, task=task).first()
    finished_count, in_progress_count, overdue_count, not_started_count = 0, 0, 0, 0

    # 获取中国时区
    china_tz = pytz.timezone('Asia/Shanghai')
    now = timezone.localtime(timezone.now(), china_tz) + timedelta(hours=8)

    if relation.percentage == 100:
        finished_count += 1
        return (finished_count, in_progress_count, overdue_count, not_started_count)

    start_diff = task.start_time - now
    end_diff = task.end_time - now
    # 均已经结束
    if start_diff <= timedelta(0) and end_diff <= timedelta(0):
        overdue_count += 1
    elif start_diff <= timedelta(0) and end_diff > timedelta(0):
        in_progress_count += 1
    else:
        not_started_count += 1
    return (finished_count, in_progress_count, overdue_count, not_started_count)


@response_wrapper
@jwt_auth()
@require_GET
def get_task_all_completion(request: HttpRequest):
    finished_count, in_progress_count, overdue_count, not_started_count = 0, 0, 0, 0
    relations = TaskUserRelationship.objects.all()
    for relation in relations:
        task = relation.task
        user = relation.related_user
        if user.identity != AUTH_STUDENT:
            continue

        stu_finished_count, stu_in_progress_count, stu_overdue_count, stu_not_started_count = _get_student_completion_info(
            user, task)
        finished_count += stu_finished_count
        in_progress_count += stu_in_progress_count
        overdue_count += stu_overdue_count
        not_started_count += stu_not_started_count
    return response({
        "completionRate": [finished_count, in_progress_count, overdue_count, not_started_count]
    })


@response_wrapper
@jwt_auth()
@require_GET
def get_task_stu_completion(request: HttpRequest):
    user = request.user
    finished_count, in_progress_count, overdue_count, not_started_count = 0, 0, 0, 0

    relations = TaskUserRelationship.objects.filter(related_user=user)
    for relation in relations:
        task = relation.task
        stu_finished_count, stu_in_progress_count, stu_overdue_count, stu_not_started_count = _get_student_completion_info(
            user, task)
        finished_count += stu_finished_count
        in_progress_count += stu_in_progress_count
        overdue_count += stu_overdue_count
        not_started_count += stu_not_started_count

    return response({
        "completionRate": [finished_count, in_progress_count, overdue_count, not_started_count]
    })


@response_wrapper
@jwt_auth()
@require_GET
def get_class_completion(request: HttpRequest, class_id: int):
    user = request.user
    _class = Class.objects.filter(id=class_id).first()

    finished_count, in_progress_count, overdue_count, not_started_count = 0, 0, 0, 0
    
    for task in _class.tasks.all():
        for student in _class.students.all():
            stu_finished_count, stu_in_progress_count, stu_overdue_count, stu_not_started_count = _get_student_completion_info(
                student, task)
            finished_count += stu_finished_count
            in_progress_count += stu_in_progress_count
            overdue_count += stu_overdue_count
            not_started_count += stu_not_started_count
    return response({
        "completionRate": [finished_count, in_progress_count, overdue_count, not_started_count]
    })


@response_wrapper
@jwt_auth()
@require_GET
def get_task_completion_7days(request: HttpRequest):
    user = request.user

    # 获取中国时区
    china_tz = pytz.timezone('Asia/Shanghai')
    now = timezone.localtime(timezone.now(), china_tz) + timedelta(hours=8)

    day_6, day_5, day_4, day_3, day_2, day_1, day_0 = 0, 0, 0, 0, 0, 0, 0

    relations = TaskUserRelationship.objects.all()
    for relation in relations:
        user = relation.related_user
        if user.identity != AUTH_STUDENT:
            continue

        finish_time = relation.finish_time
        if finish_time is None:
            continue

        finish_time = finish_time.date()
        if finish_time == now.date() - timedelta(days=6):
            day_6 += 1
        elif finish_time == now.date() - timedelta(days=5):
            day_5 += 1
        elif finish_time == now.date() - timedelta(days=4):
            day_4 += 1
        elif finish_time == now.date() - timedelta(days=3):
            day_3 += 1
        elif finish_time == now.date() - timedelta(days=2):
            day_2 += 1
        elif finish_time == now.date() - timedelta(days=1):
            day_1 += 1
        else:
            day_0 += 1

    return response({
        "completionRate": [day_6, day_5, day_4, day_3, day_2, day_1, day_0]
    })

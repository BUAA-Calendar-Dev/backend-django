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
    relations = TaskUserRelationship.objects.filter(user=user)
    for relation in relations:
        if relation.percentage == 100:
            finished += 1
        count += 1

    return response({
        "task": count,
        "done": finished
    })


def _get_student_completion_info(user: User, task: Task):
    relation = TaskUserRelationship.objects.filter(user=user, task=task).first()
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

    relations = TaskUserRelationship.objects.filter(user=user)
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
    classes = Class.objects.filter(id=class_id).first()

    finished_count, in_progress_count, overdue_count, not_started_count = 0, 0, 0, 0
    for _class in classes:
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
    # 获取7天前的时间
    seven_days_ago = now - timedelta(days=7)

    finished_count, in_progress_count, overdue_count, not_started_count = 0, 0, 0, 0

    relations = TaskUserRelationship.objects.all()
    for relation in relations:
        task = relation.task
        # 检查任务是否在最近7天内
        if task.start_time < seven_days_ago:
            continue
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

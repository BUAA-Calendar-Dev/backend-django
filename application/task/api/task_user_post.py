from datetime import datetime
from django.http import HttpRequest
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from application.tag.models import Tag
from application.task.models import Task, TaskUserRelationship
from application.users.api.auth import jwt_auth
from application.users.models import User
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
    start_time = timezone.now() if start_time is None else start_time
    end_time = start_time if end_time is None else end_time

    parent_task_id = request_data.get('parent_task_id', None)

    task = Task(title=title,
                content=content,
                start_time=start_time,
                end_time=end_time)
    # TODO：目前设置如果没有DDL，则结束和创建时间相等
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
def update_task(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)
    task = Task.objects.get(id=id)
    if task is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "任务不存在")

    # TODO：更细粒度权限检查
    if task.create_user != user:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "无权限修改")

    title = request_data.get('title')
    content = request_data.get('content')
    end_time = request_data.get('end_time')

    if title:
        if len(title) < 256:
            task.title = title
        else:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "标题过长")

    if content:
        if len(content) < 1024:
            task.content = content
        else:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "内容过长")

    # 认为传入的是XXXX-YY-ZZ的形式
    if end_time:
        try:
            # 尝试将字符串解析为 datetime 对象
            end_time = datetime.strptime(end_time, '%Y-%m-%d')
        except ValueError:
            # 如果解析失败，抛出 ValidationError
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR,
                                 "时间格式不正确，应为 YYYY-MM-DD")

            # 检查 end_time 是否在 start_time 之后
        if end_time < task.start_time:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR,
                                 "结束时间必须在开始时间之后")
    task.save()

    return response({
        "message": "成功修改任务"
    })


@response_wrapper
# @jwt_auth()
@require_POST
def add_related_user(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)
    task = Task.objects.get(id=id)

    if task is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "任务不存在")
    # TODO：可以确定更好的索引方式，id或姓名
    # 目前采用了一个id的dict
    user_id = request_data.get('user_id')
    related_user = User.objects.get(user_id)
    if related_user is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, f"不存在{user_id}的用户")
    task.related_users.add(user)
    task.save()

    return response({
        "message": "成功添加相关用户"
    })


@response_wrapper
# @jwt_auth()
@require_POST
def add_related_users(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)
    task = Task.objects.get(id=id)

    if task is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "任务不存在")
    # TODO：可以确定更好的索引方式，id或姓名
    # 目前采用了一个id的dict
    user_id_list = request_data.get('user_id_list')
    for user_id in user_id_list:
        related_user = User.objects.get(user_id)
        if related_user is None:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, f"不存在{user_id}的用户")
        task.related_users.add(user)
    task.save()

    return response({
        "message": "成功添加所有相关用户"
    })


@response_wrapper
# @jwt_auth()
@require_POST
def add_tag(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)
    task = Task.objects.get(id=id)

    if task is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "任务不存在")

    tag_id = request_data.get('tag_id')
    tag = Tag.objects.get(tag_id)
    if tag is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, f"不存在{tag_id}的tag")
    task.tags.add(tag)
    task.save()

    return response({
        "message": "成功为当前task添加tag"
    })


@response_wrapper
# @jwt_auth()
@require_POST
def add_tags(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)
    task = Task.objects.get(id=id)

    if task is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "任务不存在")

    tag_id_list = request_data.get('tag_id_list')
    for tag_id in tag_id_list:
        tag = Tag.objects.get(tag_id)
        if tag is None:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, f"不存在{tag_id}的tag")
        task.tags.add(tag)
    task.save()

    return response({
        "message": "成功为当前task添加所有tag"
    })

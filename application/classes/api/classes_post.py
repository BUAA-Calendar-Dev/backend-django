from datetime import datetime
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from application.classes.models import Class
from application.tag.models import Tag
from application.task.models import Task
from application.users.api.auth import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_data
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_POST
def create_class(request: HttpRequest):
    user = request.user
    post_data = parse_data(request)

    # TODO：创建班级是否要做权限区分，还是由前端入口控制？
    title = post_data.get('title', '新建班级')
    if len(title) > 256:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "班级标题过长")

    introduction = post_data.get('introduction', '暂无描述')
    if len(introduction) > 256:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "班级描述过长")

    class_ = Class(title=title, introduction=introduction)
    class_.save()

    return success_response({
        "message": "成功创建班级"
    })


@response_wrapper
@jwt_auth()
@require_POST
def update_class(request: HttpRequest, id: int):
    user = request.user
    post_data = parse_data(request)
    class_ = Class.objects.get(id=id)

    if class_ is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该班级")

    title = post_data.get('title')
    if title:
        if len(title) < 256:
            class_.title = title
        else:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "班级标题过长")

    introduction = post_data.get('introduction')
    if introduction:
        if len(introduction) < 1024:
            class_.introduction = introduction
        else:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "班级描述过长")

    class_.save()
    return success_response({
        "message": "信息"
    })


@response_wrapper
@jwt_auth()
@require_POST
def add_student(request: HttpRequest, id: int):
    user = request.user
    post_data = parse_data(request)
    class_ = Class.objects.get(id=id)

    if class_ is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该班级")

    student_id = post_data.get('student_id')
    student = User.objects.get(id=id)
    if student is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, f"不存在{id}的学生")
    class_.students.add(student)
    class_.save()
    return success_response({
        "message": "成功添加学生"
    })


@response_wrapper
@jwt_auth()
@require_POST
def add_students(request: HttpRequest, id: int):
    user = request.user
    post_data = parse_data(request)
    class_ = Class.objects.get(id=id)

    if class_ is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该班级")

    students_id = post_data.get('students_id')

    for student_id in students_id:
        student = User.objects.get(id=student_id)
        if student is None:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, f"不存在{id}的学生")
        class_.students.add(student)
    class_.save()
    return success_response({
        "message": "成功添加学生"
    })


@response_wrapper
@jwt_auth()
@require_POST
def add_teacher(request: HttpRequest, id: int):
    user = request.user
    post_data = parse_data(request)
    class_ = Class.objects.get(id=id)

    if class_ is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该班级")

    teacher_id = post_data.get('teacher_id')
    teacher = User.objects.get(id=teacher_id)
    if teacher is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, f"不存在{id}的老师")
    class_.teachers.add(teacher)
    class_.save()
    return success_response({
        "message": "成功添加学生"
    })


@response_wrapper
@jwt_auth()
@require_POST
def add_teachers(request: HttpRequest, id: int):
    user = request.user
    post_data = parse_data(request)
    class_ = Class.objects.get(id=id)

    if class_ is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该班级")

    teachers_id = post_data.get('teachers_id')

    for teacher_id in teachers_id:
        teacher = User.objects.get(id=teacher_id)
        if teacher is None:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, f"不存在{id}的老师")
        class_.teachers.add(teacher)
    class_.save()
    return success_response({
        "message": "成功添加学生"
    })

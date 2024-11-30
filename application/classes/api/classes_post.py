from django.http import HttpRequest
from django.views.decorators.http import require_POST

from application.classes.models import Class
from application.users.api import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_request
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_POST
def create_class(request: HttpRequest):
    request_data = parse_request(request)

    # TODO：创建班级是否要做权限区分，还是由前端入口控制？
    title = request_data.get('name', '新建班级')
    if len(title) > 256:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "班级标题过长")

    introduction = request_data.get('introduction', '暂无描述')
    if len(introduction) > 256:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "班级描述过长")

    new_class = Class(title=title, introduction=introduction)
    new_class.save()

    return response({
        "message": "成功创建班级"
    })


@response_wrapper
@jwt_auth()
@require_POST
def update_class(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)
    _class = Class.objects.filter(id=id).first()

    if _class is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该班级")

    title = request_data.get('title')
    if title:
        if len(title) < 256:
            _class.title = title
        else:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "班级标题过长")

    introduction = request_data.get('introduction')
    if introduction:
        if len(introduction) < 1024:
            _class.introduction = introduction
        else:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "班级描述过长")

    _class.save()
    return response({
        "message": "成功修改班级信息"
    })


def _add_student(_class: Class, id: int):
    student = User.objects.filter(id=id).first()
    if student is None:
        return StatusCode.REQUEST_USER_ID_NOT_EXIST
    elif student is not None and student in _class.students.all():
        return StatusCode.STUDENT_ALREADY_IN_CLASS
    _class.students.add(student)
    _class.save()
    return StatusCode.SUCCESS


@response_wrapper
@jwt_auth()
@require_POST
def add_students(request: HttpRequest, id: int):
    request_data = parse_request(request)
    _class = Class.objects.filter(id=id).first()

    if _class is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该班级")

    student_id_list = request_data.get('students')

    status_list = []
    for student_id in student_id_list:
        status = _add_student(_class, student_id)
        status_list.append({"code": status})
    return response({
        "message": "成功批量添加学生",
        "status": status_list
    })


def _remove_student(_class: Class, id: int):
    student = User.objects.filter(id=id).first()
    if student is None:
        return StatusCode.STUDENT_NOT_IN_CLASS
    if student not in _class.students.all():
        return StatusCode.STUDENT_NOT_IN_CLASS
    _class.students.remove(student)
    _class.save()
    return StatusCode.SUCCESS


@response_wrapper
@jwt_auth()
@require_POST
def remove_students(request: HttpRequest, id: int):
    request_data = parse_request(request)
    _class = Class.objects.filter(id=id).first()

    if _class is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该班级")

    student_id_list = request_data.get('students')

    status_list = []
    for student_id in student_id_list:
        status = _remove_student(_class, student_id)
        status_list.append({"code": status})
    return response({
        "message": "成功批量移除学生",
        "status": status_list
    })


def _add_teacher(_class: Class, id: int):
    teacher = User.objects.filter(id=id).first()
    if teacher is None:
        return StatusCode.REQUEST_USER_ID_NOT_EXIST
    elif teacher in _class.teachers.all():
        return StatusCode.TEACHER_ALREADY_IN_CLASS
    _class.teachers.add(teacher)
    _class.save()
    return StatusCode.SUCCESS


@response_wrapper
@jwt_auth()
@require_POST
def add_teachers(request: HttpRequest, id: int):
    request_data = parse_request(request)
    _class = Class.objects.filter(id=id).first()

    if _class is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该班级")

    teacher_id_list = request_data.get('teachers')

    status_list = []
    for teacher_id in teacher_id_list:
        status = _add_teacher(_class, teacher_id)
        status_list.append({"code": status})
    return response({
        "message": "成功批量添加老师",
        "status": status_list
    })


def _remove_teacher(_class: Class, id: int):
    teacher = User.objects.filter(id=id).first()
    if teacher is None:
        return StatusCode.REQUEST_USER_ID_NOT_EXIST
    elif teacher not in _class.teachers.all():
        return StatusCode.TEACHER_NOT_IN_CLASS
    _class.teachers.remove(teacher)
    _class.save()
    return StatusCode.SUCCESS


@response_wrapper
@jwt_auth()
@require_POST
def remove_teachers(request: HttpRequest, id: int):
    request_data = parse_request(request)
    _class = Class.objects.filter(id=id).first()

    if _class is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该班级")

    teacher_id_list = request_data.get('teachers')

    status_list = []
    for teacher_id in teacher_id_list:
        status = _remove_teacher(_class, teacher_id)
        status_list.append({"code": status})
    return response({
        "message": "成功批量移除老师",
        "status": status_list
    })

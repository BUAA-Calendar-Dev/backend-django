from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET

from application.classes.models import Class
from application.users.models import User
from application.utils.data_process import parse_request
from application.utils.response import *


def _get_user_name_list(teacher_list: list[User]):
    return [user.username for user in teacher_list]


def _get_class_info(_class: Class):
    return {
        "id": _class.id,
        "name": _class.title,
        "count": len(list(_class.students.all())),
        "teacher": _get_user_name_list(list(_class.teachers.all()))
    }


@response_wrapper
# @jwt_auth()
@require_GET
def get_class_info(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)
    _class = Class.objects.get(id=id)
    if _class is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该课程")

    return response(_get_class_info(_class))


@response_wrapper
# @jwt_auth()
@require_GET
def get_students(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)
    class_ = Class.objects.get(id=id)
    if class_ is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该课程")

    students = class_.students.all()
    student_info_list = []
    for student in students:
        student_info_list.append(_get_user_info(student.id))
    return response({
        "students": student_info_list,
        "students_num": len(student_info_list)
    })


@response_wrapper
# @jwt_auth()
@require_GET
def get_teachers(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)
    class_ = Class.objects.get(id=id)
    if class_ is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该课程")

    teachers = class_.teachers.all()
    teacher_info_list = []
    for student in teachers:
        teacher_info_list.append(_get_user_info(student.id))
    return response({
        "teachers": teacher_info_list,
        "teachers_num": len(teacher_info_list)
    })


@response_wrapper
# @jwt_auth()
@require_POST
def get_class_list(request: HttpRequest):
    user = request.user
    request_data = parse_request(request)
    classes = list(Class.objects.all())

    info_list = []
    for _class in classes:
        info_list.append(_get_class_info(_class))
    print(f"[debug] find {len(info_list)} class info"
          f"info is: {info_list}")
    return response({
        "class": info_list
    })

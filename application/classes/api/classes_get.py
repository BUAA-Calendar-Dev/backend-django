from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET

from application.classes.models import Class
from application.users.api import jwt_auth
from application.users.api.user_get import _get_user_info
from application.users.models import User
from application.users.models.user_value import *
from application.utils.data_process import parse_request
from application.utils.response import *


def _get_user_name_list(teacher_list: list[User]):
    return [teacher.username for teacher in teacher_list]


def _get_class_info(_class: Class):
    return {
        "id": _class.id,
        "name": _class.title,
        # 学生人数
        "count": len(list(_class.students.all())),
        # 教师列表
        "teacher": _get_user_name_list(list(_class.teachers.all()))
    }


@response_wrapper
@jwt_auth()
@require_GET
def get_class_info(request: HttpRequest, id: int):
    _class = Class.objects.filter(id=id).first()
    if _class is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该课程")

    return response(_get_class_info(_class))


@response_wrapper
@jwt_auth()
@require_GET
def get_students(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)
    class_ = Class.objects.filter(id=id).first()
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
@jwt_auth()
@require_GET
def get_teachers(request: HttpRequest, id: int):
    _class = Class.objects.filter(id=id).first()
    if _class is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该课程")

    teachers = _class.teachers.all()
    teacher_info_list = []
    for teacher in teachers:
        teacher_info_list.append(_get_user_info(teacher.id))
    return response({
        "teachers": teacher_info_list,
        "teachers_num": len(teacher_info_list)
    })


@response_wrapper
@jwt_auth()
@require_POST
def get_class_info_list(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()
    if user.identity == AUTH_STUDENT:
        classes = user.classes.all()
    elif user.identity == AUTH_TEACHER:
        classes = user.owned_classes.all()
    else:
        return Class.objects.all()
    classes = list(classes)

    class_info_list = []
    for _class in classes:
        class_info_list.append(_get_class_info(_class))

    print(f"[debug] find {len(class_info_list)} class info"
          f"info is: {class_info_list}")

    return response({
        "class": class_info_list
    })

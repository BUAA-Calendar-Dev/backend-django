from django.http import HttpRequest
from django.views.decorators.http import require_GET

from application.users.api import jwt_auth
from application.users.models import User
from application.users.models.user_value import *
from application.utils.response import *


def _get_user_info(id: int):
    user = User.objects.filter(id=id).first()
    print(f"[debug]user is {user}")

    if user is None:
        return None
    return {
        "username": user.username,
        "auth": user.identity,
        "name": user.name,
        "gender": user.gender,
        "avatar": user.avatar,
        "email": user.email,
        "phone": user.phone,
        "motto": user.motto,
    }


@response_wrapper
@require_GET
def get_current_user_info(request: HttpRequest):
    user = request.user
    info = _get_user_info(user.id)
    if info is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在用户")
    return response(info)


@response_wrapper
@jwt_auth()
@require_GET
def get_user_info(request: HttpRequest, id: int):
    info = _get_user_info(id)
    if info is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在用户")
    print(f"[debug] user_info is {info}")
    return response(info)

@response_wrapper
@jwt_auth()
@require_GET
def get_students(request: HttpRequest):
    students = User.objects.filter(identity=AUTH_STUDENT).all()
    return response({
        "students": [_get_user_info(student.id) for student in students]
    })

@response_wrapper
@jwt_auth()
@require_GET
def get_teachers(request: HttpRequest):
    teachers = User.objects.filter(identity=AUTH_TEACHER).all()
    return response({
        "teachers": [_get_user_info(teacher.id) for teacher in teachers]
    })
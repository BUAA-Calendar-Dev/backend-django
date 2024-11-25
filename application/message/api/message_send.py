from django.http import HttpRequest
from django.views.decorators.http import require_POST

from application.classes.models import Class
from application.message.models import Message
from application.users.models import User
from application.users.models.user_value import AUTH_STUDENT
from application.utils.data_process import parse_request
from application.utils.response import *


@response_wrapper
# @jwt_auth()
@require_POST
def send_to_student(request: HttpRequest, id: int):
    request_data = parse_request(request)

    student = User.objects.filter(id=id).first()
    if student is None:
        return response({
            "code": StatusCode.REQUEST_USER_ID_NOT_EXIST
        })

    title = request_data.get('title', '')
    content = request_data.get('content', '')

    message = Message(title=title, content=content, receive_user=student)
    message.save()
    return response({
        "message": "成功向学生发送信息"
    })


@response_wrapper
# @jwt_auth()
@require_POST
def send_to_class(request: HttpRequest, id: int):
    request_data = parse_request(request)

    _class = Class.objects.filter(id=id).first()
    if _class is None:
        return response({
            "code": StatusCode.REQUEST_USER_ID_NOT_EXIST
        })

    title = request_data.get('title', '')
    content = request_data.get('content', '')
    for student in _class.students.all():
        message = Message(title=title, content=content, receive_user=student)
        message.save()
    return response({
        "message": "成功向班级发送信息"
    })


@response_wrapper
# @jwt_auth()
@require_POST
def send_to_school(request: HttpRequest):
    request_data = parse_request(request)

    title = request_data.get('title', '')
    content = request_data.get('content', '')
    for student in User.objects.filter(identity=AUTH_STUDENT):
        message = Message(title=title, content=content, receive_user=student)
        message.save()
    return response({
        "message": "成功向全校发送信息"
    })

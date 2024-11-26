from django.http import HttpRequest
from django.views.decorators.http import require_POST

from application.message.models import Message
from application.users.api import jwt_auth
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_POST
def read_message(request: HttpRequest, id: int):
    message = Message.objects.filter(id=id).first()
    if message is None:
        return response({
            "code": StatusCode.REQUEST_MESSAGE_ID_NOT_EXIST
        })
    message.is_read = True
    message.save()

    return response({
        "message": f"成功更改-{message.title}-message的阅读状态"
    })

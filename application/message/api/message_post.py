from datetime import datetime
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from application.message.models import Message
from application.tag.models import Tag
from application.task.models import Task
from application.users.api.auth import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_request
from application.utils.response import *


@response_wrapper
# @jwt_auth()
@require_POST
def read_message(request: HttpRequest, id: int):
    user = request.user
    request_data = parse_request(request)

    message = Message.objects.get(id=id)
    message.is_read = True
    message.save()

    return response({
        "message": f"成功更改-{message.title}-message的阅读状态"
    })

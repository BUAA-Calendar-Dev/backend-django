from django.http import HttpRequest
from django.views.decorators.http import require_GET, require_POST

from application.users.api import jwt_auth
from application.users.models.user import default_preference
from application.utils.data_process import parse_request
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_GET
def get_preference(request: HttpRequest):
    user = request.user
    print(f"[debug] user.preference is {user.preference}")
    return response({
        "preference": user.preference
    })


@response_wrapper
@jwt_auth()
@require_POST
def update_preference(request: HttpRequest):
    request_data = parse_request(request)
    user = request.user
    user.preference = request_data.get("preference", default_preference)
    print(f"[debug] user.preference is {user.preference}")
    user.save()
    return response({
        "message": "更新成功"
    })

from datetime import datetime
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.core.files.storage import default_storage

from application.users.api.auth import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_data
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_GET
def get_user_info(request: HttpRequest, id: int):
    post_data = parse_data(request)
    user = User.objects.get(id=id)

    info = _get_user_info(id)
    if info is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在用户")
    return success_api_response(info)


def _get_user_info(id: int):
    user = User.objects.get(id=id)

    if user is None:
        return None
    return {
        "name": user.name,
        "avatar": default_storage.url(user.avatar),
        "email": user.email,
        "motto": user.motto,
        "gender": user.gender,
        "identity": user.identity
    }

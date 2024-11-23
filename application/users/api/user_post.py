from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.core.files.storage import default_storage

from application.users.api import name_not_allow, jwt_auth
from application.users.models import User
from application.utils.data_process import parse_data
from application.utils.response import *


@response_wrapper
# @jwt_auth()
@require_http_methods(['PUT'])
def update_user(request: HttpRequest):
    user = request.user

    post_data = parse_data(request)
    username = post_data.get('username', None)
    motto = post_data.get('motto', None)
    phone = post_data.get('phone', None)

    # 检查用户名是否已存在
    if username and User.objects.filter(username=username).exists():
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '用户名已存在')
    elif username in name_not_allow:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '非法取名')
    elif username:
        user.username = username

    # 检查个性签名是否为空
    if motto is not None:
        user.motto = motto
    if phone is not None:
        user.phone = phone

    # 更新用户
    user.save()
    return success_response({"message": "更新成功"})

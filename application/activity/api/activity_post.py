from datetime import datetime
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from application.activity.models import Activity
from application.tag.models import Tag
from application.task.models import Task
from application.users.api.auth import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_data
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_POST
def user_inout_activity(request: HttpRequest, id: int, status: str):
    user = request.user
    activity = Activity.objects.get(id=id)

    if activity is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在该活动")

    if status == "join":
        if user in activity.participants.all():
            return fail_response(ErrorCode.ALREADY_EXISTS_ERROR, "用户已在活动中")
        activity.participants.add(user)
    elif status == "exit":
        if user not in activity.participants.all():
            return fail_response(ErrorCode.NOT_FOUND_ERROR, "用户不在活动中，无法退出")
        activity.participants.remove(user)
    else:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "无效的状态")

    activity.save()
    return success_api_response({
        "message": f"成功改变用户的{status}"
    })

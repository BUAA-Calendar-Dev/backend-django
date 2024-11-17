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


def _check_user_in_activity(user: User, activity: Activity):
    return user in activity.participants


def _get_activity_detail(activity: Activity):
    return {
        "id": activity.id,
        "name": activity.content,
        "time": activity.start_time,
    }


@response_wrapper
@jwt_auth()
@require_GET
def get_activities_all(request: HttpRequest):
    user = request.user
    activity_list = list(Activity.objects.all())

    info = []
    for activity in activity_list:
        info.append({
            "id": activity.id,
            "name": activity.content,
            "time": activity.start_time,
            "tags": [],  # TODO：对tags列表的处理
            "signed-in": _check_user_in_activity(user, activity)
        })
    return success_response(info)


@response_wrapper
@jwt_auth()
@require_GET
def get_activity_detail(request: HttpRequest, id: int):
    activity = Activity.objects.get(id=id)
    return success_response({
        "content": _get_activity_detail(activity)
    })


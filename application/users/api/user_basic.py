from datetime import datetime
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from application.task.models import Task
from application.users.api.auth import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_data
from application.utils.response import *


def get_user_info(id: int):
    user = User.objects.get(id)

    if user is None:
        return None
    return {
        "name": user.name,
        "avatar": user.avatar,
        "email": user.email,
        "motto": user.motto,
        "gender": user.gender,
        "identity": user.identity
    }

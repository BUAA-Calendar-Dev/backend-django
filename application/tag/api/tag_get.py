from datetime import datetime
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from application.tag.models import Tag
from application.task.models import Task
from application.users.api.auth import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_data
from application.utils.response import *


@response_wrapper
# @jwt_auth()
@require_GET
def get_tags(request: HttpRequest):
    user = request.user
    tags_related = Tag.objects.filter(create_user=user)

    tags = []
    for tag in tags_related:
        tags.append({
            "id": tag.id,
            "title": tag.title,
            "content": tag.content,
            "color": tag.color
        })
    return success_response({
        "tags": tags,
        "tags_num": len(tags)
    })

from datetime import datetime
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from application.tag.models import Tag
from application.task.models import Task
from application.users.api.auth import jwt_auth
from application.users.models import User
from application.utils.data_process import parse_data
from application.utils.response import *


def sort_by_time(tasks_list: list):
    return sorted(tasks_list,
                  key=lambda x: x['end_time']
                  if (x['end_time'] and x['start_time'] != x['end_time'])
                  else '0000-12-31 23:59:59', reverse=True)


@response_wrapper
@jwt_auth()
@require_GET
def get_tasks_related(request: HttpRequest):
    user = request.user
    tasks_related = Task.objects.filter(create_user=user)

    tasks_list = []
    specialHours = []
    for task in tasks_related:
        tasks_list.append({
            "task-id": task.id,
            "title": task.title,
            "task-content": task.content,
            "task-time": task.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end": task.end_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return success_response({
        "specialHours": specialHours,
        "events": sort_by_time(tasks_list),
    })
from django.http import HttpRequest
from django.views.decorators.http import require_GET

from application.task.models import Task, TaskUserRelationship
from application.users.api import jwt_auth
from application.users.models import User
from application.utils.response import *


def sort_by_time(tasks_list: list):
    return sorted(tasks_list,
                  key=lambda x: x['end']
                  if (x['end'] and x['"task-time"'] != x['end'])
                  else '0000-12-31 23:59:59', reverse=True)


def _get_task_tag_list(task: Task, user: User):
    tag_list = set()
    relationship = TaskUserRelationship.objects.filter(related_user=user, task=task).first()

    # 添加活动的标签
    tag_list.update(task.tags.all())
    # 如果存在关系，添加关系的标签
    if relationship:
        tag_list.update(relationship.tags.all())
    # 将集合转换为列表返回
    return [tag.id for tag in list(tag_list)]


def _get_alarms(relationship: TaskUserRelationship):
    return [alarm.value for alarm in relationship.alarms.all()]


@response_wrapper
@jwt_auth()
@require_GET
def get_related_tasks(request: HttpRequest):
    user = request.user
    task_user_relationships = list(TaskUserRelationship.objects.filter(related_user=user))
    print(f"[debug]find {len(task_user_relationships)} relas")

    tasks_list = []
    for relationship in task_user_relationships:
        task = relationship.task
        tasks_list.append({
            "id": task.id,
            "name": relationship.name,
            "content": task.content,
            "startTime": task.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "endTime": task.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            "percentage": relationship.percentage,
            "tags": _get_task_tag_list(task, user),
            "alarms": _get_alarms(relationship)
        })

    print(f"[debug]find {len(tasks_list)} tasks")
    print(f"tasks is {tasks_list}")

    return response({
        "tasks": tasks_list,
    })

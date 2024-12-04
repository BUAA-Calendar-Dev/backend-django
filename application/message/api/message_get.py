from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.db.models import Case, When, BooleanField

from application.message.api.ddl_reminder import ddl_remind
from application.users.api import jwt_auth
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_GET
def get_messages(request: HttpRequest):
    user = request.user
    ddl_remind(user)
    
    # 先按未读状态排序（未读在前），然后按时间倒序排序
    user_messages = user.receive_message.all().annotate(
        unread=Case(
            When(is_read=False, then=True),
            default=False,
            output_field=BooleanField(),
        )
    ).order_by('-unread', '-send_time')

    messages = []
    for message in user_messages:
        messages.append({
            "id": message.id,
            "title": message.title,
            "content": message.content,
            "from": message.send_user.name,
            "time": message.send_time.strftime('%Y-%m-%d %H:%M'),
            "unread": False if message.is_read else True
        })

    print(f"[debug]messages: {messages}")
    return response({
        "messages": messages,
        "messages_num": len(messages)
    })

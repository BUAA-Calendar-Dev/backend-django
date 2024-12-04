from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from application.users.api import jwt_auth
from application.utils.response import *


@response_wrapper
@jwt_auth()
@require_GET
def get_messages(request: HttpRequest):
    user = request.user
    user_messages = user.receive_message.all()

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

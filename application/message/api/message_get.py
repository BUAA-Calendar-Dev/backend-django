from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from application.utils.response import *


@response_wrapper
# @jwt_auth()
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

            "from": message.send_user.username,
            "time": message.send_time,
            "unread": True if message.is_read else False
        })

    return response({
        "messages": messages,
        "messages_num": len(messages)
    })

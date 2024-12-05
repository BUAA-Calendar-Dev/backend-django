from application.activity.models.activity_user_relationship import ActivityUserRelationship
from application.users.models.user import User
from application.message.models.message import Message
from application.task.models.task_user_relationship import TaskUserRelationship
from django.utils import timezone
from datetime import datetime, timedelta

def has_reminded(title: str, user: User) -> bool:
    """检查是否已经发送过该任务的提醒"""
    # 检查最近24小时内是否发送过相同标题的提醒
    recent_time = timezone.now() - timedelta(minutes=user.preference.get("taskReminder", 360))
    return Message.objects.filter(
        receive_user=user,
        title__contains=title,
        send_time__gte=recent_time
    ).exists()

def send_message(title: str, content: str, user: User):
    root_user = User.objects.filter(username="rot").first()
    print(f"[debug] root_user is {root_user}")
    Message.objects.create(title=title, content=content, send_user=root_user, receive_user=user)

def ddl_remind(user: User):
    # 检查当前用户的ddl
    # 如果ddl在24小时内且未过期，则发送提醒
    task_relationships = TaskUserRelationship.objects.filter(related_user=user, percentage__lt=100).all()
    for relationship in task_relationships:
        time_diff = relationship.task.end_time - timezone.now()
        print(f"[debug] task {relationship.task.title} time_diff: {time_diff}")
        if timedelta(0) <= time_diff <= timedelta(minutes=user.preference.get("taskReminder", 360)):
            # 检查是否已经发送过提醒
            if not has_reminded(relationship.task.title, user):
                title = f"[系统提醒]：{relationship.task.title} 即将截止"
                content = f"请在{relationship.task.end_time}前完成{relationship.task.content}"
                send_message(title, content, user)
                print(f"[debug] send message-task: {relationship.task.title} {relationship.task.content}")
            else:
                print(f"[debug] task {relationship.task.title} already reminded")
    
    activity_relationships = ActivityUserRelationship.objects.filter(related_user=user, permission=1).all()
    for relationship in activity_relationships:
        time_diff = relationship.activity.start_time - timezone.now()
        print(f"[debug] activity {relationship.activity.title} time_diff: {time_diff}")
        if timedelta(0) <= time_diff <= timedelta(minutes=user.preference.get("activityReminder", 30)):
            # 检查是否已经发送过提醒
            if not has_reminded(relationship.activity.title, user):
                title = f"[系统提醒]：{relationship.activity.title} 即将开始"
                content = f"请记得在{relationship.activity.start_time}参加{relationship.activity.content}活动"
                send_message(title, content, user)
                print(f"[debug] send message-activity: {relationship.activity.title} {relationship.activity.content}")
            else:
                print(f"[debug] activity {relationship.activity.title} already reminded")

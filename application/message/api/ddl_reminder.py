import pytz
from application.activity.models.activity_user_relationship import ActivityUserRelationship
from application.users.models.user import User
from application.message.models.message import Message
from application.task.models.task_user_relationship import TaskUserRelationship
from django.utils import timezone
from datetime import datetime, timedelta

def has_reminded(title: str, user: User) -> bool:
    """检查是否已经发送过该任务的提醒"""
    china_tz = pytz.timezone('Asia/Shanghai')
    now = timezone.localtime(timezone.now(), china_tz)
    # 检查最近24小时内是否发送过相同标题的提醒
    recent_time = now - timedelta(minutes=int(user.preference.get("taskReminder", 360)))
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
    # 获取中国时区
    china_tz = pytz.timezone('Asia/Shanghai')
    # 获取当前中国时间
    now = timezone.localtime(timezone.now(), china_tz)
    now = now + timedelta(hours=8)
    print(f"[debug] time_now is {now}")

    # 检查当前用户的ddl
    task_relationships = TaskUserRelationship.objects.filter(related_user=user, percentage__lt=100).all()

    for relationship in task_relationships:
        # 直接使用 task.end_time，它已经是 datetime 对象
        task_end_time = relationship.task.end_time
        time_diff = task_end_time - now
        print(f"[debug] task {relationship.task.title} time_diff: {time_diff} end_time: {task_end_time}")

        if timedelta(0) <= time_diff <= timedelta(minutes=int(user.preference.get("taskReminder", 360))):
            if not has_reminded(relationship.task.title, user):
                title = f"[系统提醒]：{relationship.task.title} 即将截止"
                content = f"请在{task_end_time.strftime('%Y-%m-%d %H:%M')}前完成任务，其内容为：{relationship.task.content}"
                send_message(title, content, user)
                print(f"[debug] send message-task: {relationship.task.title} {relationship.task.content}")
            else:
                print(f"[debug] task {relationship.task.title} already reminded")

    activity_relationships = ActivityUserRelationship.objects.filter(related_user=user, permission=1).all()
    for relationship in activity_relationships:
        # 直接使用 activity.start_time，它已经是 datetime 对象
        activity_start_time = timezone.localtime(relationship.activity.start_time, china_tz)
        time_diff = activity_start_time - now
        print(f"[debug] activity {relationship.activity.title} time_diff: {time_diff}")

        if timedelta(0) <= time_diff <= timedelta(minutes=int(user.preference.get("activityReminder", 30))):
            if not has_reminded(relationship.activity.title, user):
                title = f"[系统提醒]：{relationship.activity.title} 即将开始"
                content = f"请记得在{activity_start_time.strftime('%Y-%m-%d %H:%M')}参加活动，其内容为：{relationship.activity.content}"
                send_message(title, content, user)
                print(f"[debug] send message-activity: {relationship.activity.title} {relationship.activity.content}")
            else:
                print(f"[debug] activity {relationship.activity.title} already reminded")

from django.db import models
from django.db.models import CASCADE

from application.tag.models import Tag
from application.task.models import Task
from application.task.models.alarm import Alarm
from application.users.models import User

PERMISSION_CHOICE = (
    (0, '创建'),
    (1, '参与')
)


class TaskUserRelationship(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    # 关系标记的唯一任务
    task = models.ForeignKey(Task, related_name="relationship", on_delete=CASCADE)
    # 相关的用户
    related_user = models.ForeignKey(User,
                                     related_name="task_relationship",
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)
    # ddl提醒
    alarms = models.ManyToManyField(Alarm, verbose_name="alarms")
    # 任务别名
    name = models.CharField(max_length=256, default="任务名", verbose_name="aliasName")
    # 完成情况
    percentage = models.FloatField(verbose_name="finish_percentage", default=0)
    # 权限管理
    permission = models.IntegerField(verbose_name="permission", choices=PERMISSION_CHOICE, default=0)
    # 自定义私有tag
    tags = models.ManyToManyField(Tag,
                                  related_name="tasks_have_tag",
                                  blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'task_user_relationship'

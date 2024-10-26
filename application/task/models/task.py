from django.db import models

from application.tag.models import Tag
from application.users.models import User


class Task(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    title = models.CharField(max_length=256, default="活动", verbose_name="title")
    content = models.CharField(max_length=1024, default="任务描述", verbose_name="content")

    start_time = models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name="start_time")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="end_time")

    create_user = models.ForeignKey(User,
                                    verbose_name="create_user",
                                    related_name="task_create",
                                    on_delete=models.CASCADE,
                                    blank=True, null=True)
    # 默认包含了创建的user
    related_users = models.ManyToManyField(User,
                                           verbose_name="related_users",
                                           related_name="tasks_related",
                                           blank=True)

    tags = models.ManyToManyField(Tag,
                                  verbose_name="task_tag",
                                  related_name="tasks_have_tag",
                                  blank=True)

    # 允许任务具有子任务，使用父任务的方式来简历树状结构
    # TODO：考虑嵌套层次的限制
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='son_task')

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'task'

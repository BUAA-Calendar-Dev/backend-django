from django.db import models

from application.tag.models import Tag
from application.users.models import User


class Task(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    name = models.CharField(max_length=256, default="活动", verbose_name="name")
    content = models.CharField(max_length=1024, default="任务描述", verbose_name="content")

    start_time = models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name="start_time")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="end_time")

    create_users = models.ManyToManyField(User, verbose_name="create_users",
                                          related_name="tasks_created")
    related_uses = models.ManyToManyField(User, verbose_name="related_users",
                                          related_name="tasks_related")

    tags = models.ManyToManyField(Tag, verbose_name="task_tag", related_name="tasks_have_tag")

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'task'

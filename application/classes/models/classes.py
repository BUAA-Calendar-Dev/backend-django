from django.db import models

from application.task.models import Task
from application.users.models import User


class Class(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    title = models.CharField(max_length=256, default="班级", verbose_name="title")
    introduction = models.TextField(default="暂时还没有班级介绍", verbose_name="introduction")

    students = models.ManyToManyField(User, verbose_name="students", related_name="classes", blank=True)
    teachers = models.ManyToManyField(User, verbose_name="teachers", related_name="owned_classes", blank=True)

    tasks = models.ManyToManyField(Task, verbose_name="tasks", related_name="shared_classes", blank=True)

    def __str__(self):
        return str(f"[class]{self.title}")

    class Meta:
        db_table = 'classes'

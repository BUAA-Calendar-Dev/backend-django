from django.db import models

from application.task.models import Task
from application.users.models import User


class Class(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    title = models.CharField(max_length=1024, default="班级", verbose_name="class_title")
    introduction = models.CharField(max_length=1024, default="暂时还没有班级介绍", verbose_name="class_intro")

    students = models.ManyToManyField(User, verbose_name="class_students", related_name="classes")
    teachers = models.ManyToManyField(User, verbose_name="class_teachers", related_name="owned_classes")

    tasks = models.ManyToManyField(Task, verbose_name="class_tasks", related_name="shared_classes")

    def __str__(self):
        return str(f"{self.title} {self.id}")

    class Meta:
        db_table = 'classes'

from django.db import models
from django.db.models import CASCADE

from application.tag.models import Tag
from application.task.models import Task
from application.users.models import User

PERMISSION_CHOICE = (
    (0, '创建'),
    (1, '参与')
)


class TaskUserRelationship(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    # 关系标记的唯一任务
    task = models.ForeignKey(Task, verbose_name="task_ponit", related_name="relationship", on_delete=CASCADE)
    # 手动保证为任务名
    name = models.CharField(max_length=256, default="任务名", verbose_name="aliasName")

    # 完成情况
    percentage = models.FloatField(verbose_name="finish_percentage", default=0)

    permission = models.IntegerField(verbose_name="permission", choices=PERMISSION_CHOICE, default=0)

    tags = models.ManyToManyField(Tag,
                                  verbose_name="task_tag",
                                  related_name="tasks_have_tag",
                                  blank=True)

    related_user = models.ForeignKey(User,
                                     verbose_name="related_user",
                                     related_name="task_relationship",
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'task_user_relationship'

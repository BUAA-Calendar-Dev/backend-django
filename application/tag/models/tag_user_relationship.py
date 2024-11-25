from django.db import models
from django.db.models import CASCADE

from application.tag.models import Tag
from application.task.models import Task
from application.users.models import User

PERMISSION_CHOICE = (
    (0, '可以修改'),
    (1, '只能查看')
)


class TagUserRelationship(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    # 关联的tag
    tag = models.ForeignKey(Tag,
                            verbose_name="related_tag",
                            related_name="tag_relationship",
                            on_delete=models.CASCADE,
                            blank=True, null=True)
    # 关联的user
    user = models.ForeignKey(User,
                             verbose_name="related_user",
                             related_name="task_relationship",
                             on_delete=models.CASCADE,
                             blank=True, null=True)
    task = models.ForeignKey(Task, verbose_name="task_ponit", related_name="relationship", on_delete=CASCADE)

    # 别名
    name = models.CharField(max_length=256, default="任务名", verbose_name="aliasName")
    # 自定义颜色
    color = models.CharField(max_length=64, default="#FFEFDB", verbose_name="color")

    # 权限
    permission = models.IntegerField(verbose_name="permission", choices=PERMISSION_CHOICE, default=0)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'tag_user_relationship'

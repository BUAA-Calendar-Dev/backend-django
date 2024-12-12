from django.db import models
from django.db.models import CASCADE

from application.activity.models import Activity
from application.tag.models import Tag
from application.users.models import User

PERMISSION_CHOICE = (
    (0, '创建'),
    (1, '参与')
)


class ActivityUserRelationship(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    # 关系标记的唯一任务
    activity = models.ForeignKey(Activity, verbose_name="activity_ponit", related_name="relationship",
                                 on_delete=CASCADE)
    # 相关的用户
    related_user = models.ForeignKey(User,
                                     related_name="related_activities",
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)

    # 手动保证为任务名
    name = models.CharField(max_length=256, default="任务名", verbose_name="aliasName")

    permission = models.IntegerField(verbose_name="permission", choices=PERMISSION_CHOICE, default=0)

    tags = models.ManyToManyField(Tag,
                                  related_name="activities_have_tag",
                                  blank=True)
    # 自定义颜色
    color = models.CharField(max_length=64, default="", verbose_name="color")

    def __str__(self):
        return f"[activity_rela]{self.name, self.related_user.username}"

    class Meta:
        db_table = 'activity_user_relationship'

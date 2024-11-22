from django.db import models

from application.users.models import User


class Tag(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    title = models.CharField(max_length=256, default="tag名", verbose_name="title")
    content = models.CharField(max_length=1024, default="暂无tag描述", verbose_name="content")

    color = models.CharField(max_length=64, default="#FFEFDB", verbose_name="color")
    fixed = models.BooleanField(verbose_name="fixed", default=False)

    def __str__(self):
        return f"@tag-{self.title}"

    class Meta:
        db_table = 'tag'

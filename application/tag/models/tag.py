from django.db import models

from application.users.models import User


class Tag(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    name = models.CharField(max_length=256, default="tag名", verbose_name="tag_name")
    content = models.CharField(max_length=1024, default="暂无tag描述", verbose_name="tag_content")

    create_user = models.ForeignKey(User,
                                    verbose_name="create_user",
                                    related_name="tag_create",
                                    on_delete=models.CASCADE,
                                    blank=True, null=True)

    def __str__(self):
        return f"@tag-{self.name}"

    class Meta:
        db_table = 'tag'

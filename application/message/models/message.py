from django.db import models

from application.users.models import User


class Message(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    title = models.CharField(max_length=256, default="email", verbose_name="title")
    content = models.CharField(max_length=4096, default="信息内容", verbose_name="content")

    send_time = models.DateTimeField(blank=False, null=False, verbose_name="send_time",
                                     auto_now_add=True)
    # 是否已读
    is_read = models.BooleanField(default=False, verbose_name="is_read")
    # 将message归属到唯一的user
    send_user = models.ForeignKey(User,
                                  verbose_name="from_user",
                                  related_name="send_message",
                                  on_delete=models.CASCADE,
                                  blank=True, null=True)
    receive_user = models.ForeignKey(User,
                                     verbose_name="receive_user",
                                     related_name="receive_message",
                                     on_delete=models.CASCADE,
                                     blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'message'

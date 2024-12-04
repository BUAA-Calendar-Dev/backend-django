from django.db import models
from application.users.models import User


class Comment(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    content = models.TextField(default="", verbose_name="content")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="author")
    time = models.DateTimeField(blank=False, null=False, verbose_name="time", auto_now_add=True)

    # 父评论，如果是一级评论则为空
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    # 添加一个方法来判断是否为一级评论
    @property
    def is_parent(self):
        return self.parent is None

    # 添加一个方法来获取所有回复
    def get_replies(self):
        return self.replies.all()

    def __str__(self):
        return f"[comment] {self.content}"

    class Meta:
        db_table = 'comment'
        ordering = ['time']

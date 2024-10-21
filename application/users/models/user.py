from django.contrib.auth.models import AbstractUser
from django.db import models

from application.tag.models import Tag
from application.users.models.user_value import *


class User(AbstractUser):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    password = models.CharField(max_length=256, verbose_name="密码")

    gender = models.CharField(choices=GENDER_CHOICE, max_length=32, default="保密", verbose_name="性别")
    identity = models.CharField(choices=IDENTITY_CHOICE, max_length=32, default="学生", verbose_name="身份")

    tags = models.ManyToManyField(Tag, verbose_name="own_tags", related_name="tasks_owners")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_users',  # 这里将 related_name 改为 'custom_users'
        related_query_name='custom_user',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_users',
        related_query_name='custom_user',
        blank=True,
    )

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-date_joined']
        verbose_name = '用户'
        verbose_name_plural = '用户'

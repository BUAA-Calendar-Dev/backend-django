from django.contrib.auth.models import AbstractUser
from django.db import models

from application.users.models.user_value import *


class User(AbstractUser):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    password = models.CharField(max_length=256, verbose_name="password")

    name = models.CharField(max_length=32, default="保密", verbose_name="name")
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.png', verbose_name='avatar')
    email = models.EmailField(unique=True, verbose_name='email',
                              error_messages={'unique': '该邮箱已被注册'}, blank=False)
    phone = models.CharField(max_length=32, default="未定义", verbose_name="phone")

    motto = models.CharField(max_length=256, default='这个人很懒，什么都没有留下', verbose_name='motto')
    gender = models.CharField(choices=GENDER_CHOICE, max_length=32, default="保密", verbose_name="gender")

    identity = models.CharField(choices=IDENTITY_CHOICE, max_length=32, default="学生", verbose_name="identity")

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

    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_joined']
        verbose_name = '用户'
        verbose_name_plural = '用户'

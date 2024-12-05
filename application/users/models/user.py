from django.contrib.auth.models import AbstractUser
from django.db import models

from application.users.models.user_value import *

default_avatar = "https://pigkiller-011955-1319328397.cos.ap-beijing.myqcloud.com/img/202407241830349.avif"

default_preference = {
    "activityReminder": "30",
    "taskReminder": "360",
    "activityColor": "#409EFF",
    "taskColor": "#F56C6C",
    "defaultView": "calendar",
    "theme": "light",
}


class User(AbstractUser):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    password = models.CharField(max_length=256, verbose_name="password")
    # 身份鉴权
    identity = models.IntegerField(choices=IDENTITY_CHOICE, default=AUTH_STUDENT, verbose_name="identity")
    # 用户是否已经被删除
    isDelete = models.BooleanField(default=False)

    # 用户名
    name = models.CharField(max_length=32, default="默认昵称", verbose_name="name")
    # 性别
    gender = models.CharField(choices=GENDER_CHOICE, max_length=32, default="保密", verbose_name="gender")
    # 头像
    avatar = models.CharField(default=default_avatar, verbose_name='avatar', max_length=500)
    # 邮箱
    email = models.EmailField(unique=True, default='邮箱还未定义', error_messages={'unique': '该邮箱已被注册'},
                              verbose_name='email')
    # 手机号
    phone = models.CharField(max_length=32, default="手机号还未定义", verbose_name="phone")
    # 个性签名
    motto = models.CharField(max_length=256, default='这个人很懒，什么都没有留下', verbose_name='motto')

    # 偏好
    preference = models.JSONField(default=dict, verbose_name="preference")

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
        return f"[user]{self.username}"

    class Meta:
        ordering = ['-date_joined']

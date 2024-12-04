# Generated by Django 5.1.1 on 2024-12-04 17:52

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("password", models.CharField(max_length=256, verbose_name="password")),
                (
                    "identity",
                    models.IntegerField(
                        choices=[(0, "管理员"), (1, "教师"), (2, "学生")],
                        default=2,
                        verbose_name="identity",
                    ),
                ),
                ("isDelete", models.BooleanField(default=False)),
                (
                    "name",
                    models.CharField(
                        default="默认昵称", max_length=32, verbose_name="name"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("secret", "不设置/保密"), ("male", "男"), ("female", "女")],
                        default="保密",
                        max_length=32,
                        verbose_name="gender",
                    ),
                ),
                (
                    "avatar",
                    models.CharField(
                        default="https://pigkiller-011955-1319328397.cos.ap-beijing.myqcloud.com/img/202407241830349.avif",
                        max_length=500,
                        verbose_name="avatar",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        default="邮箱还未定义",
                        error_messages={"unique": "该邮箱已被注册"},
                        max_length=254,
                        unique=True,
                        verbose_name="email",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        default="手机号还未定义", max_length=32, verbose_name="phone"
                    ),
                ),
                (
                    "motto",
                    models.CharField(
                        default="这个人很懒，什么都没有留下", max_length=256, verbose_name="motto"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        related_name="custom_users",
                        related_query_name="custom_user",
                        to="auth.group",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="custom_users",
                        related_query_name="custom_user",
                        to="auth.permission",
                    ),
                ),
            ],
            options={
                "ordering": ["-date_joined"],
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="AuthRecord",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("login_at", models.DateTimeField()),
                ("expires_by", models.DateTimeField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "default_permissions": (),
            },
        ),
    ]

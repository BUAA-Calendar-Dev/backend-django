# Generated by Django 5.1.1 on 2024-11-22 07:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tag", "0003_tag_color_tag_fixed"),
        ("task", "0003_alter_task_start_time"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="create_user",
        ),
        migrations.RemoveField(
            model_name="task",
            name="related_users",
        ),
        migrations.RemoveField(
            model_name="task",
            name="tags",
        ),
        migrations.CreateModel(
            name="TaskUserRelationship",
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
                    "name",
                    models.CharField(
                        default="任务名", max_length=256, verbose_name="aliasName"
                    ),
                ),
                (
                    "permission",
                    models.IntegerField(choices=[(0, "创建"), (1, "参与")], default=0),
                ),
                (
                    "related_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_relationship",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="related_user",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True,
                        related_name="tasks_have_tag",
                        to="tag.tag",
                        verbose_name="task_tag",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="relationship",
                        to="task.task",
                        verbose_name="task_ponit",
                    ),
                ),
            ],
            options={
                "db_table": "user_task_relationship",
            },
        ),
    ]
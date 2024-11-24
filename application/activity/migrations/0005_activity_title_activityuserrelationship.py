# Generated by Django 5.1.1 on 2024-11-24 16:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("activity", "0004_activity_is_public"),
        ("tag", "0004_remove_tag_create_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="activity",
            name="title",
            field=models.CharField(
                default="活动标题", max_length=256, verbose_name="title"
            ),
        ),
        migrations.CreateModel(
            name="ActivityUserRelationship",
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
                    models.IntegerField(
                        choices=[(0, "创建"), (1, "参与")],
                        default=0,
                        verbose_name="permission",
                    ),
                ),
                (
                    "related_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_activities",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True, related_name="activities_have_tag", to="tag.tag"
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="relationship",
                        to="activity.activity",
                        verbose_name="activity_ponit",
                    ),
                ),
            ],
            options={
                "db_table": "activity_user_relationship",
            },
        ),
    ]
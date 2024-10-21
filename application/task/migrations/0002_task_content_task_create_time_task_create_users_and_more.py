# Generated by Django 5.1.1 on 2024-10-21 06:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0001_initial"),
        ("users", "0003_remove_user_charge_classes_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="content",
            field=models.CharField(
                default="任务描述", max_length=1024, verbose_name="content"
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="create_time",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="create_time",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="task",
            name="create_users",
            field=models.ManyToManyField(
                related_name="tasks_created",
                to="users.user",
                verbose_name="create_users",
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="name",
            field=models.CharField(default="活动", max_length=256, verbose_name="name"),
        ),
        migrations.AddField(
            model_name="task",
            name="overdue_time",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="overdue_time",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="task",
            name="related_uses",
            field=models.ManyToManyField(
                related_name="tasks_related",
                to="users.user",
                verbose_name="related_users",
            ),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-21 06:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0002_task_content_task_create_time_task_create_users_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="overdue_time",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="overdue_time"
            ),
        ),
    ]

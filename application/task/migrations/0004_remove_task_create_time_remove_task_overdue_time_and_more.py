# Generated by Django 5.1.1 on 2024-10-21 07:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tag", "0002_tag_name"),
        ("task", "0003_alter_task_overdue_time"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="create_time",
        ),
        migrations.RemoveField(
            model_name="task",
            name="overdue_time",
        ),
        migrations.AddField(
            model_name="task",
            name="end_time",
            field=models.DateTimeField(blank=True, null=True, verbose_name="end_time"),
        ),
        migrations.AddField(
            model_name="task",
            name="start_time",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="start_time",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="task",
            name="tags",
            field=models.ManyToManyField(
                related_name="tasks_have_tag", to="tag.tag", verbose_name="task_tag"
            ),
        ),
    ]

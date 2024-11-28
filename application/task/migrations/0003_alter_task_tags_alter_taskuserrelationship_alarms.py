# Generated by Django 5.1.1 on 2024-11-28 07:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tag", "0002_initial"),
        ("task", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                related_name="tag_tasks",
                to="tag.tag",
                verbose_name="task_tag",
            ),
        ),
        migrations.AlterField(
            model_name="taskuserrelationship",
            name="alarms",
            field=models.ManyToManyField(
                blank=True, to="task.alarm", verbose_name="alarms"
            ),
        ),
    ]

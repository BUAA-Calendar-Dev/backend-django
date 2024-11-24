# Generated by Django 5.1.1 on 2024-11-24 17:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tag", "0004_remove_tag_create_user"),
        ("task", "0006_alter_taskuserrelationship_related_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="tags",
            field=models.ManyToManyField(
                related_name="tag_tasks", to="tag.tag", verbose_name="task_tag"
            ),
        ),
        migrations.AlterField(
            model_name="taskuserrelationship",
            name="task",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="relationship",
                to="task.task",
            ),
        ),
    ]

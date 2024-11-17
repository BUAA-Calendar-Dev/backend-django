# Generated by Django 5.1.1 on 2024-10-26 05:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("tag", "0002_initial"),
        ("task", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="create_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="task_create",
                to="users.user",
                verbose_name="create_user",
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="parent_task",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="son_task",
                to="task.task",
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="related_users",
            field=models.ManyToManyField(
                blank=True,
                related_name="tasks_related",
                to="users.user",
                verbose_name="related_users",
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="tags",
            field=models.ManyToManyField(
                blank=True,
                related_name="tasks_have_tag",
                to="tag.tag",
                verbose_name="task_tag",
            ),
        ),
    ]
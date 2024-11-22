# Generated by Django 5.1.1 on 2024-11-22 08:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0004_remove_task_create_user_remove_task_related_users_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="taskuserrelationship",
            name="percentage",
            field=models.FloatField(default=0, verbose_name="finish_percentage"),
        ),
        migrations.AlterField(
            model_name="taskuserrelationship",
            name="permission",
            field=models.IntegerField(
                choices=[(0, "创建"), (1, "参与")], default=0, verbose_name="permission"
            ),
        ),
        migrations.AlterModelTable(
            name="taskuserrelationship",
            table="task_user_relationship",
        ),
    ]
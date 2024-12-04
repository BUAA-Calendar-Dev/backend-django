# Generated by Django 5.1.1 on 2024-12-01 02:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0003_alter_task_tags_alter_taskuserrelationship_alarms"),
    ]

    operations = [
        migrations.AddField(
            model_name="taskuserrelationship",
            name="is_finished",
            field=models.BooleanField(default=False, verbose_name="is_finished"),
        ),
        migrations.AlterField(
            model_name="taskuserrelationship",
            name="percentage",
            field=models.IntegerField(default=0, verbose_name="finish_percentage"),
        ),
    ]
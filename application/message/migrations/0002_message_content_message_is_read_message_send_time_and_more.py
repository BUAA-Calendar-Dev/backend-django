# Generated by Django 5.1.1 on 2024-11-22 08:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("message", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="content",
            field=models.CharField(
                default="任务描述", max_length=1024, verbose_name="content"
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="is_read",
            field=models.BooleanField(default=False, verbose_name="is_read"),
        ),
        migrations.AddField(
            model_name="message",
            name="send_time",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="send_time",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="message",
            name="title",
            field=models.CharField(
                default="email", max_length=256, verbose_name="title"
            ),
        ),
    ]

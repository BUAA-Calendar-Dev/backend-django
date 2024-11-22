# Generated by Django 5.1.1 on 2024-11-22 08:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("message", "0002_message_content_message_is_read_message_send_time_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="receive_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="receive_message",
                to=settings.AUTH_USER_MODEL,
                verbose_name="receive_user",
            ),
        ),
        migrations.AddField(
            model_name="message",
            name="send_user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="send_message",
                to=settings.AUTH_USER_MODEL,
                verbose_name="from_user",
            ),
        ),
    ]
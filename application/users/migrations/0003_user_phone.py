# Generated by Django 5.1.1 on 2024-11-17 08:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_motto_alter_user_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(default="未定义", max_length=32, verbose_name="phone"),
        ),
    ]

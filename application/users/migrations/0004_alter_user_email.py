# Generated by Django 5.1.1 on 2024-12-10 13:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_alter_user_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                blank=True,
                default="邮箱还未定义",
                error_messages={"unique": "该邮箱已被注册"},
                max_length=254,
                verbose_name="email",
            ),
        ),
    ]
# Generated by Django 5.1.1 on 2024-12-04 17:52

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="tag名", max_length=256, verbose_name="title"
                    ),
                ),
                (
                    "content",
                    models.CharField(
                        default="暂无tag描述", max_length=1024, verbose_name="content"
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        default="#FFEFDB", max_length=64, verbose_name="color"
                    ),
                ),
                ("fixed", models.BooleanField(default=True, verbose_name="fixed")),
            ],
            options={
                "db_table": "tag",
            },
        ),
    ]

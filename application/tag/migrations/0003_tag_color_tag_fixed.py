# Generated by Django 5.1.1 on 2024-11-17 08:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tag", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="color",
            field=models.CharField(
                default="#FFEFDB", max_length=64, verbose_name="color"
            ),
        ),
        migrations.AddField(
            model_name="tag",
            name="fixed",
            field=models.BooleanField(default=False, verbose_name="fixed"),
        ),
    ]

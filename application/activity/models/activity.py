from django.db import models

from application.tag.models import Tag


class Activity(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    is_public = models.BooleanField(default=False)

    title = models.CharField(max_length=256, default="活动标题", verbose_name="title")
    content = models.CharField(max_length=1024, default="活动描述", verbose_name="content")
    place = models.CharField(max_length=1024, default="活动地点", verbose_name="place")

    start_time = models.DateTimeField(blank=False, null=False, verbose_name="start_time")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="end_time")

    tags = models.ManyToManyField(Tag, verbose_name="activity_tag", related_name="tag_activities", blank=True)

    def __str__(self):
        return f"[activity]{self.title}"

    class Meta:
        db_table = 'activity'

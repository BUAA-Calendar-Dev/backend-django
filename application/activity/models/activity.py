from django.db import models

from application.tag.models import Tag
from application.users.models import User


class Activity(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    place = models.CharField(max_length=1024, default="活动地点", verbose_name="place")
    content = models.CharField(max_length=1024, default="活动描述", verbose_name="content")

    start_time = models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name="start_time")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="end_time")

    participants = models.ManyToManyField(User, verbose_name="activity_participants", related_name="activities_in")
    owners = models.ManyToManyField(User, verbose_name="activity_owners", related_name="activities_own")

    tags = models.ManyToManyField(Tag, verbose_name="activity_tag", related_name="tags")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'activity'

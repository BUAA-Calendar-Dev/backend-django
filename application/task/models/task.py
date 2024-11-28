from django.db import models

from application.tag.models import Tag


class Task(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    title = models.CharField(max_length=256, default="活动", verbose_name="title")
    content = models.CharField(max_length=1024, default="任务描述", verbose_name="content")

    start_time = models.DateTimeField(blank=False, null=False, verbose_name="start_time")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="end_time")

    # 允许任务具有子任务，使用父任务的方式来简历树状结构
    # TODO：考虑嵌套层次的限制
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='son_task')

    tags = models.ManyToManyField(Tag, verbose_name="task_tag", related_name="tag_tasks", blank=True)

    def __str__(self):
        return f"[task]{self.title}"

    class Meta:
        db_table = 'task'

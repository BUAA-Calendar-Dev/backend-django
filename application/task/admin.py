from django.contrib import admin

from application.task.models import Task
from application.task.models import TaskUserRelationship

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskUserRelationship)

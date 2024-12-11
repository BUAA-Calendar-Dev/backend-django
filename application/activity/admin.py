from django.contrib import admin

from application.activity.models import Activity
from application.activity.models.activity_user_relationship import ActivityUserRelationship

# Register your models here.
admin.site.register(Activity)
admin.site.register(ActivityUserRelationship)

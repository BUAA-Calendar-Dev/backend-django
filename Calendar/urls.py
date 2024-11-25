from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from Calendar import settings

urlpatterns = [
    path("admin", admin.site.urls),

    path("api/token/", include('application.csrf.csrf_token')),
    # 用户
    path("api/user/", include('application.users.urls')),
    # 班级
    path("api/class/", include('application.classes.urls')),
    # 活动
    path("api/activity/", include('application.activity.urls')),
    # 任务
    path("api/task/", include('application.task.urls')),
    path("api/event/", include('application.task.urls')),
    # 信息
    path("api/message/", include('application.message.urls')),
    # 标签
    path("api/tag/", include('application.tag.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

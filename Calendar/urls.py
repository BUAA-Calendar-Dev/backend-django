from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from Calendar import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r'^api/', include([
        path("token/", include('application.csrf.csrf_token')),
        # 用户
        path("user/", include('application.users.urls')),
        # 班级
        path("class/", include('application.classes.urls')),
        # 活动
        path("activity/", include('application.activity.urls')),
        # 任务
        path("task/", include('application.task.urls')),
        path("event/", include('application.task.urls')),
        # 信息
        path("message/", include('application.message.urls')),
        # 标签
        path("tag/", include('application.tag.urls')),

    ])),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

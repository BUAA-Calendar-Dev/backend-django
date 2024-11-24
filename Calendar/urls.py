from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from Calendar import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r'^api/', include([
        path("token/", include('application.csrf.csrf_token')),
        path("user/", include('application.users.urls')),

        path("activity/", include('application.activity.urls')),
        path("class/", include('application.classes.urls')),
        path("message/", include('application.message.urls')),
        path("tag/", include('application.tag.urls')),
        path("task/", include('application.task.urls')),
        path("event/", include('application.task.urls')),

    ])),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

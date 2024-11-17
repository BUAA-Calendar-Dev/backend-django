from django.urls import path
from django.middleware.csrf import get_token
from application.utils.response import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse(data={'token': csrf_token})


urlpatterns = [
    path('', get_csrf_token),
]

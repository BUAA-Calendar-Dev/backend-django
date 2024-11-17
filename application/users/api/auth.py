from datetime import timedelta

import jwt
from django.utils import timezone
from django.views.decorators.http import require_POST, require_GET

from Calendar import settings
from ..models import User
from ..models.auth_record import AuthRecord
from ...utils.response import *


@response_wrapper
@require_GET
def refresh_token(request):
    """
    刷新token
    """
    try:
        # 从请求头中获取token
        header = request.META.get('HTTP_AUTHORIZATION')
        if header is None:
            raise jwt.InvalidTokenError
        # 解码token
        auth_info = header.split(' ')
        if len(auth_info) != 2:
            raise jwt.InvalidTokenError
        auth_type, auth_token = auth_info
        if auth_type != 'Bearer':
            raise jwt.InvalidTokenError
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            print('InvalidTokenError')
            raise jwt.InvalidTokenError

        if payload['type'] != 'refresh_token':
            raise jwt.InvalidTokenError

        user_id = payload['user_id']
        record_id = payload['record_id']
        user = User.objects.filter(id=user_id).first()
        record = AuthRecord.objects.filter(id=record_id).first()

        if record is None or record.user != user:
            raise jwt.InvalidTokenError

        if record.expires_by < timezone.now():
            raise jwt.InvalidTokenError

        # 生成新的token
        token = generate_token(user)

        return success_response({'token': token})
    except jwt.InvalidTokenError:
        return fail_response(ErrorCode.INVALID_TOKEN_ERROR, '登录过期, token无效')


def byte2str(b):
    if type(b) is str:
        return b
    return b.decode('utf-8')


def get_user(request) -> User:
    header = request.META.get('HTTP_AUTHORIZATION')
    try:
        if header is None:
            raise jwt.InvalidTokenError

        # 解码token
        auth_info = header.split(' ')

        if len(auth_info) != 2:
            raise jwt.InvalidTokenError
        auth_type, auth_token = auth_info

        if auth_type != 'Bearer':
            raise jwt.InvalidTokenError
        payload = jwt.decode(auth_token, key=settings.SECRET_KEY, algorithms=['HS256'])

        if payload['type'] != 'access_token':
            raise jwt.InvalidTokenError
        user_id = payload['user_id']
        user = User.objects.filter(id=user_id).first()
        if user is None:
            raise jwt.InvalidTokenError
        return user
    except jwt.InvalidTokenError:
        return None


def generate_token(user: User, access_token_delta: int = 1) -> str:
    """generate jwt

        Args:
            user (User): user
            access_token_delta (int, optional): time to expire. Defaults to 1 (hour).
    """

    current_time = timezone.now()
    access_token_payload = {
        "user_id": user.id,
        "exp": current_time + timedelta(hours=access_token_delta),
        "iat": current_time,
        "type": "access_token",
    }

    return byte2str(jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256"))


def generate_refresh_token(user: User, refresh_token_delta: int = 6 * 24) -> str:
    """generate jwt

    Args:
        user (User): user
        refresh_token_delta (int, optional): time to expire. Defaults to 6 days (7 * 24 hours).
    """

    current_time = timezone.now()

    # 删除旧的refresh_token
    AuthRecord.objects.filter(user=user).delete()

    auth_record = AuthRecord(user=user, login_at=current_time,
                             expires_by=current_time + timedelta(hours=refresh_token_delta))
    auth_record.save()

    refresh_token_payload = {
        "user_id": user.id,
        "record_id": auth_record.id,
        "iat": current_time,
        "type": "refresh_token",
    }

    return byte2str(jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"))


def jwt_auth(allow_anonymous=False):
    def decorator(api):
        def wrapper(request, *args, **kwargs):
            user = get_user(request)
            if user is None or user.isDelete:
                if allow_anonymous:
                    user = None
                else:
                    return fail_response(ErrorCode.UNAUTHORIZED_ERROR, '未登录')
            request.user = user
            return api(request, *args, **kwargs)
        return wrapper
    return decorator




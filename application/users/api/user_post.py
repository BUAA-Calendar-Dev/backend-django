import os

from django.http import HttpRequest
from django.views.decorators.http import require_POST

from Calendar import settings
from application.users.api import name_not_allow
from application.users.models import User
from application.users.models.user_value import AUTH_TEACHER
from application.utils.data_process import parse_request
from application.utils.pic_upload import upload
from application.utils.response import *


@response_wrapper
# @jwt_auth()
@require_POST
def modify_user_info(request: HttpRequest):
    user = request.user

    request_data = parse_request(request)
    username = request_data.get('username', None)
    motto = request_data.get('motto', None)
    phone = request_data.get('phone', None)

    # 检查用户名是否已存在
    if username and User.objects.filter(username=username).exists():
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '用户名已存在')
    elif username in name_not_allow:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '非法取名')
    elif username:
        user.username = username

    # 检查个性签名是否为空
    if motto is not None:
        user.motto = motto
    if phone is not None:
        user.phone = phone

    # 更新用户
    user.save()
    return response({
        "message": "更新成功"
    })


@response_wrapper
# @jwt_auth()
@require_POST
def impower_user(request: HttpRequest):
    request_data = parse_request(request)
    user_id = request_data.get('userid')

    user = User.objects.get(id=user_id)
    user.identity = AUTH_TEACHER
    user.save()

    return response({
        "message": f"成功将用户{user.username}权限提升为老师"
    })


@response_wrapper
@require_POST
def update_avatar(request):
    user = User.objects.get(id=request.user.id)

    # 由前端指定的name获取到图片数据
    img = request.FILES.get('img')

    # 截取文件后缀和文件名
    img_name = img.name
    file_name = os.path.splitext(img_name)[0]
    file_type = os.path.splitext(img_name)[1]
    # 重定义文件名
    img_name = f'avatar-{file_name}{file_type}'
    # 从配置文件中载入图片保存路径
    img_path = os.path.join(settings.STATIC_URL, img_name)

    # 写入文件到指定地址
    with open(img_path, 'ab') as fp:
        # 如果上传的图片非常大，就通过chunks()方法分割成多个片段来上传
        for chunk in img.chunks():
            fp.write(chunk)
    url = upload(img_path, img_name)

    user.avatar = url
    user.save()

    print(f"[debug] upload img's url is {url}")

    return response({
        "avatar": url,
        "message": "上传成功",
    })

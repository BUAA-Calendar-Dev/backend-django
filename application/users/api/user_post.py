import os

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from Calendar import settings
from application.users.api import name_not_allow, jwt_auth
from application.users.models import User
from application.users.models.user_value import AUTH_TEACHER
from application.utils.data_process import parse_request
from application.utils.pic_upload import upload
from application.utils.response import *


@response_wrapper
@jwt_auth()
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
@jwt_auth()
@require_POST
def impower_user(request: HttpRequest):
    request_data = parse_request(request)
    user_id = request_data.get('userid')

    user = User.objects.filter(id=user_id).first()
    user.identity = AUTH_TEACHER
    user.save()

    return response({
        "message": f"成功将用户{user.username}权限提升为老师"
    })


@response_wrapper
@jwt_auth()
@require_POST
def update_avatar(request):
    try:
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return fail_response(ErrorCode.USER_NOT_FOUND, "用户不存在")

        # 由前端指定的name获取到图片数据
        img = request.FILES.get('img')
        if not img:
            return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "没有收到文件")

        # 截取文件后缀和文件名
        img_name = img.name
        file_name = os.path.splitext(img_name)[0]
        file_type = os.path.splitext(img_name)[1]
        # 重定义文件名
        img_name = f'avatar-{file_name}{file_type}'
        
        # 确保static目录存在
        static_dir = os.path.join(settings.BASE_DIR, 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
            
        # 保存到static目录
        img_path = os.path.join(static_dir, img_name)

        # 写入文件到指定地址
        with open(img_path, 'wb') as fp:
            # 如果上传的图片非常大，就通过chunks()方法分割成多个片段来上传
            for chunk in img.chunks():
                fp.write(chunk)
        
        url = upload(img_path, img_name)
        user.avatar = url
        user.save()
        
        print(f"[debug] upload avatar: {url}")

        return response({
            "avatar": url,
            "message": "上传成功"
        })
    except Exception as e:
        return fail_response(ErrorCode.INTERNAL_SERVER_ERROR, f"上传失败：{str(e)}")

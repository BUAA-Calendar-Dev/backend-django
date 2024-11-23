from datetime import datetime

from django.contrib.auth.context_processors import auth
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.core.files.storage import default_storage

from django.contrib.auth import authenticate, login, logout

from application.users.api.auth import jwt_auth, generate_token, generate_refresh_token
from application.users.api.email import varify_captcha
from application.users.models import User
from application.utils.data_process import parse_data
from application.utils.response import *

name_not_allow = ['default', 'delete']


@response_wrapper
# @jwt_auth()
@require_GET
def get_now_user_info(request: HttpRequest):
    post_data = parse_data(request)
    user = request.user

    info = _get_user_info(user.id)
    if user is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在用户")
    return success_response({
        "users": _get_user_info(user.id)
    })


@response_wrapper
# @jwt_auth()
@require_GET
def get_user_info(request: HttpRequest, id: int):
    post_data = parse_data(request)
    user = User.objects.get(id=id)

    info = _get_user_info(id)
    if user is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "不存在用户")
    return success_response({
        "users": _get_user_info(id)
    })


def _get_user_info(id: int):
    user = User.objects.get(id=id)

    if user is None:
        return None
    return {
        "username": user.username,
        # "avatar": default_storage.url(user.avatar),
        "email": user.email,
        "motto": user.motto,
        "gender": user.gender,
        "identity": user.identity,
    }


@response_wrapper
@require_POST
def user_login(request: HttpRequest):
    post_data = parse_data(request)
    print(f"post data is : {post_data}")
    username = post_data.get('username')
    password = post_data.get('password')

    # TODO：对于具体身份的区分
    authen = post_data.get('authen')

    # 使用Django的authenticate函数验证用户名和密码
    user = authenticate(username=username, password=password)
    print(f"login user is {user}")

    # 通过查询邮箱找到对应的用户
    if user is None and '@' in username:
        # 使用邮箱登录，查询email相等的用户
        tmp_user = User.objects.filter(email=username).first()
        if tmp_user is None:
            return fail_response(ErrorCode.CANNOT_LOGIN_ERROR, "用户名或邮箱不存在！")
        username = tmp_user.username
        user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)

        request.session['is_login'] = True
        request.session['user_id'] = user.id
        request.session['username'] = user.username

        return success_response({
            "message": "登录成功",
            "username": user.username,
            "user_id": user.id,
            "token": generate_token(user),

        })
    elif User.objects.filter(username=username).exists():
        # 密码错误
        return fail_response(ErrorCode.CANNOT_LOGIN_ERROR, "密码错误！")
    else:
        # 登录失败
        return fail_response(ErrorCode.CANNOT_LOGIN_ERROR, "用户名或邮箱不存在！")


@response_wrapper
@require_GET
def user_logout(request):
    request.session.pop('is_login', None)
    request.session.pop('username', None)
    request.session.pop('user_id', None)
    logout(request)

    return success_response({
        "message": "退出成功"
    })


# 用户注册
@response_wrapper
@require_POST
def user_register(request: HttpRequest):
    if request.session.get('is_login', None):
        return success_response({
            "message": "已经登录"
        })
    post_data = parse_data(request)
    username = post_data.get('username')
    password = post_data.get('password')
    email = post_data.get('email')
    # TODO：对于邮箱发送验证码的支持
    # captcha = request.GET('captcha')

    # 检查是否有字段为空
    if username is None or password is None or email is None:
        return fail_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '内容未填写完整')

    # 检查用户名是否已存在
    if User.objects.filter(username=username).exists():
        print('用户名已存在')
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '用户名已存在')
    if username in name_not_allow:
        print('非法取名')
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '非法取名')
    if User.objects.filter(email=email).exists():
        print("邮箱已注册")
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "邮箱已注册")
    if password == '':
        print("密码不能为空")
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "密码不能为空")
    # 验证验证码
    # if not varify_captcha(email, captcha):
    #     return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "验证码错误")

    # 创建新用户
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password)
    user.save()

    return success_response({
        "message": "注册成功"
    })


# 修改密码
@response_wrapper
@require_POST
def change_password(request: HttpRequest):
    user = request.user

    post_data = parse_data(request)
    old_password = post_data.get('old_password')
    new_password = post_data.get('new_password')

    # 使用Django的authenticate函数验证用户名和密码
    user = authenticate(username=user.username, password=old_password)
    if user is not None:
        # 修改密码
        user.password = make_password(new_password)
        user.save()
        return success_response({'message': '密码修改成功'})
    else:
        # 登录失败
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "原密码错误")


# 忘记密码：修改密码的翻版
# TODO：对邮件的支持
@response_wrapper
@require_POST
def forget_password(request: HttpRequest):
    post_data = parse_data(request)
    email = post_data.get('email')
    captcha = post_data.get('captcha')
    new_password = post_data.get('password')

    user = User.objects.filter(email=email).first()
    if user is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "邮箱未注册")
    if varify_captcha(email, captcha):
        user.password = make_password(new_password)
        user.save()
        return success_response({"message": "验证码正确，密码已修改"})
    else:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "验证码错误")

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth import authenticate, login, logout

from application.users.api.auth import jwt_auth, generate_token
from application.users.api.email import varify_captcha
from application.users.models import User
from application.utils.data_process import parse_request
from application.utils.response import *
from application.users.models.user import default_preference

name_not_allow = ['default', 'delete']


@response_wrapper
@require_POST
def user_login(request: HttpRequest):
    request_data = parse_request(request)
    username = request_data.get('username')
    password = request_data.get('password')
    auth = request_data.get('authen')

    # 使用Django的authenticate函数验证用户名和密码
    user = authenticate(username=username, password=password)
    print(f"[debug]login user is {user} {username} {password}")

    # 通过查询邮箱找到对应的用户
    if user is None and '@' in username:
        # 使用邮箱登录，查询email相等的用户
        tmp_user = User.objects.filter(email=username).first()

        if tmp_user is None:
            return response({
                "code": StatusCode.LOGIN_ACCOUNT_ERROR,
                "message": "用户名或邮箱不存在"
            })

        username = tmp_user.username
        user = authenticate(username=username, password=password)
        print(f"[debug]login user is {user}")

    # 成功进行登录
    if user is not None:
        if auth != user.identity:
            # 登录权限错误
            return response({
                "code": StatusCode.LOGIN_PERMISSION_ERROR,
                "message": "登录权限错误"
            })
        # 一切正常
        login(request, user)
        # 登记相关的session
        request.session['is_login'] = True
        request.session['user_id'] = user.id
        request.session['username'] = user.username

        return response({
            "message": "登录成功",
            "username": user.username,
            "user_id": user.id,
            "token": generate_token(user)
        })
    elif User.objects.filter(username=username).exists():
        # 密码错误
        return response({
            "code": StatusCode.LOGIN_ACCOUNT_ERROR,
            "message": "密码错误"
        })
    else:
        # 登录失败
        return response({
            "code": StatusCode.LOGIN_ACCOUNT_ERROR,
            "message": "登录错误"
        })


@response_wrapper
@require_GET
def user_logout(request):
    # 处理相关的session
    request.session.pop('is_login', None)
    request.session.pop('username', None)
    request.session.pop('user_id', None)
    logout(request)

    return response({
        "message": "退出成功"
    })


def _check_register_status(username, password, email=''):
    # 检查是否有字段为空
    if username is None or password is None:
        return fail_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '[register]内容未填写完整')

    # 检查用户名是否已存在
    if User.objects.filter(username=username).exists():
        return StatusCode.REGISTER_NAME_ERROR

    if username in name_not_allow:
        return StatusCode.OTHER_ERROR
    if email and User.objects.filter(email=email).exists():
        return StatusCode.OTHER_ERROR
    if password == '':
        return StatusCode.OTHER_ERROR
    return StatusCode.SUCCESS


# 用户注册
@response_wrapper
@require_POST
def user_register(request: HttpRequest):
    if request.session.get('is_login', None):
        if request.user is not AnonymousUser:
            print(f"[debug] login user is AnonymousUser")
        else:
            print(f"[debug]已经登录")
            return response({
                "message": "已经登录"
            })

    request_data = parse_request(request)
    username = request_data.get('username', None)
    password = request_data.get('password', '')
    # 可选信息
    email = request_data.get('email', '')
    print(f"[debug]email is {email}")
    phone = request_data.get('phone', None)
    # TODO：邀请码目前的用处不大
    join_code = request_data.get('joincode', None)

    check_code = _check_register_status(username=username,
                                        password=password,
                                        email=email)
    print(f"[debug]check code is {check_code}")
    if check_code == StatusCode.SUCCESS:
        # 创建新用户
        user = User.objects.create_user(username=username, password=password, email=email)
        if phone is not None:
            user.phone = phone
        user.preference = default_preference
        user.save()
        print("[debug]注册成功")
        return response({
            "message": "注册成功"
        })
    else:
        return response({
            "code": check_code,
            "message": "登录失败"
        })


# 批量注册用户
@response_wrapper
@require_POST
def create_users(request: HttpRequest):
    request_data = parse_request(request)
    students = request_data.get('students')

    status_list = []
    for student_info in students:
        username = student_info['username']
        password = student_info['password']

        status = _check_register_status(username=username, password=password)
        status_list.append({"code": status})

        if status == StatusCode.SUCCESS:
            user = User.objects.create_user(username=username, password=password)
            user.save()
    return response({
        "status": status_list
    })


@response_wrapper
@jwt_auth()
@require_POST
def reset_password(request: HttpRequest, id: int):
    user = User.objects.filter(id=id).first()
    request_data = parse_request(request)
    password = request_data.get('password', '')

    if user is None:
        return fail_response(ErrorCode.USER_NOT_FOUND, "用户不存在")

    if password == '':
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "密码不能为空")

    user.password = make_password(password)
    user.save()

    return response({
        "message": f"成功修改{user.username}密码"
    })


# 修改密码
@response_wrapper
@jwt_auth()
@require_POST
def change_password(request: HttpRequest):
    user = request.user
    request_data = parse_request(request)
    old_password = request_data.get('old-password', '')
    new_password = request_data.get('new-password', '')

    # 验证用户名和密码
    user = authenticate(username=user.username, password=old_password)
    if user is not None:
        user.password = make_password(new_password)
        user.save()
        return response({
            "message": "密码修改成功"
        })
    # 验证失败
    return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "原密码错误")


# 忘记密码：修改密码的翻版
# TODO：对邮件的支持
@response_wrapper
@jwt_auth()
@require_POST
def forget_password(request: HttpRequest):
    request_data = parse_request(request)
    email = request_data.get('email')
    captcha = request_data.get('captcha')
    new_password = request_data.get('password')

    user = User.objects.filter(email=email).first()
    if user is None:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "邮箱未注册")
    if varify_captcha(email, captcha):
        user.password = make_password(new_password)
        user.save()
        return response({
            "message": "验证码正确，密码已修改"
        })
    else:
        return fail_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, "验证码错误")

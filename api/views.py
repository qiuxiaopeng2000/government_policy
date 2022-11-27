import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from api.models import Data, user_info_data
from django.core import serializers
from django.http import JsonResponse
from get_data.main import *
from .forms import follow_form, user_info_form, user_login_form, user_change_email_form
from .models import follow
# from rest_framework.authtoken.views import APIView, AuthTokenSerializer
# from rest_framework.authtoken.models import Token


@require_http_methods(["GET"])
def show_policy(request):
    response = {}
    try:
        city = request.GET.get('city')
        policys = Data.objects.filter(city=city)
        response['list'] = json.loads(serializers.serialize("json", policys))
        response['msg'] = '0'
        response['error_num'] = 0
    except Exception as e:
        response['signal'] = str(e)
        response['msg'] = '-1'
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def update_policy(request):
    response = {}
    try:
        city = request.GET.get('city')
        func = 'spider_' + str(city)
        cmd = "{}()".format(func)
        exec(cmd)
        # if city == 'anhui':
        #     spider_anhui()
        response['msg'] = '0'
        response['city'] = city
        response['error_num'] = 0
        response['cmd'] = cmd
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 0: 操作成功, 1: 密码不正确, 2: 用户不存在, 3: 用户已经存在, -1: 错误
@require_http_methods(["GET"])
def user_register(request):
    response = {}
    try:
        username = request.GET.get('username')
        password = request.GET.get('password')
        email = request.GET.get('email')
        if User.objects.filter(username=username).exists():
            response['signal'] = '用户名已被注册'
            response['msg'] = '3'
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            new_user_info_form = user_info_form()
            new_user_info_data = new_user_info_form.save(commit=False)
            new_user_info_data.user = user
            new_user_info_data.save()
            # token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            response['msg'] = '0'
            response['error_num'] = 0
            response['signal'] = '注册成功'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET"])
def user_login(request):
    response = {}
    try:
        new_user_login_form = user_login_form(data=request.GET)
        if new_user_login_form.is_valid():
            data = new_user_login_form.cleaned_data
            # 检验账号、密码是否正确
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                response['msg'] = '0'
                response['error_num'] = 0
                response['signal'] = '登录成功'
                response['list'] = user.username
            else:
                response['msg'] = '1'
                response['error_num'] = 1
                response['signal'] = '账号或密码输入有误。请重新输入!'
        else:
            response['msg'] = '-1'
            response['error_num'] = 1
            response['signal'] = '账号或密码格式不正确'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET"])
def user_logout(request):
    response = {}
    try:
        logout(request)
        response['msg'] = '0'
        response['error_num'] = 0
        response['signal'] = '退出成功！'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


# 0: 操作成功, 1: 密码不正确, 2: 用户不存在, 3: 用户以及存在, -1: 错误
@require_http_methods(["GET"])
def user_delete(request):
    response = {}
    try:
        # username = request.GET.get('username')
        username = request.user.username
        password = request.GET.get('password')
        user = User.objects.get(username=username)
        if user.password == password and request.user == user:
            logout(request)
            user.delete()
            response['msg'] = '0'
            response['error_num'] = 0
            response['signal'] = '删除成功!'
        else:
            response['msg'] = '1'
            response['error_num'] = 1
            response['signal'] = '你没有通过身份验证，你无权注销用户'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET"])
def user_change_password(request):
    response = {}
    try:
        # username = request.GET.get('username')
        username = request.user.username
        old_password = request.GET.get('old_password')
        new_password = request.GET.get('new_password')
        if not User.objects.filter(username=username).exists():
            response['msg'] = '2'
            response['signal'] = '用户不存在'
        else:
            user = User.objects.get(username=username)
            if request.user == user and check_password(old_password, user.password):
                user.password = make_password(new_password)
                user.save()
                login(request, user)
                response['msg'] = '0'
                response['error_num'] = 0
                response['signal'] = '修改成功！'
            else:
                response['msg'] = '1'
                response['error_num'] = 1
                response['signal'] = '密码不正确'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


# @login_required
@require_http_methods(["GET"])
def user_change_email(request):
    response = {}
    try:
        # username = request.GET.get('username')
        username = request.user.username
        email = request.GET.get('email')
        if not User.objects.filter(username=username).exists():
            response['msg'] = '2'
            response['signal'] = '用户不存在'
        else:
            user = User.objects.get(username=username)
            if request.user == user:
                user.email = email
                user.save()
                response['msg'] = '0'
                response['error_num'] = 0
                response['signal'] = '修改成功！'

            else:
                response['msg'] = '1'
                response['error_num'] = 1
                response['signal'] = '你无权修改该用户邮箱！'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET"])
def user_change_phone(request):
    response = {}
    try:
        # username = request.GET.get('username')
        username = request.user.username
        phone = request.GET.get('phone')
        if not User.objects.filter(username=username).exists():
            response['msg'] = '2'
            response['signal'] = '用户不存在'
        else:
            user = User.objects.get(username=username)
            if request.user == user:
                user_data = user_info_data.objects.get(user=user)
                user_data.phone = phone
                user_data.save()
                response['msg'] = '0'
                response['error_num'] = 0
                response['signal'] = '修改成功！'
            else:
                response['msg'] = '1'
                response['error_num'] = 1
                response['signal'] = '你无权修改该用户信息！'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET"])
def user_change_portrait(request):
    response = {}
    try:
        # username = request.GET.get('username')
        username = request.user.username
        # portrait = request.FILES.get('portrait')
        if not User.objects.filter(username=username).exists():
            response['msg'] = '2'
            response['signal'] = '用户不存在'
        else:
            user = User.objects.get(username=username)
            if request.user == user:
                user_info = request.FILES.get('portrait')
                user_data = user_info_data.objects.get(user=user)
                user_data.portrait = user_info
                user_data.save()
                response['msg'] = '0'
                response['error_num'] = 0
                response['signal'] = '%s修改成功！' % user_info

            else:
                response['msg'] = '1'
                response['error_num'] = 1
                response['signal'] = '你无权修改该用户信息！'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_user_info(request):
    response = {}
    try:
        # city = request.GET.get('city')
        # username = request.GET.get('username')
        username = request.user.username
        user = User.objects.get(username=username)
        user_data = user_info_data.objects.get(user=user)
        lists = {'username': username, 'email': user.email, 'portrait': user_data.get_portrait_url(), 'phone': user_data.get_phone()}
        response['list'] = lists
        response['msg'] = '0'
        response['signal'] = '查询成功！'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET"])
def follow_city_category(request):
    response = {}
    try:
        city = request.GET.get('city')
        category = request.GET.get('category')
        # username = request.GET.get('username')
        username = request.user.username
        follow_other = follow_form().save(commit=False)
        follow_other.follow_city = city
        follow_other.follow_category = category
        follow_other.username = username
        follow_other.save()
        response['msg'] = '0'
        response['signal'] = '关注成功！'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_follow(request):
    response = {}
    try:
        # city = request.GET.get('city')
        # username = request.GET.get('username')
        username = request.user.username
        follows = follow.objects.filter(username=username)
        response['list'] = json.loads(serializers.serialize("json", follows))
        response['msg'] = '0'
        response['signal'] = '查询成功！'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET"])
def delete_follow(request):
    response = {}
    try:
        city = request.GET.get('city')
        category = request.GET.get('category')
        # username = request.GET.get('username')

        username = request.user.username
        follows = follow.objects.filter(username=username, follow_city=city)
        if city is not None:
            follows.follow_city = ""
        if category is not None:
            follows.follow_category = ""
        # follows.delete()
        response['list'] = json.loads(serializers.serialize("json", follows))
        response['msg'] = '0'
        response['signal'] = '删除成功！'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)

#
# @require_http_methods(["GET"])
# def search_fans_username(request):
#     response = {}
#     try:
#         city = request.GET.get('city')
#         category = request.GET.get('category')
#         # username = request.GET.get('username')
#         username = request.user.username
#         follows = follow.objects.filter(username=username)
#         response['list'] = json.loads(serializers.serialize("json", follows))
#         response['msg'] = '0'
#         response['signal'] = '查询成功！'
#     except Exception as e:
#         response['msg'] = '-1'
#         response['error_num'] = 1
#         response['error'] = str(e)
#     return JsonResponse(response)

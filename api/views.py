import json
from django.views.decorators.http import require_http_methods
from api.models import Data
from django.core import serializers
from django.http import JsonResponse
from get_data.main import *
from .forms import user_register_form, follow_form
from .models import user_info_data, follow


@require_http_methods(["GET"])
def show_policy(request):
    response = {}
    try:
        city = request.GET.get('city')
        policys = Data.objects.filter(city=city)
        response['list'] = json.loads(serializers.serialize("json", policys))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
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
        response['msg'] = 'success'
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
        if user_info_data.objects.filter(username=username).exists():
            response['msg'] = '3'
        else:
            user_register_info = user_register_form()
            user_info = user_register_info.save(commit=False)
            user_info.username = username
            user_info.password = password
            user_info.save()
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
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = user_info_data.objects.get(username=username)
        if user.password == password:
            response['msg'] = '0'
            response['error_num'] = 0
            response['signal'] = '登陆成功'
        else:
            response['msg'] = '1'
            response['error_num'] = 1
            response['signal'] = '密码不正确'
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
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = user_info_data.objects.get(username=username)
        if user.password == password:
            user.delete()
            response['msg'] = '0'
            response['error_num'] = 0
            response['signal'] = '删除成功!'
        else:
            response['msg'] = '1'
            response['error_num'] = 1
            response['signal'] = '密码不正确'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET"])
def user_change_password(request):
    response = {}
    try:
        username = request.GET.get('username')
        old_password = request.GET.get('old_password')
        new_password = request.GET.get('new_password')
        if not user_info_data.objects.filter(username=username).exists():
            response['msg'] = '2'
            response['signal'] = '用户不存在'
        else:
            user = user_info_data.objects.get(username=username)
            if user.password == old_password:
                user.password = new_password
                user.save()
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


@require_http_methods(["GET"])
def follow_city(request):
    response = {}
    try:
        city = request.GET.get('city')
        username = request.GET.get('username')
        follow_other = follow_form().save(commit=False)
        follow_other.follow_city = city
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
        username = request.GET.get('username')
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
        username = request.GET.get('username')
        follows = follow.objects.filter(username=username, follow_city=city)
        follows.delete()
        response['list'] = json.loads(serializers.serialize("json", follows))
        response['msg'] = '0'
        response['signal'] = '删除成功！'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)

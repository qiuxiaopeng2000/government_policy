import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from api.models import Data, user_info_data, PolicyUrl
from django.core import serializers
from django.http import JsonResponse
from get_data.main import *
from .forms import follow_form, user_info_form, user_login_form, user_change_email_form
from .models import follow
# from rest_framework.authtoken.views import APIView, AuthTokenSerializer
# from rest_framework.authtoken.models import Token
from .utils.MsmService import sendMsm


# @require_http_methods(["GET"])
# def show_policy(request):
#     response = {}
#     try:
#         city = request.GET.get('city')
#         policys = PolicyUrl.objects.filter(city=city)
#         response['list'] = json.loads(serializers.serialize("json", policys))
#         response['msg'] = '0'
#         response['error_num'] = 0
#     except Exception as e:
#         response['signal'] = str(e)
#         response['msg'] = '-1'
#         response['error_num'] = 1
#     return JsonResponse(response)

@require_http_methods(["GET"])
def show_policy(request):
    response = {}
    try:
        city = request.GET.get('city')
        category = request.GET.get('category')
        #print("12321213" + category)
        policys = Data.objects.filter(Q(city=city) | Q(category=category))
        #print(len(policys))
        #response['list'] = json.loads(serializers.serialize("json", policys))
        List = []
        for policy in policys:
            policyData = {}
            policyData['title'] = policy.title
            policyData['city'] = policy.city
            policyData['url'] = policy.url
            policyData['id'] = policy.id
            policyData['category'] = policy.category
            policyData['create_time'] = policy.create_time
            List.append(policyData)
        response['list'] = List
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_policy_detail(request):
    response = {}
    try:
        policy_pk = request.GET.get('pk')
        # policy_pk = str(policy_pk)
        policy = Data.objects.filter(id=policy_pk)
        response['list'] = json.loads(serializers.serialize("json", policy))
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
            # new_user_info_form = user_info_form()
            # new_user_info_data = new_user_info_form.save(commit=False)
            # new_user_info_data.user = user
            print('?????')
            request.session["info"] = {'username': username}
            if user_info_data.objects.filter(user_id=user.id).exists():
                get_user_info = user_info_data.objects.get(user_id=user.id)
            else:
                get_user_info = user_info_data.objects.create(user=user)
            # new_user_info_data = user_info_data.objects.create(user=user)
            print('+++++')
            # new_user_info_data.save()
            # token, created = Token.objects.get_or_create(user=user)
            #login(request, user)
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
            username = data['username']
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                response['msg'] = '0'
                response['error_num'] = 0
                response['signal'] = '登录成功'
                response['list'] = user.username
                request.session["info"] = {'username': username}
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
    # return render(request, 'login/login.html', response)
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
        # old_password = request.GET.get('old_password')
        password = request.GET.get('password')
        if not User.objects.filter(username=username).exists():
            response['msg'] = '2'
            response['signal'] = '用户不存在'
        else:
            user = User.objects.get(username=username)
            if request.user == user:
                user.password = make_password(password)
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
        # print('??????')
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
        # print('?????', username)
        phone = request.GET.get('phone')
        if not User.objects.filter(username=username).exists():
            response['msg'] = '2'
            response['signal'] = '用户不存在'
        else:
            user = User.objects.get(username=username)
            if request.user == user:
                # print('!!!!')
                user_data = user_info_data.objects.get(user=user)
                # print('!!!!')
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
        # username = request.user.username
        username = 'qxp1'
        portrait = request.FILES.get('portrait')
        print(portrait)
        if not User.objects.filter(username=username).exists():
            response['msg'] = '2'
            response['signal'] = '用户不存在'
        else:
            user = User.objects.get(username=username)
            if request.user == user:
                user_info = request.FILES.get('portrait')
                user_data = user_info_data.objects.get(user=user)
                user_data.portrait = user_info
                # user_data.save()
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


# @require_http_methods(["GET"])
# def follow_city_category(request):
#     response = {}
#     try:
#         city = request.GET.get('city')
#         category = request.GET.get('category')
#         # username = request.GET.get('username')
#         username = request.user.username
#         follow_other = follow_form().save(commit=False)
#         follow_other.follow_city = city
#         follow_other.follow_category = category
#         follow_other.username = username
#         follow_other.save()
#         response['msg'] = '0'
#         response['signal'] = '关注成功！'
#     except Exception as e:
#         response['msg'] = '-1'
#         response['error_num'] = 1
#         response['error'] = str(e)
#     return JsonResponse(response)

@require_http_methods(["GET"])
def follow_city(request):
    response = {}
    try:
        city = request.GET.get('city')
        username = request.session.get('info').get('username')
        print("1232132132" + username)
        follow_other = follow_form().save(commit=False)
        follow_other.follow_city = city
        follow_other.username = username
        print(follow_other.username)
        follow_other.last_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        print("ejhrehrer")
        follow_other.save()
        print("12345")
        response['msg'] = '0'
        response['signal'] = '关注成功！'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


def policy(request):
    policy_pk = request.GET.get('pk')
    # policy_pk = str(policy_pk)
    policy = Data.objects.filter(id=policy_pk).first()
    return render(request, 'templatesTest/policy.html',
                  {'policy':policy})


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
        print(username)
        follows = follow.objects.filter(username=username, follow_city=city)
        for item in follows:
            if city is not None:
                item.follow_city = None
        # follows.save()
        follow2 = follow.objects.filter(username=username, follow_category=category)
        for item in follow2:
            if category is not None:
                item.follow_category = None
        # follow2.save()
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


# 获取未更新的信息条数
@require_http_methods(["GET"])
def getNumOfUnupdate(request):
    # request.session.get("info").get("username")
    username = 'qqt'
    update_time = follow.objects.filter(username=username).first().last_time
    # print(update_time)
    followArray = follow.objects.filter(username=username).all()
    followCityArray = []
    followCategoryArray = []
    for followItem in followArray:
        if not followItem.follow_city == '':
            followCityArray.append(followItem.follow_city)
        else:
            followCategoryArray.append(followItem.follow_category)
    dataCount = Data.objects.filter(Q(create_time__gte=update_time),Q(city__in=followCityArray) | Q(category__in=followCategoryArray)).count()
    # print(dataCount)
    return JsonResponse({"status":True,"numOfMessage": dataCount})


# 获取未更新的data数据并刷新更新时间
@require_http_methods(["GET"])
def getUnUpdateInfo(request):
    username = 'qqt'
    update_time = follow.objects.filter(username=username).first().last_time
    # print(update_time)
    followArray = follow.objects.filter(username=username).all()
    followCityArray = []
    followCategoryArray = []
    for followItem in followArray:
        if not followItem.follow_city == '':
            followCityArray.append(followItem.follow_city)
        else:
            followCategoryArray.append(followItem.follow_category)
    dataArray = Data.objects.filter(Q(create_time__gte=update_time),Q(city__in=followCityArray) | Q(category__in=followCategoryArray)).order_by('-create_time')
    print(type(dataArray))
    returnDataArray = serializers.serialize("json",dataArray,fields=('title','url','city','category','create_time'))
    follow.objects.filter(username=username).update(last_time = time.strftime('%Y-%m-%d', time.localtime(time.time())))
    return JsonResponse({'status':True,'dataArray':returnDataArray})


@require_http_methods(["GET"])
def test(request):
    return render(request, 'test.html')


def newData(request):
    QuerySet = {'title':'安徽省人民政府关于印发安徽省政府投资管理办法的通知','city':'安徽省','url':'https://www.ah.gov.cn/public/1681/554182711.html','category':'疫情'}
    Data.objects.create(**QuerySet)
    return JsonResponse({"status": "true"})


def SmsTest(request):
    sendMsm("18390956471")
    return JsonResponse({"status": True})

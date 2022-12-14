import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from api.models import Data, user_info_data, PolicyUrl, follow
from django.core import serializers
from django.http import JsonResponse
from get_data.main import *
from .forms import follow_form, user_info_form, user_login_form, user_change_email_form
# from .models import follow, user_info_data
# from rest_framework.authtoken.views import APIView, AuthTokenSerializer
# from rest_framework.authtoken.models import Token
from .utils.MsmService import sendMsm
import datetime
# from get_data.anhui.xuancheng.xuancheng_policy import data


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
        if city is not None and category is not None:
            policys = Data.objects.filter(Q(city=city) & Q(category=category)).order_by('-create_time')
        else:
            policys = Data.objects.filter(Q(city=city) | Q(category=category)).order_by('-create_time')
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
        lens = len(List)
        response['list'] = List
        response['count'] = lens
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_all_policy(request):
    response = {}
    try:
        policys = Data.objects.all().order_by('-create_time')
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
        lens = len(List)
        # print('lens: ' + str(lens))
        response['list'] = List
        response['count'] = lens
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
        # print("+++++++++")

        city = request.GET.get('city')
        print('city: ' + city)
        func = 'spider_' + str(city)
        cmd = "{}()".format(func)
        exec(cmd)
        # print(str(data))
        # print("dsafksafa")
        # QuerySet = {'title': '???????????????????????????????????????????????????????????????????????????', 'city': '?????????',
        #             'url': 'https://www.ah.gov.cn/public/1681/554182711.html', 'category': '??????'}
        # Data.objects.create(**QuerySet)
        # print("kjsanfksahsa")
        # if city == 'anhui':
        #     spider_anhui()
        response['msg'] = '0'
        response['city'] = city
        response['error_num'] = 0
        response['cmd'] = cmd
    except Exception as e:
        # print("----------")
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 0: ????????????, 1: ???????????????, 2: ???????????????, 3: ??????????????????, -1: ??????
@require_http_methods(["GET"])
def user_register(request):
    response = {}
    try:
        username = request.GET.get('username')
        password = request.GET.get('password')
        email = request.GET.get('email')
        # email = '2621099562@qq.com'
        # if email is None:
        #     email = '2621099562@qq.com'
        if User.objects.filter(username=username).exists():
            response['signal'] = '?????????????????????'
            response['msg'] = '3'
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            # new_user_info_form = user_info_form()
            # new_user_info_data = new_user_info_form.save(commit=False)
            # new_user_info_data.user = user
            # user = User.objects.get(id=user.id)
            print('?????')
            request.session["info"] = {'username': username}
            print('------')
            if user_info_data.objects.filter(user_id=user.id).exists():
                get_user_info = user_info_data.objects.get(user_id=user.id)
            else:
                get_user_info = user_info_data.objects.create(user=user, last_time="2022-10-17")
                # get_user_info.last_time = datetime.datetime.now()
            # new_user_info_data = user_info_data.objects.create(user=user)
            print('+++++')
            # new_user_info_data.save()
            # token, created = Token.objects.get_or_create(user=user)
            # login(request, user)
            response['msg'] = '0'
            response['error_num'] = 0
            response['signal'] = '????????????'
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
            # ?????????????????????????????????
            username = data['username']
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                response['msg'] = '0'
                response['error_num'] = 0
                response['signal'] = '????????????'
                response['list'] = user.username
                request.session["info"] = {'username': username}
            else:
                response['msg'] = '1'
                response['error_num'] = 1
                response['signal'] = '?????????????????????????????????????????????!'
        else:
            response['msg'] = '-1'
            response['error_num'] = 1
            response['signal'] = '??????????????????????????????'
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
        response['signal'] = '???????????????'
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


# 0: ????????????, 1: ???????????????, 2: ???????????????, 3: ??????????????????, -1: ??????
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
            response['signal'] = '????????????!'
        else:
            response['msg'] = '1'
            response['error_num'] = 1
            response['signal'] = '???????????????????????????????????????????????????'
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
            response['signal'] = '???????????????'
        else:
            user = User.objects.get(username=username)
            if request.user == user:
                user.password = make_password(password)
                user.save()
                login(request, user)
                response['msg'] = '0'
                response['error_num'] = 0
                response['signal'] = '???????????????'
            else:
                response['msg'] = '1'
                response['error_num'] = 1
                response['signal'] = '???????????????'
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
        username = request.session.get('info').get('username')
        email = request.GET.get('email')
        # print('??????')
        if not User.objects.filter(username=username).exists():
            response['msg'] = '2'
            response['signal'] = '???????????????'
        else:
            user = User.objects.get(username=username)
            user.email = email
            user.save()
            response['msg'] = '0'
            response['error_num'] = 0
            response['signal'] = '???????????????'


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
        username = request.session.get('info').get('username')
        # print('?????', username)
        phone = request.GET.get('phone')
        if not User.objects.filter(username=username).exists():
            response['msg'] = '2'
            response['signal'] = '???????????????'
        else:
            user = User.objects.get(username=username)
            # print('!!!!')
            user_data = user_info_data.objects.get(user=user)
                # print('!!!!')
            user_data.phone = phone
            user_data.save()
            response['msg'] = '0'
            response['error_num'] = 0
            response['signal'] = '???????????????'

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
        username = request.session.get('info').get('username')
        portrait = request.FILES.get('portrait')
        print(portrait)
        if not User.objects.filter(username=username).exists():
            response['msg'] = '2'
            response['signal'] = '???????????????'
        else:
            user = User.objects.get(username=username)
            user_info = request.FILES.get('portrait')
            user_data = user_info_data.objects.get(user=user)
            user_data.portrait = user_info
            # user_data.save()
            response['msg'] = '0'
            response['error_num'] = 0
            response['signal'] = '%s???????????????' % user_info


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
        response['signal'] = '???????????????'
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
#         response['signal'] = '???????????????'
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
        if request.session.get("info") is None:
            return JsonResponse({'signal': '????????????', 'msg': 0},)
        username = request.session.get('info').get('username')
        # print("1232132132" + username)
        follow_other = follow_form().save(commit=False)
        follow_other.follow_city = city
        follow_other.username = username
        # print(follow_other.username)
        follow_other.last_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # print("ejhrehrer")
        follow_other.save()
        print("12345")
        response['msg'] = '0'
        response['signal'] = '???????????????'
        response['city_id'] = '%d' % follow_other.id
    except Exception as e:
        response['msg'] = '-1'
        response['error_num'] = 1
        response['error'] = str(e)
    return JsonResponse(response)


@require_http_methods(["GET"])
def follow_category(request):
    response = {}
    try:
        category = request.GET.get('category')
        if request.session.get("info") is None:
            return JsonResponse({'signal': '????????????', 'msg': 0},)
        username = request.session.get('info').get('username')
        # print("1232132132" + username)
        follow_other = follow_form().save(commit=False)
        follow_other.follow_category = category
        follow_other.username = username
        # print(follow_other.username)
        follow_other.last_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # print("ejhrehrer")
        follow_other.save()
        print("12345")
        response['msg'] = '0'
        response['signal'] = '???????????????'
        response['category_id'] = '%d' % follow_other.id
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
                  {'policy': policy})


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
        response['signal'] = '???????????????'
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
        # username = request.user.username
        username = request.session.get('info').get('username')
        # print(username)
        if city is not None:
            follows = follow.objects.filter(username=username, follow_city=city)
            follows.delete()
        # for item in follows:
        #     if city is not None:
        #
                # item.objects.update(follow_city='')
                # print('item.follow_city ' + str(item.follow_city))
        # follows.save()
        if category is not None:
            follow2 = follow.objects.filter(username=username, follow_category=category)
            follow2.delete()
        # for item in follow2:
        #     if category is not None:
        #         # item.objects.update(follow_category='')

        # follow2.save()
        # follows.save()
        # follows.delete()
        response['list'] = json.loads(serializers.serialize("json", follows))
        response['msg'] = '0'
        response['signal'] = '???????????????'
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
#         response['signal'] = '???????????????'
#     except Exception as e:
#         response['msg'] = '-1'
#         response['error_num'] = 1
#         response['error'] = str(e)
#     return JsonResponse(response)


# ??????????????????????????????

@require_http_methods(["GET"])
def test(request):
    return render(request, 'test.html')


def newData(request):
    # QuerySet = {'title':'????????????????????????????????????????????????????????????????????????????????????????????????','city':'?????????','url':'http://www.xuancheng.gov.cn/Xzgfxwjk/show/2545407.html','category':'????????????', 'create_time': '2022-11-08'}
    # Data.objects.create(**QuerySet)
    QuerySet = {'title': '?????????????????????????????????????????????????????????????????????', 'city': '?????????',
                'url': 'http://www.xuancheng.gov.cn/Xzgfxwjk/show/2529725.html', 'category': '????????????',
                'create_time': '2022-10-18'}
    print("+++++++++++")
    Data.objects.create(**QuerySet)
    print("1sygdiuwjcis")

    return JsonResponse({"status": "true"})


def newDataTest(title, url, create_time, city, category, head,body):
    Data.objects.create(title=title, url=url, create_time=create_time, city=city, category=category, head=head,
                        body=body)
    print("+++++++")
    return JsonResponse({"status": "true"})


@require_http_methods(["GET"])
def getNumOfUnupdate(request):
    username = request.session.get("info").get("username")
    user = User.objects.filter(username=username).first()
    update_time = user_info_data.objects.filter(user=user).first().last_time
    # print(update_time)
    followArray = follow.objects.filter(username=username).all()
    followCityArray = []
    followCategoryArray = []
    for followItem in followArray:
        if followItem.follow_city is not None:
            followCityArray.append(followItem.follow_city)
        else:
            followCategoryArray.append(followItem.follow_category)
    print("followCity" + str(followCityArray))
    print("followCategory" + str(followCategoryArray))
    dataCount = Data.objects.filter(Q(create_time__gte=update_time),
                                    Q(city__in=followCityArray) | Q(category__in=followCategoryArray)).count()
    # print(dataCount)
    return JsonResponse({"status": True, "numOfMessage": dataCount})


# ??????????????????data???????????????????????????
@require_http_methods(["GET"])
def getUnUpdateInfo(request):
    username = request.session.get("info").get("username")
    print("+++++++" + username)
    user = User.objects.filter(username=username).first()
    update_time = user_info_data.objects.filter(user=user).first().last_time
    # update_time = follow.objects.filter(username=username).first().last_time
    # print(update_time)
    followArray = follow.objects.filter(username=username).all()
    print("followArray" + str(followArray))
    followCityArray = []
    followCategoryArray = []
    for followItem in followArray:
        if followItem.follow_city is not None:
            followCityArray.append(followItem.follow_city)
        else:
            followCategoryArray.append(followItem.follow_category)
    print("category" + str(followCategoryArray))
    dataArray = Data.objects.filter(Q(create_time__gte=update_time),
                                    Q(city__in=followCityArray) | Q(category__in=followCategoryArray)).order_by(
        '-create_time')
    dataArray1 = Data.objects.filter(Q(create_time__lt=update_time),
                                     Q(city__in=followCityArray) | Q(category__in=followCategoryArray)).order_by(
        '-create_time')
    for item in dataArray1:
        print(item.category)
    List = []
    ListRead = []
    for policy in dataArray:
        policyData = {}
        policyData['title'] = policy.title
        policyData['city'] = policy.city
        policyData['url'] = policy.url
        policyData['id'] = policy.id
        policyData['category'] = policy.category
        policyData['create_time'] = policy.create_time
        List.append(policyData)
    for policy in dataArray1:
        policyData = {}
        policyData['title'] = policy.title
        policyData['city'] = policy.city
        policyData['url'] = policy.url
        policyData['id'] = policy.id
        policyData['category'] = policy.category
        policyData['create_time'] = policy.create_time
        ListRead.append(policyData)
    # returnDataArray = serializers.serialize("json",dataArray,fields=('title','url','city','category','create_time'))
    user_info_data.objects.filter(user=user).update(last_time=time.strftime('%Y-%m-%d', time.localtime(time.time())))
    return JsonResponse({'status': True, 'dataArray': List, 'dataHaveRead': ListRead})


def SmsTest(request):
    sendMsm("18390956471")
    return JsonResponse({"status": True})

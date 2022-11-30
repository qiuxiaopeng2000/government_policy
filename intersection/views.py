from django.contrib.auth.models import User
from api.models import user_info_data, follow, Data
from django.shortcuts import render
from api.models import PolicyUrl

# Create your views here.
from intersection.forms import user_info_form


def all_policy_data(request):
    all_policy = PolicyUrl.objects.all()
    all_policy = all_policy[:10]
    context = {'all_policy': all_policy}

    return render(request, 'templatesTest/home.html', context)


def user_data_info(request):
    portrait_new = request.FILES.get('portrait')
    print(request.user.id)
    user = User.objects.get(id=request.user.id)
    user_data = user_info_data.objects.get(user=user)
    if portrait_new is not None:
        user_data.portrait = portrait_new
        print('??????')
    username = user.username
    password = user.password
    email = user.email
    phone = user_data.phone
    portrait = user_data.portrait
    follows = follow.objects.filter(username=username)
    # user_data.save()
    context = {
        'username': username,
        'password': password,
        'email': email,
        'phone': phone,
        'portrait': portrait,
        'follows': follows,
    }
    return render(request, 'templatesTest/user.html', context)


def get_policy_detail(request, policy_id):
    policy = Data.objects.get(id=policy_id)
    context = {'policy': policy}
    return render(request, 'policy-detail.html', context)


def login(request):
    return render(request, 'templatesTest/login.html')


def register(request):
    return render(request, 'templatesTest/register.html')


def change_password(request):
    return render(request, 'templatesTest/change-password.html')


def home(request):
    username = request.session.get('info').get('username')
    dataList = Data.objects.all()
    return render(request, 'templatesTest/home.html', {
        'user_name': username,
        'dataList': dataList
    })


def policy(request):
    return render(request, 'templatesTest/policy.html')


def user(request):
    return render(request, 'templatesTest/user.html')
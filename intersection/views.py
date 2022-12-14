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
    category_list = ['金融保险', '财政税务', '发展改革', '文化旅游', '农林水利', '市场监管', '科技工信', '住房城建',
                     '医疗卫生', '其它']
    # print(request.user)
    username = request.session.get('info').get('username')
    user = User.objects.get(username=username)
    user_data = user_info_data.objects.get(user=user)
    if portrait_new is not None:
        user_data.portrait = portrait_new
        user_data.save()
        # print('??????')
    password = user.password
    email = user.email
    phone = user_data.phone
    portrait = user_data.portrait
    print(portrait, "++++++++")
    follows = follow.objects.filter(username=username)
    # print(username + '+++++' + str(len(follows)))
    # user_data.save()
    context = {
        'username': username,
        'password': password,
        'email': email,
        'phone': phone,
        'portrait': portrait,
        'follows': follows,
        'category_list': category_list,
    }
    return render(request, 'templatesTest/user.html', context)


def get_policy_detail(request, policy_id):
    category_list = ['金融保险', '财政税务', '发展改革', '文化旅游', '农林水利', '市场监管', '科技工信', '住房城建',
                     '医疗卫生', '其它']
    policy = Data.objects.get(id=policy_id)
    context = {'policy': policy,
               'category_list': category_list,
               }
    return render(request, 'templatesTest/policy.html', context)


def login(request):
    return render(request, 'templatesTest/login.html')


def register(request):
    return render(request, 'templatesTest/register.html')


def change_password(request):
    return render(request, 'templatesTest/change-password.html')


# def home(request):
#     username = request.session.get('info').get('username')
#     dataList = Data.objects.all()
#     return render(request, 'templatesTest/home.html', {
#         'user_name': username,
#         'dataList': dataList
#     })

def home(request):
    # dataList = Data.objects.all()
    # List = []
    category_list = ['金融保险', '财政税务', '发展改革', '文化旅游', '农林水利', '市场监管', '科技工信', '住房城建',
                     '医疗卫生', '其它']
    # for policy in dataList:
    #     policyData = {}
    #     policyData['title'] = policy.title
    #     policyData['city'] = policy.city
    #     policyData['url'] = policy.url
    #     policyData['id'] = policy.id
    #     policyData['category'] = policy.category
    #     policyData['create_time'] = policy.create_time
    #     List.append(policyData)
    pages = range(1, 6)
    if request.session.get("info"):
        username = request.session.get('info').get('username')
        return render(request, 'templatesTest/home.html', {
            'user_name': username,
            # 'dataList': List,
            'category_list': category_list,
            'pages': pages,
        })

    return render(request, 'templatesTest/home.html', {
        # 'dataList': List,
        'category_list': category_list,
        'pages': pages,
    })


def policy(request):
    return render(request, 'templatesTest/policy.html')


def user(request):
    return render(request, 'templatesTest/user.html')


def category(request):
    category_list = ['金融保险', '财政税务', '发展改革', '文化旅游', '农林水利', '市场监管', '科技工信', '住房城建', '医疗卫生', '其它']
    context = {'category_list': category_list}
    # print(len(category_list))
    return render(request, 'policy-tablist.html', context)

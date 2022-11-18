import json
from django.views.decorators.http import require_http_methods
from api.models import Data
from django.core import serializers
from django.http import JsonResponse
from get_data.main import *


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




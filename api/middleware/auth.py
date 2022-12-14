from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect
# class M1(MiddlewareMixin):
#     #如果process_request没有返回值或者返回none，可进入M2，否则直接M1结束（链状结构）
#     def process_request(self,request):
#         print("M1进来了")
#         return HttpResponse("无权访问")
#     def process_response(self,request,response):#该方法必须return response
#         print("M1出去")
#         return response
# class M2(MiddlewareMixin):
#     def process_request(self,request):
#         print("M2进来")
#     def process_response(self,request,response):
#         print("M2出去")
#         return response


class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        #去除那些不需要登录的url
        if request.path_info in ["/api/user_login","/api/user_register","/intersection/login/","/api/policy/","/api/show_policy","/intersection/register/","/media/v3.mp4","/media/navbar6.ico","/intersection/home/","/api/follow_city"]:
            return
        #1、读取当前访问的用户的session信息,如果读到，说明已登录过
        info_dict = request.session.get("info")
       # print(info_dict)
        if info_dict:
            return
        #2、如果未能读到，则返回未登录，回到登录页面
        return redirect("/intersection/login/")
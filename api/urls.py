from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url("show_policy$", views.show_policy, name='show_policy'),
    url("update_policy$", views.update_policy, name='update_policy'),
    url("user_register$", views.user_register, name='user_register'),
    url("user_login$", views.user_login, name='user_login'),
    url("user_change_password$", views.user_change_password, name='user_change_password'),
    url("user_delete$", views.user_delete, name='user_delete'),
    url("follow_city$", views.follow_city, name='follow_city'),
    url("show_follow$", views.show_follow, name='show_follow'),
    url("delete_follow$", views.delete_follow, name='delete_follow'),
    url("user_logout$", views.user_logout, name='user_logout'),
    url("user_change_email$", views.user_change_email, name='user_change_email'),
    url("user_change_portrait$", views.user_change_portrait, name='user_change_portrait'),
    url("show_user_info$", views.show_user_info, name='show_user_info'),
]

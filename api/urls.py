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
]

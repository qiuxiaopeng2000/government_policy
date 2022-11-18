from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url("show_policy$", views.show_policy, name='show_policy'),
    url("update_policy$", views.update_policy, name='update_policy'),
]
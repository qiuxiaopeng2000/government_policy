from django.urls import path
from . import views

app_name = 'intersection'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('change-password/', views.change_password, name='change-password'),
    path('home/', views.home, name='home'),
    path('policy/', views.policy, name='policy'),
    path('user/', views.user_data_info, name='user'),
    path('all-policy-data/', views.all_policy_data, name='all_policy_data'),
    path('user-data-info/', views.user_data_info, name='user_data_info'),
    path('policy-detail/', views.get_policy_detail, name='get_policy_detail'),
]

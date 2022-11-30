"""government URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from intersection.views import login
from django.views.static import serve
from .settings import MEDIA_ROOT

# from api.views import user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('', login, name='login'),
    path('intersection/', include("intersection.urls")),
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
]

# 主路由中：显性告诉django绑定media_url和media_root
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

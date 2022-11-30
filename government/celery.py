# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from government import settings
# 指定Django默认配置文件、这里我们把Celery相关配置文件放在Django项目的settings.py里面
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'government.settings')

# 创建Celery实例；这里建议指定broker、不指定broker容易出现错误
app = Celery('government_policy', broker='redis://127.0.0.1:6379/0')

# 指定从django的settings.py里读取celery配置
app.config_from_object('django.conf:settings')

# 自动从所有已注册的django app中加载任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# 用于测试的异步任务
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
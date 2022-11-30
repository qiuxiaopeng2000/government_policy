
from government.celery import app
from celery import shared_task
from .utils import MsmService,MailService
import time

@shared_task
def mul(x, y):
    print('发生耗时操作...')
    time.sleep(10) # 模拟耗时操作
    return x * y
@shared_task
def send_sms(phoneNum):
    MsmService.sendMsm(phoneNum)

@shared_task
def send_mail(subject,to_email,message):
    MailService.own_send_email(subject,to_email,message)
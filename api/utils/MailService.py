from government import settings
from django.core import mail


def own_send_email(subject,to_email,message):
    #subject = 'C语言中文网链接'  # 主题
    from_email = settings.EMAIL_HOST_USER  # 发件人，在settings.py中已经配置
    #to_email = '3230822899@qq.com'  # 邮件接收者列表
    # 发送的消息
    #message = 'c语言中文网欢迎你点击登录 http://c.biancheng.net/'  # 发送普通的消息使用的时候message
    # meg_html = '<a href="http://www.baidu.com">点击跳转</a>'  # 发送的是一个html消息 需要指定
    mail.send_mail(subject, message, from_email, [to_email])
    return True
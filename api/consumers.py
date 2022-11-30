import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save,post_save
from api import models
from government import settings
from django.core import mail
from django.core import serializers
from .utils.MsmService import sendMsm
from .utils.utilsReturnData import follow_users
from .tasks import send_sms,send_mail
map = {}
@receiver(post_save, sender=models.user_info_data)
def myhandler(sender, instance, **kwargs):
        #print(map['qqt'])
        print(type(instance))
        row_dict = {
            'username':instance.username,
            'id':instance.id
        }

        map['qqt'].send(json.dumps(row_dict))

@receiver(post_save, sender=models.Data)
def myhandler(sender, instance, **kwargs):
        #print(map['qqt'])
        print("?????????????/")
        userNameArray = follow_users(instance.city,instance.category)
        print(len(userNameArray))
        row_dict = {
            # 'username':instance.username,
            # 'id':instance.id
            'title': instance.title,
            'city': instance.city,
            'url': instance.url,
            'category':instance.category
        }
        for username in userNameArray:
            print(username)
            user = User.objects.get(username=username)
            user_data = models.user_info_data.objects.filter(user=user).first()
            #sendMsm(user.phone)
            if not user_data.phone == '':
                send_sms.delay(str(user_data.phone))
            if not user.email == '':
                if not row_dict.get("city"):
                #send_mail('您关注的城市' + row_dict.get('city') + '有政策更新', user.email,row_dict.get('title') + row_dict.get('url')).delay()
                    send_mail.delay('您关注的城市' + row_dict.get('city') + '有政策更新', user.email,row_dict.get('title') + row_dict.get('url'))
                if not row_dict.get("category"):
                #send_mail('您关注的标签' + row_dict.get('category') + '有政策更新', user.email,row_dict.get('title') + row_dict.get('url')).delay()
                    send_mail.delay('您关注的标签' + row_dict.get('category') + '有政策更新', user.email,row_dict.get('title') + row_dict.get('url'))
                else:
                    send_mail.delay('您关注的城市' + row_dict.get('city') + '和标签' + row_dict.get('category') +  '有政策更新', user.email ,row_dict.get('title') + row_dict.get('url'))
            if username in map:
                map.get(username).send(json.dumps(row_dict, ensure_ascii=False))
        #if instance.city == models.follow.objects.filter(username='qqt').first().follow_city:
            # row_dict = {
            #     # 'username':instance.username,
            #     # 'id':instance.id
            #     'title':instance.title,
            #     'city':instance.city,
            #     'url':instance.url
            # }

        #     if 'qqt' in map:
        #         own_send_email('您关注的城市' + row_dict.get('city') + '有政策更新' ,'0',row_dict.get('title') + row_dict.get('url'))
        #         sendMsm("18674810708")
        #         map.get('qqt').send(json.dumps(row_dict,ensure_ascii=False))
        # else:
        #     map['qqt'].send(json.dumps({'status':"false"}))


class UserConsumer(WebsocketConsumer):
    def connect(self):
        self.user_name = self.scope["url_route"]["kwargs"]["user_name"]
        # self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name, self.channel_name
        # )
        map[self.user_name] = self
        print("连接建立成功")
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name, self.channel_name
        # )
        pass
    # Receive message from WebSocket

    def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]

        # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name, {"type": "chat_message", "message": message}
        # )
        # async_to_sync(
        #     {"type": "chat_message", "message": message}
        # )
        self.send()

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

class ChatConsumer1(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

# class PushConsumer(AsyncWebsocketConsumer):
#   async def connect(self):
#     self.group_name = self.scope['url_route']['kwargs']['username']
#     await self.channel_layer.group_add(
#       self.group_name,
#       self.channel_name
#     )
#     await self.accept()
#   async def disconnect(self, close_code):
#     await self.channel_layer.group_discard(
#       self.group_name,
#       self.channel_name
#     )
#     # print(PushConsumer.chats)
#   async def push_message(self, event):
#     print(event)
#     await self.send(text_data=json.dumps({
#       "event": event['event']
#     }))
#
#     def push(username, event):
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             username,
#             {
#                 "type": "push.message",
#                 "event": event
#             }
#         )
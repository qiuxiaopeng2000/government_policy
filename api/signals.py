from django.dispatch import receiver

from api.consumers import handler
import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from .utils.utilsReturnData import follow_users
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from api import models

map123 = {}
@receiver(post_save, sender=models.Data)
def myhandler(sender, instance, **kwargs):
    print("chufa signal21313")
    handler(instance)




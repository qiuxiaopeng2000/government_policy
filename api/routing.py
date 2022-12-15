from django.urls import re_path

from . import consumers,signals
# from .utils.websocketUtils import UserConsumer
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<user_name>\w+)/$", consumers.UserConsumer.as_asgi()),
]
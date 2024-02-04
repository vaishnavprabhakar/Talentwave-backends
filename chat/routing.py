# chat/routing.py
from django.urls import re_path, path
from .consumer import ChatConsumer


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    # path("ws/chat/", ChatConsumer.as_asgi()),
]
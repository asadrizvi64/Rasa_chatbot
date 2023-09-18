from django.urls import re_path

from . import consumers

# to be used in later stages
websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatBotConsumer.as_asgi()),
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatBotConsumer.as_asgi()),
]
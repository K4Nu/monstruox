# routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/friend_requests/(?P<user_id>\d+)/$', consumers.FriendRequestConsumer.as_asgi()),
]

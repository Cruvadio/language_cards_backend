from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/dialogs/(?P<sel>\w+)/$', consumers.ChatConsumer),
]
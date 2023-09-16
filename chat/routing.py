from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
  # re_path(r'ws/conversation/(?P<conversation_id>\w+)/$', consumers.ConversationConsumer.as_asgi()),
  path('ws/conversation/<str:conversation_id>/', consumers.ConversationConsumer.as_asgi()),
]
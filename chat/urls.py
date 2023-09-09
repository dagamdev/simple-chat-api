from django.urls import path, re_path, include
from rest_framework import routers
from .views import UserView, ConversationView, MessageView, login, signup, ping, refresh_token

router = routers.DefaultRouter()
router.register(r'users', UserView, 'users')
router.register(r'conversation', ConversationView, 'conversation')
router.register(r'messages', MessageView, 'messages')

urlpatterns = [
  path('', include(router.urls)),
  path('', include(router.urls)),
  path('', include(router.urls)),
  re_path('ping', ping),
  re_path('login', login),
  re_path('signup', signup),
  re_path('refresh', refresh_token),
]
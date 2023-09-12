from django.urls import path, re_path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserView, 'users')
router.register(r'conversations', views.ConversationView, 'conversations')
router.register(r'messages', views.MessageView, 'messages')

urlpatterns = [
  path('', include(router.urls)),
  path('', include(router.urls)),
  path('', include(router.urls)),
  re_path('messages', views.messages),
  re_path('ping', views.ping),
  re_path('login', views.login),
  re_path('signup', views.signup),
  re_path('refresh', views.refresh_token),
]
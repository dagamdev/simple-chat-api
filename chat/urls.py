from django.urls import path, include
from rest_framework import routers
from .views import MessageView

router = routers.DefaultRouter()
router.register(r'', MessageView, 'messages')

urlpatterns = [
  path('messages/', include(router.urls))
]
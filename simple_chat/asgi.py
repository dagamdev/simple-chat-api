"""
ASGI config for simple_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_chat.settings')
default_asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
  'http': default_asgi_application,
  # "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
  
  'websocket': AllowedHostsOriginValidator(
    AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
  )
  # "websocket": URLRouter(routing.websocket_urlpatterns),
})

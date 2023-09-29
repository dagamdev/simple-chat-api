from os import environ
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import chat.routing

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
  # "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
  
  'websocket': AllowedHostsOriginValidator(
    AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),
    ['http://localhost:3000' if environ.get('IN_DEVELOPMENT') else 'https://chat-simple.vercel.app']
  )
  # "websocket": URLRouter(routing.websocket_urlpatterns),
})
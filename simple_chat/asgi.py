"""
ASGI config for simple_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_chat.settings')
# default_asgi_application = get_asgi_application()
django.setup()
application = get_default_application()

# application = ProtocolTypeRouter({
#   'http': default_asgi_application,
#   # "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns))
  
#   'websocket': AllowedHostsOriginValidator(
#     AuthMiddlewareStack(URLRouter([
#       path('ws/conversation/<str:conversation_id>/', ConversationConsumer.as_asgi())
#     ]))
#   )
#   # "websocket": URLRouter(routing.websocket_urlpatterns),
# })

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from core.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application
from django.conf.urls import url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hashchat.settings')

asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
  "http": URLRouter([
      url(r'', get_asgi_application())
  ]),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

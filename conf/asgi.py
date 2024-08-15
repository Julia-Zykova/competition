import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from notifications_app.urls import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

application = ProtocolTypeRouter({
   "http": get_asgi_application(),
   "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(
       ws_urlpatterns
   ))),
})
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from chat.middleware import ChatMiddleware
from channels.auth import AuthMiddlewareStack
# import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Talentwave.settings")
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                ChatMiddleware(
                    (URLRouter(routes=websocket_urlpatterns)),
                ),
            ),
        ),
    }
)


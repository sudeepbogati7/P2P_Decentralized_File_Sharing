from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from channels.auth import AuthMiddlewareStack
from filetransfer import consumers
from channels.security.websocket import AllowedHostsOriginValidator

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "p2p_file_sharing.settings")

websocket_urlpatterns = [
    path('/ws/peers/', consumers.PeerConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
import os
import django
from channels.routing import get_default_application
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.urls import path
from channels.auth import AuthMiddlewareStack
from filetransfer import consumers
from filetransfer import routing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "p2p_file_sharing.settings")



django.setup()

application = get_default_application()

# application = ProtocolTypeRouter({
#     "http": get_default_application(),
#     "websocket": AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter([
#                 path('/ws/peers/', consumers.PeerConsumer.as_asgi()),
#             ])
#         ),
#     )
# })

# filetransfer/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("/ws/peers/", consumers.PeerDiscoveryConsumer.as_asgi()),
]

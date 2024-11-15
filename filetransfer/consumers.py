import json
from channels.generic.websocket import WebsocketConsumer
from .peer_discovery import PeerDiscovery
import time

class PeerDiscoveryConsumer(WebsocketConsumer):
    def connect(self):
        self.discovery = PeerDiscovery()
        self.accept()
        while True:
            peers = self.discovery.get_peers()
            self.send(text_data=json.dumps({"peers": peers}))
            time.sleep(5)  

    def disconnect(self, close_code):
        self.discovery.close()

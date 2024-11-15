import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .peer_discovery import PeerDiscovery  # Import the peer discovery class

class PeerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Initialize PeerDiscovery
        self.peer_discovery = PeerDiscovery()

        # Create a task to discover peers asynchronously
        self.peer_discovery_task = asyncio.create_task(self.start_peer_discovery())

        # Define the room/group for WebSocket communication (optional)
        self.room_group_name = "peer_room"

        # Join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

        # Send initial peer data to the client
        await self.send_peers_to_client()

    async def disconnect(self, close_code):
        # Cancel the peer discovery task when the connection closes
        self.peer_discovery_task.cancel()

        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle the WebSocket message
        text_data_json = json.loads(text_data)
        peer_data = text_data_json.get('peer', None)
        print(f"Received data: {peer_data}")

        # You can handle incoming peer data here if needed

        # Send back a confirmation message
        await self.send(text_data=json.dumps({
            'message': f'Peer data received: {peer_data}'
        }))

    async def start_peer_discovery(self):
        """Continuously fetch and send the list of discovered peers"""
        while True:
            print("Continuously searching for peers ...............")
            peers = self.peer_discovery.get_peers()  # Get the latest list of peers
            print(f"Current peers: {peers}")  # Log it or update the client
            await self.send_peers_to_client()  # Send the peers to the client
            await asyncio.sleep(2)  # Delay between discovery cycles

    async def send_peers_to_client(self):
        """Send the list of peers to the WebSocket client"""
        peers = self.peer_discovery.get_peers()  # Fetch the latest peers
        await self.send(text_data=json.dumps({
            'peers': peers
        }))

import asyncio
import websockets
import json
from .peer_discovery import PeerRegistration, WebSocketHandler  # Import from your existing file

# Instantiate the PeerRegistration
peer = PeerRegistration(8000)
peer.register_service()

# Create the WebSocketHandler with the PeerRegistration instance
ws_handler = WebSocketHandler(peer)

# Define the WebSocket Server Handler
async def websocket_server_handler(websocket, path):
    # Retrieve client address
    client_address = websocket.remote_address

    try:
        async for message in websocket:
            # Pass the message to WebSocketHandler
            ws_handler.on_message(message, client_address)

    except websockets.exceptions.ConnectionClosedError:
        print(f"Connection with {client_address} closed")

# Start the WebSocket Server
async def start_server():
    server = await websockets.serve(websocket_server_handler, "0.0.0.0", 8765)
    print("WebSocket server started on port 8765")
    await server.wait_closed()

# Main entry point
if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("Shutting down server...")
    finally:
        peer.close()

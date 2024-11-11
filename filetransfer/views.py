from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .peer_discovery import discover_peers, register_service
import socket

class MainPage(View):
    def get(self, request):
        # Register this server as a peer
        register_service()

        # Discover other peers on the network
        peers = discover_peers()

        # Get server (local machine) details
        server_ip = socket.gethostbyname(socket.gethostname())
        server_info = {
            "name": "Current Device",
            "ip": server_ip,
            "port": 8000,  # Assuming your Django server is running on port 8000
        }

        # Prepare context data
        context = {
            "server_info": server_info,
            "peers": peers,
        }

        # Render the main page with server and peer details
        return render(request, "main.html", context)
    
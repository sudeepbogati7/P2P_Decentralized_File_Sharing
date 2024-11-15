from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .peer_discovery import PeerDiscovery, PeerRegistration
from zeroconf import ServiceInfo, Zeroconf, NonUniqueNameException
import socket
import json
import uuid
import time
# Initialize Zeroconf globally
zeroconf = Zeroconf()
import threading
from .websocket_server import start_server  # Import your WebSocket server start function


class MainPage(View):
    def get(self, request):
        global websocket_server_started
        websocket_server_started = False
        # Start the WebSocket server only if it hasn't been started yet
        if not websocket_server_started:
            threading.Thread(target=start_server, daemon=True).start()
            websocket_server_started = True
            print("WebSocket server started from get method")

        # Discover other peers on the network
        peer_discovery = PeerDiscovery()
        peers = peer_discovery.get_peers()

        print("Discovered peers:", peers)
        # Render the main page with peer details
        return render(request, "main.html", {"peers": peers})
    def post(self, request):
        try:
            data = json.loads(request.body)
            ip_address = data.get('ip')
            device_name = data.get('device')

            print("-ip------>", ip_address)
            print("--->------->", device_name)

            # Register the device in mDNS service
            service_name = f"{device_name}-{ip_address}.local."
            info = ServiceInfo(
                "_http._tcp.local.",
                f"{service_name}._http._tcp.local.",
                addresses=[socket.inet_aton(ip_address)],
                port=8000,
                properties={"peer": "true"}
            )

            zeroconf = Zeroconf()
            try:
                zeroconf.register_service(info)
                print(f"Peer registered: {service_name}")
                return render(request, "main.html", {
                    "message":"Peer registered successfully .",
                    "ip_addr":ip_address,
                    "device_name":device_name
                })
            except Exception as e:
                print(f"Error registering peer: {e}")
                return render(request, "main.html", {
                    "error":e,
                })
            finally:
                zeroconf.close()
        except Exception as ex:
            return JsonResponse({"status": "error", "message": str(ex)})
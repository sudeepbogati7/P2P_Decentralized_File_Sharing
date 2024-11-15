from zeroconf import Zeroconf, ServiceBrowser, ServiceInfo
import socket, asyncio
from .get_local_ip import get_local_ip
import websockets
import json


class WebSocketHandler:
    def __init__(self, peer_registration):
        self.peers = {}
        self.peer_registration = peer_registration

    def on_message(self, message, client_address):
        try:
            data = json.loads(message)
            action = data.get("action")
            if action == "register":
                client_ip = data.get("ip", client_address[0])
                client_hostname = data.get("hostname", f"unknown_{client_address[0]}")
                print("client ip : ", client_ip)
                print("Client hostname : ", client_hostname)
                # Register the client device
                self.peer_registration.register_client_service(client_ip, client_hostname)
                
                # Add to internal peer list for WebSocket management
                self.peers[client_hostname] = {"ip": client_ip, "port": self.peer_registration.port}
                print(f"Registered peer via WebSocket: {client_hostname} with IP: {client_ip}")
                
                # Send update to all connected clients
                self.send_update()

        except json.JSONDecodeError:
            print("Invalid JSON received.")

    def send_update(self):
        # Notify all connected clients with the updated peer list
        for client in self.clients:
            client.send(json.dumps({"peers": self.peers}))



class PeerRegistration:
    def __init__(self, port):
        self.zeroconf = Zeroconf()
        self.port = port
        self.registered_services = {}  # Store registered services

    def register_service(self):
        # Register the server itself
        service_name = socket.gethostname()
        local_ip = get_local_ip()
        print(f"Registering server {service_name} at {local_ip}:{self.port}")
        
        info = ServiceInfo(
            "_http._tcp.local.",
            f"{service_name}._http._tcp.local.",
            addresses=[socket.inet_aton(local_ip)],
            port=self.port,
        )
        self.zeroconf.register_service(info)
        self.registered_services[service_name] = info
        print(f"Service {service_name} registered on port {self.port} at {local_ip}")

    def register_client_service(self, client_ip, client_hostname):
        # Register the client device as a peer
        service_name = f"{client_hostname}._http._tcp.local."
        print(f"Registering client {client_hostname} at {client_ip}:{self.port}")
        
        info = ServiceInfo(
            "_http._tcp.local.",
            service_name,
            addresses=[socket.inet_aton(client_ip)],
            port=self.port,
        )

        # Register client service and store it
        self.zeroconf.register_service(info)
        self.registered_services[client_hostname] = info
        print(f"Client {client_hostname} registered on port {self.port} at {client_ip}")


    def unregister_service(self):
        # Unregister all services
        for service_name, info in self.registered_services.items():
            print(f"Unregistering service {service_name}")
            self.zeroconf.unregister_service(info)
        self.registered_services.clear()

    def close(self):
        self.unregister_service()
        self.zeroconf.close()


class PeerListener:
    def __init__(self):
        self.peers = {}

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        print("======================================")
        print("info=>", info)
        if info:
            ip_address = socket.inet_ntoa(info.addresses[0])
            service_name = info.name
            if service_name not in self.peers:
                self.peers[service_name] = {
                    "name": service_name,
                    "ip": ip_address,
                    "port": info.port,
                }
                print("self . peers ==> ", self.peers)
                print(f"Discovered peer: {service_name} at {ip_address}")

    def remove_service(self, zeroconf, service_type, name):
        if name in self.peers:
            print(f"Service removed: {name}")
            del self.peers[name]

    def update_service(self, zeroconf, service_type, name):
        print(f"Service updated: {name}")


class PeerDiscovery:
    def __init__(self):
        self.zeroconf = Zeroconf()
        self.listener = PeerListener()
        self.browser = ServiceBrowser(self.zeroconf, "_http._tcp.local.", self.listener)

    def get_peers(self):
        return list(self.listener.peers.values())

    def close(self):
        self.zeroconf.close()
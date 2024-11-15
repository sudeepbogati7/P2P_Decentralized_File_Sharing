# peer_discovery.py
from zeroconf import Zeroconf, ServiceBrowser
import socket

class PeerListener:
    def __init__(self):
        self.peers = {}

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        if info:
            ip_address = socket.inet_ntoa(info.addresses[0])
            service_name = info.name
            if service_name not in self.peers:
                print(f"Discovered peer: {service_name} at {ip_address}")
                self.peers[service_name] = {
                    "name": service_name,
                    "ip": ip_address,
                    "port": info.port,
                }

    def remove_service(self, zeroconf, service_type, name):
        if name in self.peers:
            print(f"Service removed: {name}")
            del self.peers[name]

    def update_service(self, zeroconf, service_type, name):
        print(f"Service updated: {name}")

# Function to discover peers continuously
class PeerDiscovery:
    def __init__(self):
        self.zeroconf = Zeroconf()
        self.listener = PeerListener()
        self.browser = ServiceBrowser(self.zeroconf, "_http._tcp.local.", self.listener)

    def get_peers(self):
        return list(self.listener.peers.values())

    def close(self):
        self.zeroconf.close()

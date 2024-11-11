# peer_discovery.py
# peer_discovery.py

from zeroconf import Zeroconf, ServiceInfo, ServiceBrowser,IPVersion
import socket

class PeerListener:
    def __init__(self):
        self.peers = []

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        if info:
            peer_data = {
                "name": info.server,
                "ip": socket.inet_ntoa(info.addresses[0]),
                "port": info.port,
            }
            # Avoid adding the current device as a peer
            if peer_data["ip"] != socket.gethostbyname(socket.gethostname()):
                self.peers.append(peer_data)

    def remove_service(self, zeroconf, service_type, name):
        print(f"Service removed: {name}")

def discover_peers():
    zeroconf = Zeroconf(ip_version=IPVersion.All)
    listener = PeerListener()
    service_type = "_p2pfiletransfer._tcp.local."

    browser = ServiceBrowser(zeroconf, service_type, listener)

    import time
    time.sleep(10)

    zeroconf.close()

    return listener.peers

def register_service():
    zeroconf = Zeroconf()
    service_type = "_p2pfiletransfer._tcp.local."
    service_name = f"p2p-server-{socket.gethostname()}._p2pfiletransfer._tcp.local."
    ip = socket.inet_aton(socket.gethostbyname(socket.gethostname()))
    port = 8000  # Adjust this if running on a different port

    service_info = ServiceInfo(
        service_type,
        service_name,
        addresses=[ip],
        port=port,
        properties={},
        server=f"{socket.gethostname()}.local.",
    )

    zeroconf.register_service(service_info)
    print(f"Service registered as {service_name} with IP {socket.gethostbyname(socket.gethostname())}")\




from zeroconf import Zeroconf, ServiceInfo
import socket


def discover_peers():
    zeroconf = Zeroconf()
    service_type = "_p2pfiletransfer._tcp.local."
    print("Discovering peers...")

    try:
        browser = zeroconf.add_service_listener(service_type, MyListener())

    except Exception as e :
        print(f"Error in discovery: {e}")
    input("Press enter to exit...")

    zeroconf.close()


class MyListener:
    def remove_service(self, zeroconf, type, name):
        print(f"Service removed: {name}")

    def add_service(self, zeroconf, type, name):
        print(f"Service added: {name}")
        # You can further extract IPs, port, and other data here
        info = zeroconf.get_service_info(type, name)
        print(f"Peer found: {info.server} at {info.addresses[0]}:{info.port}")

def register_service():
    zeroconf = Zeroconf()
    host_name = socket.gethostname()
    ip = socket.gethostbyname(host_name)
    port = 9999 

    service_info = ServiceInfo(
        "_p2pfiletransfer._tcp.local.",
        f"Peer-{host_name}._p2pfiletransfer._tcp.local.",
        addresses=[socket.inet_aton(ip)],
        port=port,
        properties={},
    )
    zeroconf.register_service(service_info)
    print(f"Service registered: {service_info.name} at {ip}:{port}")

    input("Press enter to unregister service and exit...")
    zeroconf.unregister_service(service_info)
    zeroconf.close()
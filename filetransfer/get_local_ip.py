import socket
from zeroconf import Zeroconf, ServiceInfo
def get_local_ip():
    # Using socket to connect to a remote address to get the correct local network IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # Connect to an arbitrary external address to determine the local interface
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'  # Fallback to localhost if connection cannot be made
    finally:
        s.close()
    return local_ip
import socket
import fcntl
import struct

def main():
    print(get_ip_address("wlan0"))
    

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s',ifname[:15].encode('utf-8'))
    )[20:24])
    
if __name__ == "__main__":
    main()


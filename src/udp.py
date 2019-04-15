

import random
import socket
import struct


class sendDNSpacket:
    def __init__(self, url, ip, port=53):
        self.url = url
        self.ip = ip
        self.port = port

    def send_packet(self):
        packet = self.build_packet()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1)
        sock.sendto(bytes(packet), (self.ip, self.port))
        data, addr = sock.recvfrom(1024)
        sock.close()
        return data  # reomove this later for the attack

    def build_packet(self):
        randomint = random.randint(0, 65535)
        packet = struct.pack(">H", randomint)
        packet += struct.pack(">H", 0x0100)
        packet += struct.pack(">H", 1)
        packet += struct.pack(">H", 0)
        packet += struct.pack(">H", 0)
        packet += struct.pack(">H", 0)
        split_url = self.url.split(".")
        for part in split_url:
            packet += struct.pack("B", len(part))
            for s in part:
                packet += struct.pack('c', s.encode())
        packet += struct.pack("B", 0)
        packet += struct.pack(">H", 1)
        packet += struct.pack(">H", 1)
        return packet

def check_port():
    # Eric and Hugh's down stairs router 74.110.211.52
    s = sendDNSpacket('www.google.com', '74.110.211.52')
    portOpen = False
    for _ in range(5):
        try:
            s.send_packet()
            portOpen = True
            break
        except socket.timeout:
            pass
    if portOpen:
        print('port open')
    else:
        print('port closed')

if __name__ == '__main__':
    check_port()

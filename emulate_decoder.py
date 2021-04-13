#!/usr/bin/env python

# Module to interface a Scaleit scale with a Moxa NPORT RS232-ETH converter.
# Tested on OS X, Python 3.7, Moxa NPort 5110A, ScaleIT DINI DFWLKI panel with DINI PBQI30 base
# 16 July 2019 - Added nonblocking

# Message can be max 46 bytes long
# 1,ST,     0.620,       0.000,         0,kg\r\n

# Message fields:
# A,B,C,D,E,F\r\n

import socket
import sys
from collections import deque

# Algorithm:
# Count number of \r\n in received buffer
# 0: store data for later
# 1: 

def main():
    print("running decoder")

    toread = 128 # How much to read into a chunk
    buf = bytearray(toread)
    view = memoryview(buf)

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 4003)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    while toread:
        nbytes = sock.recv_into(view, toread)
        view = view[nbytes:] # slicing views is cheap
        toread -= nbytes

    # We now have a chunk, hopefully containing our message. We have to drop a lot of chunks.
    sock.close()

    print('Buffer received', buf)

if __name__ == '__main__':
    main()
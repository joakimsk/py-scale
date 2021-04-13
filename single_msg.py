#!/usr/bin/env python

# Message can be max 44 bytes long for extended
# 1,ST,     0.620,       0.000,         0,kg<CR><LF>
# You may need to adjust this
MESSAGESIZE = 44

import socket
import time
import math
import sys

UDP_IP = "192.168.1.15" # Localhost IP for correct interface
UDP_PORT = 10202

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(MESSAGESIZE) # buffer size is 1024 bytes
    print(data.decode())

if __name__ == '__main__':
    main()
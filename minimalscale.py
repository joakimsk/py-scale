#!/usr/bin/env python

# Message can be max 44 bytes long
# 1,ST,     0.620,       0.000,         0,kg<CR><LF>
MESSAGESIZE = 46

import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 10202

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message:", data)



if __name__ == '__main__':
    main()
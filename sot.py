#!/usr/bin/env python

"""
Scale Optimization Tool

Used to test connection between scale and computer running this program.
Capture video of scale screen and the output from this program at the same time.
You can count number of frames between change, to determine latency.
Also use this tool to identify slow computers, networks and the likes that may infer delays.
A good connection should give around 28-30 messages per second from the scale.
"""

# Message can be max 44 bytes for extended messages
# 1,ST,     0.620,       0.000,         0,kg<CR><LF>

# Message can be max 19 bytes for short messages
# ST,GS,   0.620,kg<CR><LF>

# Can test using: echo 'ST,GS,   0.620,kg\r\n' | nc -u 127.0.0.1 10202

import socket
import time
import sys
import getopt

from os import system, name

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def usage():
    print('Scale Optimization Tool')
    print('Usage: sot.py -p <port>')
    print('Other options:')
    print('-v verbose')
    print('-h show usage (this thing)')
    print('SEE THE GITHUB PAGE (https://nmap.org/book/man.html) FOR EXAMPLES')

def closing(socket, framesize, counter, start_time):
    deltatime = time.time()-start_time
    datatraffic = framesize*counter

    socket.close()
    print('')
    print(F"Received {counter} messages over {deltatime:.2f} seconds, average {int(counter/deltatime)} per second")
    print(F"Data traffic {datatraffic} bytes over {deltatime:.2f} seconds, average {int(datatraffic/deltatime)} bytes per second")
    print('closing socket and exiting...')
    exit()

def main(argv):
    MESSAGESIZE = 19 # Bytes per message, 19 for STD and 44 for EXT
    TERMINATION = '\r\n' # <CR><LF> termination of UDP packet
    FRAME_LENGTH = 14 + 20 + 8 # Ethernet II + IPv4 + UDP Header

    BUFFER = bytearray(MESSAGESIZE) # Initialize a byte buffer of length MESSAGESIZE
    MEMORYVIEW_BUFFER = memoryview(BUFFER) # Make memoryview for slicing

    CLOSING = False

    try:
        UDP_IP = "0.0.0.0" # Localhost IP for correct interface
        UDP_BIND_PORT = 10202 # Default port

        try:
            opts, args = getopt.getopt(sys.argv[1:], "hp:v", ["help", "port="])
        except getopt.GetoptError as err:
            print(F"scalecalib: {err}")
            print('See the output of scalecalib.py -h for a summary of options.')
            sys.exit(2)

        output = None
        verbose = False
        for o, a in opts:
            if o == "-v":
                verbose = True
            elif o in ("-h", "--help"):
                usage()
                sys.exit()
            elif o in ("-p", "--port"):
                UDP_BIND_PORT = int(a)
            else:
                assert False, "unhandled option"

        print(F'listen on UDP interface:port:{UDP_IP}:{UDP_BIND_PORT}')

        lastsecond = 0
        no = 0
        start_time = time.time()
        counter = 0

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.bind((UDP_IP, UDP_BIND_PORT))

        last_messages_per_second = ''
        while True:
            if CLOSING: closing(sock, (MESSAGESIZE+FRAME_LENGTH), counter, start_time)
            no += 1
            nbytes, addr = sock.recvfrom_into(MEMORYVIEW_BUFFER,MESSAGESIZE) # buffer size is 1024 bytes
            if nbytes == MESSAGESIZE:
                counter = counter + 1
            received_at_time = time.time()-start_time

            currentsecond = int(received_at_time)
            if currentsecond > lastsecond:
                last_messages_per_second = F"{no} messages per second received"
                no = 0
                lastsecond = currentsecond

            clear()
            print(F"data: {BUFFER[:-len(TERMINATION)].decode()}")
            print(F"current time:         {time.time()-start_time}")
            print(F"last msg received at: {received_at_time}")
            print(last_messages_per_second)
    except KeyboardInterrupt:
        closing(sock, MESSAGESIZE+FRAME_LENGTH, counter, start_time)

if __name__ == '__main__':
   main(sys.argv[1:])
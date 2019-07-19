#!/usr/bin/env python

# Message can be max 44 bytes long for extended messages
# 1,ST,     0.620,       0.000,         0,kg<CR><LF>
# You may need to adjust this

MESSAGESIZE = 44
TERMINATION = '\r\n' # <CR><LF> termination of UDP packet
FRAME_LENGTH = 14 + 20 + 8 # Ethernet II + IPv4 + UDP Header

import socket
import time
import math
import sys
import getopt

from os import system, name 

CLOSING = False

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

def closing(socket, counter, start_time):
    deltatime = time.time()-start_time
    datatraffic = (MESSAGESIZE+FRAME_LENGTH)*counter

    socket.close()
    print('')
    print('Received',counter,'messages over',deltatime,'seconds, average', int(counter/deltatime), 'per second')
    print('Data traffic:',datatraffic,'bytes over',deltatime,'seconds, average', int(datatraffic/deltatime), 'bytes per second')
    print('closing socket and exiting...')
    exit()

def main(argv):
    try:
        UDP_IP = "0.0.0.0" # Localhost IP for correct interface
        UDP_BIND_PORT = 10202 # Default port

        try:
            opts, args = getopt.getopt(sys.argv[1:], "hp:v", ["help", "port="])
        except getopt.GetoptError as err:
            print('scalecalib: ' + str(err))
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

        print('listen on UDP interface:port:',UDP_IP+":"+str(UDP_BIND_PORT))

        lastsecond = 0
        no = 0
        start_time = time.time()
        counter = 0

        #print('ScaleCalib started')

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.bind((UDP_IP, UDP_BIND_PORT))

        last_messages_per_second = ''
        while True:
            if CLOSING: closing(sock, counter, start_time)

            no = no + 1
            data, addr = sock.recvfrom(MESSAGESIZE) # buffer size is 1024 bytes
            if len(data) == MESSAGESIZE:
                counter = counter + 1
            received_at_time = time.time()-start_time

            currentsecond = math.floor(received_at_time)
            if currentsecond > lastsecond:
                last_messages_per_second = str(no)+' messages per second received'
                no = 0
                lastsecond = currentsecond

            clear()
            print('data:',data[:-len(TERMINATION)].decode())
            print('current time:         ',time.time()-start_time)
            print('last msg received at: ',received_at_time)
            print(last_messages_per_second)
    except KeyboardInterrupt:
        closing(sock, counter, start_time)

if __name__ == '__main__':
   main(sys.argv[1:])
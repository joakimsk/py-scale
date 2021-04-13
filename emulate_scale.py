#!/usr/bin/env python

# Length of message is 44 bytes including \r\n, or in ascii, 46 characters due to \

# BYTES: b' -0.030,       0.000,         0,kg\r\n1,ST,    -0.030,       0.000,         0,kg\r\n'
#BYTES: b'1,ST,    -0.030,       0.000,         0,kg\r\n1,ST,    -0.030,       0.000,         0,kg\r\n1,ST,    -0.030,'

import random
from termcolor import colored
import socket
import sys
import time


ok = b'1,ST,    -0.030,       0.000,         0,kg\r\n'
bad = b'0,kg\r\n1,ST,    -0.030,       0.000,         0,kg\r\n1,ST,    -0.030,'
bad2 = b'0,kg\r\n1,ST,  1,ST,    -0.030,'

def randompacket():
    alternatives = [ok, bad, bad2]
    return alternatives[random.randint(0,2)]


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 4003)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    sock.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                randomdata = randompacket()
                print(randomdata)
                connection.sendall(randomdata)
                time.sleep(random.random())

        finally:
            # Clean up the connection
            connection.close()
    #for packetno in range(100):
        #print(packetno)
        #andlen = random.randint(1, len(afullmessage))
        #partialmsg = afullmessage[0:randlen+1]
        #remaindermsg = afullmessage[randlen:-1]

        #print(afullmessage, len(afullmessage))
        #print(colored(partialmsg, 'red'), colored(remaindermsg, 'green'))
        #print(colored(len(partialmsg), 'red'), colored(len(remaindermsg), 'green'))

         

if __name__ == '__main__':
    main()
#!/usr/bin/env python

# Module to interface a Scaleit scale with a Moxa NPORT RS232-ETH converter.
# Tested on OS X, Python 3.7, Moxa NPort 5110A, ScaleIT DINI DFWLKI panel with DINI PBQI30 base

# Message can be max 44 bytes for extended messages
# 1,ST,     0.620,       0.000,         0,kg<CR><LF>

# Message can be max 19 bytes for short messages
# ST,GS,   0.620,kg<CR><LF>

MESSAGESIZE = 19

import socket
import time
import sys
from decimal import *
import threading

class Scale():
    def __init__(self, UDP_BIND_PORT=10202):
        print('scale start')

        self.MESSAGESIZE = 19 # Bytes per message, 19 for STD and 44 for EXT
        self.TERMINATION = '\r\n' # <CR><LF> termination of UDP packet
        self.BUFFER = bytearray(MESSAGESIZE) # Initialize a byte buffer of length MESSAGESIZE
        self.MEMORYVIEW_BUFFER = memoryview(self.BUFFER) # Make memoryview for slicing
        self._dweight = 0.0
        self._time_received = None
        self.UDP_IP = "0.0.0.0" # Localhost IP for correct interface
        self.UDP_BIND_PORT = UDP_BIND_PORT

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self._sock.bind((self.UDP_IP, self.UDP_BIND_PORT))
        self._sock.setblocking(1) # Still blocking since its in a thread
        print('scale running')

        self._worker = threading.Thread(target=self.run, args=())
        self._worker.daemon = True
        self._worker.start()

    def interpret_data(self, data):
        a, b, dweight, unit = data.split(',')
        self._dweight = float('{}'.format(Decimal(dweight.strip()).quantize(Decimal('.001'), rounding=ROUND_HALF_EVEN)))

    def run(self):
        while True:
            try:
                nbytes, addr = self._sock.recvfrom_into(self.MEMORYVIEW_BUFFER,self.MESSAGESIZE) # buffer size is 1024 bytes
                temptime = time.time()
                if nbytes == self.MESSAGESIZE:
                    self.interpret_data(self.BUFFER[:-len(self.TERMINATION)].decode())
                    self._time_received = temptime
                else:
                    self.BUFFER = None
                    # Invalid message, empty buffer
            except socket.error:
                pass

    def return_last_weight(self):
        return self._time_received, self._dweight

def main():
    print("running scale module standalone")
    myscale = Scale(10202)

if __name__ == '__main__':
    main()
#!/usr/bin/env python

# Module to interface a Scaleit scale with a Moxa NPORT RS232-ETH converter.
# Tested on OS X, Python 3.7, Moxa NPort 5110A, ScaleIT DINI DFWLKI panel with DINI PBQI30 base

import socket
import sys
import time
from threading import Thread

class Scale:
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._socket = socket.socket()
        self._socket.connect((self._ip,int(self._port)))

        self._id = 0
        self._status = 'NA'
        self._dweight = 0.0
        self._tweight = 0.0
        self._npcs = 0
        self._unit = 'NA'

        self._worker = Thread(target=self.run, args=())
        self._worker.daemon = True
        self._worker.start()

    def run(self):
        while True:
            for line in self.readlines(self._socket):
                self.scaleline(line)

    def scaleline(self, line):
        # 6 elements, check page 41 of TECH_MAN_ENG_DFW_v4.pdf for details
        #   id    status    display weight  tare weight   # of pieces  unit
        # ['1', 'ST', '     0.000', '       0.245', '         0', 'kg\r']
        try:
            id, status, dweight, tweight, npcs, unit = line.split(',')
            self._id = int(id.strip())
            self._status = str(status.strip())
            self._dweight = float(dweight.strip())
            self._tweight = float(tweight.strip())
            self._npcs = int(npcs.strip())
            self._unit = str(unit.strip())
        except ValueError as err:
            pass
        except:
            raise

    def readlines(self, sock, recv_buffer=4096, delim='\r\n'):
        #print('readlines')
        buffer = ''
        readable = True
        if readable:
            data = self._socket.recv(recv_buffer).decode()
            buffer += data

            while buffer.find(delim) != -1:
                line, buffer = buffer.split('\r\n', 1)
                yield line
        return

    def lastdata(self):
        return self._id, self._status, self._dweight, self._tweight, self._npcs, self._unit

def main():
    print("running scale module standalone")
    myscale = Scale('192.168.1.4','4001')
    while True:
        data = myscale.lastdata()
        print(data)

if __name__ == '__main__':
    main()
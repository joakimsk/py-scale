#!/usr/bin/env python

# Module to interface a Scaleit scale with a Moxa NPORT RS232-ETH converter.
# Tested on OS X, Python 3.7, Moxa NPort 5110A, ScaleIT DINI DFWLKI panel with DINI PBQI30 base
# 16 July 2019 - Added nonblocking, major refactoring

# Message can be max 44 bytes for extended messages
# 1,ST,     0.620,       0.000,         0,kg<CR><LF>

# Message can be max 19 bytes for short messages
# ST,GS,   0.620,kg<CR><LF>

MESSAGESIZE = 19

import socket
import time
import sys
import getopt

from os import system, name

class Error(Exception):
   """Base class for other exceptions"""
   pass

class MessageTooLong(Error):
   """Raised when the received message is too long"""
   pass
class MessageTooShort(Error):
   """Raised when the received message is too long"""
   pass

class Scale:
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._socket = socket.socket()
        self._socket.connect((self._ip,int(self._port)))

        self._socket.setblocking(0)

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
        start_time = time.time()
        while True:
            try:
                msgbuffer = self.select_recv(self._socket, 128, timeout = None)
                msgbuffer_len = len(msgbuffer)

                print('fullbuffer',msgbuffer)
                messages = msgbuffer.split(b'\r\n')
                for idx, msg in enumerate(messages):
                    if idx == 1:
                        print(colored(msg, 'cyan'))
                    else:
                        print(msg)
                if len(messages) == 3:
                    # We know we have one complete message in the middle... Ick.
                    print('3x msg')
                
                #if msgbuffer_len > MESSAGESIZE:
                #    print(colored(msgbuffer_len, 'red'), colored(msgbuffer, 'red'))
                #    raise MessageTooLong
                #if msgbuffer_len < MESSAGESIZE:
                #    print(colored(msgbuffer_len, 'yellow'), colored(msgbuffer, 'yellow'))
                #    raise MessageTooShort
                
                

                print('## DATA START ##')
                time_since_start = time.time()-start_time
                print('TIME:',time_since_start)
                print('LEN:',msgbuffer_len)
                print('BYTES:',msgbuffer)
                if len(messages) == 3:
                    print('ISOLATED MSG:',messages[1])
                    try:
                        data = messages[1].decode('ascii', 'strict')
                    except:
                        print('decode problem')

                    # Data has been decoded from binary to ascii, and will now be interpreted
                    try:
                        self.interpret_line(data)
                        interpret_result = 'id='+str(self._id)+'status='+self._status+ \
                            'dweight='+str(self._dweight)+'tweight='+str(self._tweight)+ \
                            'npcs='+str(self._npcs)+'unit='+self._unit

                        print(colored('INTERPRET: ', 'green'), interpret_result)
                    except ValueError:
                        print(colored('INTERPRET: ValueError, invalid data', 'red'))

                print('## DATA END ##')
                print('')

            except MessageTooLong:
                print(colored("MessageTooLong, something very bad.", 'red'))
            except MessageTooShort:
                print(colored("MessageTooShort, warning.", 'yellow'))

    def select_recv(self, conn, buff_size, timeout=None):
        """add timeout for socket.recv()
        :type conn: socket.SocketType
        :type buff_size: int
        :type timeout: float
        :rtype: Union[bytes, None]
        """
        rlist, _, _ = select.select([conn], [], [], timeout)
        if not rlist:
            # timeout
            raise RuntimeError("recv timeout")

        buff = conn.recv(buff_size)
        if not buff:
            raise RuntimeError("received zero bytes, socket was closed")

        return buff 

    def interpret_line(self, line):
        try:
            id, status, dweight, tweight, npcs, unit = line.split(',')
            self._id = int(id.strip())
            self._status = str(status.strip())
            self._dweight = '{}'.format(Decimal(dweight.strip()).quantize(Decimal('.001'), rounding=ROUND_HALF_EVEN))
            self._tweight = '{}'.format(Decimal(tweight.strip()).quantize(Decimal('.001'), rounding=ROUND_HALF_EVEN))
            self._npcs = int(npcs.strip())
            self._unit = str(unit.strip())
        except ValueError as err:
            raise err
        except:
            raise

    def readlines(self, sock, recv_buffer=4096, delim='\r\n'):
        print('readlines')
        buffer = ''
        readable = True
        if readable:
            data = self._socket.recv(recv_buffer).decode()
            buffer += data#

            while buffer.find(delim) != -1:
                line, buffer = buffer.split('\r\n', 1)
                yield line
        return

    def lastdata(self):
        return self._id, self._status, self._dweight, self._tweight, self._npcs, self._unit

def main():
    print("running scale module standalone")
    myscale = Scale('localhost','4001')
    while True:
        data = myscale.lastdata()
        print(data)


if __name__ == '__main__':
    main()
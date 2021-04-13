#!/usr/bin/env python

# Message can be max 44 bytes long for extended
# 1,ST,     0.620,       0.000,         0,kg<CR><LF>
# You may need to adjust this
MESSAGESIZE = 44

import socket
import time
import math
from termcolor import colored
import sys

import matplotlib.pyplot as plt
import matplotlib.animation as animation

UDP_IP = "192.168.1.15" # Localhost IP for correct interface
UDP_PORT = 10202

def main():
    lastsecond = 0
    no = 0
    start_time = time.time()

    print('Minimal UDP receive')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    fig = plt.figure(num='Scale Calibration Window',figsize=(12,6))

    # X Y position, higher number is higher in form, from 0 to 1
    lbl_header = fig.text(0.5, 0.9, 'Scale Calibration Window', horizontalalignment='center', verticalalignment='center', fontsize='20')
    txt_now = fig.text(0.1, 0.7, 'placeholder', horizontalalignment='left', verticalalignment='center', fontsize='40')
    txt_timestamp = fig.text(0.1, 0.5, 'placeholder', horizontalalignment='left', verticalalignment='center', fontsize='40')
    txt_data = fig.text(0.1, 0.3, 'placeholder', horizontalalignment='left', verticalalignment='center', fontsize='40')
    txt_msgpersec = fig.text(0.1, 0.1, 'placeholder', horizontalalignment='left', verticalalignment='center', fontsize='40')
    
    def handle_close(evt):
        print('Closed window!')
        exit()
    
    fig.canvas.mpl_connect('close_event', handle_close)

    plt.ion() # Interactive mode on
    plt.show()

    global_timestamp = ''
    global_data = ''
    global_msgpersec = 0

    def updatewindow():
        timenow = str(time.time())
        #weight = ''
        txt_now.set_text('now:        ' + str(time.time()-start_time))
        txt_timestamp.set_text('last rcvd: ' + str(global_timestamp))
        txt_data.set_text(global_data[0:-2])
        txt_msgpersec.set_text(str(global_msgpersec)+'# msg received last second')
        plt.pause(0.001)
        plt.draw()

    while True:

        no = no + 1
        data, addr = sock.recvfrom(MESSAGESIZE) # buffer size is 1024 bytes
        timenow = time.time()-start_time

        currentsecond = math.floor(timenow)
        if currentsecond > lastsecond:
            print(colored('##  messages per second received', 'green'), colored(no,'green'))
            global_msgpersec = no
            no = 0
            lastsecond = currentsecond

        global_timestamp = timenow
        global_data = data.decode()

        print(timenow, data)
        updatewindow()
        



if __name__ == '__main__':
    main()
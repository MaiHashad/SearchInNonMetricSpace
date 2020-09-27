"""This program implements the driver file for our webserver
On your web browser navigate to the following URL: http://hostname:8000/
"""

import time
import os
import threading
import queue
from http.server import ThreadingHTTPServer
from server import Server
from socket import *
from random import shuffle
from human_backend import use_data_files



HOST_NAME = "SRLAB03.ece.umn.edu" #gethostbyname(gethostname())
PORT_NUMBER = 80

#all we're doing below is launching the server (view server.py for this stuff) and waiting to catch a KeyboardInterrupt. 
if __name__ == '__main__':
    use_data_files()
    httpd = ThreadingHTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))

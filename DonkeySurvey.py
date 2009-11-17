#!/usr/bin/python

import sys
import getopt
import thread
import time

from Config import *
from Client import *
from Listener import *

def main():
    cfg = Config()
    cfg.load_options()

    # Start mldonkey Connection Phase without pool mode
    # Connect and start listener thread
    mldonkey = Client(cfg)
    mldonkey.connect()

    # Start listener thread to receive server msgs 
    listener = Listener("Listener", mldonkey.connection, cfg)
    thread.start_new_thread(listener.start, ())

    while 1:time.sleep(0)
    #while 1:pass

if __name__ == "__main__":
    main()


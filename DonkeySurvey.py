#!/usr/bin/python

import sys
import getopt
import thread
import time
import logging

from Config import *
from Client import *
from Listener import *
from MessageHandler import *

def main():
    # Load config options from config file and command line args
    cfg = Config()
    cfg.load_options()

    # Create logger
    log_format = '%(asctime)s DonkeySurvey %(levelname)s: %(message)s'
    log_level = logging.INFO
    if cfg.debug is 1:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level, 
                        format=log_format, 
                        filename=cfg.output_filename)
    # Define a Handler which writes "log_level" messages or 
    # higher to the sys.stdout
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(log_level)
    # Set a format which is simpler for console use
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    # Tell the handler to use this format
    console.setFormatter(formatter)
    # Add the handler to the root logger
    logging.getLogger('').addHandler(console)

    # Start mldonkey Connection Phase without pool mode
    # Connect and start listener thread
    mldonkey = Client(cfg)
    mldonkey.connect()

    # Start listener thread to receive server msgs 
    listener = Listener("Listener", mldonkey.connection, cfg)
    handler = MessageHandler(listener)
    #thread.start_new_thread(listener.start, ())
    thread.start_new_thread(handler.start, ())

    while 1:time.sleep(0)
    #while 1:pass

if __name__ == "__main__":
    main()


#!/usr/bin/python

import sys
import getopt
import thread
import time
import logging
import atexit
import resource

sys.path.append('./database')

from DBConnection import *
from Config import *
from Client import *
from Listener import *
from MessageHandler import MessageHandler

def main():
    # Load config options from config file and command line args
    cfg = Config()
    cfg.load_options()

    if cfg.background is 1:
        # Detach a process from the controlling terminal and run it in the
        # background as a daemon.
        try:
           pid = os.fork()
        except OSError, e:
           raise Exception, "%s [%d]" % (e.strerror, e.errno)
    
        if (pid == 0):       # The first child.
           os.setsid()
    
           try:
              pid = os.fork()        # Fork a second child.
           except OSError, e:
              raise Exception, "%s [%d]" % (e.strerror, e.errno)
    
           if (pid == 0):    # The second child.
              os.chdir('/')
              os.umask(0)
           else:
              sys.exit(0)    # Exit parent (the first child) of the second child.
        else:
           sys.exit(0)       # Exit parent of the first child.
    
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

    if cfg.background is not 1:
        # Add the handler to the root logger
        logging.getLogger('').addHandler(console)

    # Start mldonkey Connection Phase without pool mode
    # Connect and start listener thread
    mldonkey = Client(cfg)
    mldonkey.connect()

    # Start listener thread to receive server msgs
    dbconnection = DBConnection.getInstance();
    dbconnection.setHost(cfg.dbhost)
    dbconnection.setDatabase(cfg.dbname) 
    dbconnection.setUser(cfg.dbuser) 
    dbconnection.setPassword(cfg.dbpass) 
    listener = Listener("Listener", mldonkey.connection, cfg)
    handler = MessageHandler(listener)
    #thread.start_new_thread(listener.start, ())
    thread.start_new_thread(handler.start, ())

    #while 1:time.sleep(0)
    while 1:pass

if __name__ == "__main__":
    main()


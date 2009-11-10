#!/usr/bin/python

import sys
import getopt
import thread
import time

from Config import Config

from Client import Client
from Listener import Listener

def usage():
    print "Syntax error"
    print "  -h, --help         This help"
    print "  -d, --debug        Set debug to true, showing messages sent and received."
    print "  -v, --verbose      Set verbose to true, showing useful."
    print "  -o, --output=FILE  Dump all output in FILE. (Default Stdout)"
    print "  -H, --host=HOST    Host name to connect. (Default localhost)"
    print "  -p, --port=PORT    Port to connect. (Default 4001)"
    print "  -U, --user=USER    User for authentication. (Default admin)"
    print "  -P, --pass=PASS    Password for authentication. (Default empty)"

def get_args():
    config = Config()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdvo:H:p:U:P:",
                                   ["help", "debug", "verbose", "output=", "host=", "port=", "user=", "pass="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--debug"):
            config.DEBUG = 1
        elif o in ("-v", "--verbose"):
            config.VERBOSE = 1
        elif o in ("-o", "--output"):
            config.OUTPUT_FILE = a
        elif o in ("-H", "--host"):
            config.HOST = a
        elif o in ("-p", "--port"):
            config.PORT = int(a)
        elif o in ("-U", "--user"):
            config.USER = a
        elif o in ("-P", "--pass"):
            config.PASSWORD = a
        else:
            assert False, "unhandled option"

    return config

def main():
    config = get_args()

    # Start mldonkey Connection Phase without pool mode
    # Connect and start listener thread
    mldonkey = Client(config)
    mldonkey.connect()

    # Start listener thread to receive server msgs 
    listener = Listener("Listener", mldonkey.connection, config)
    thread.start_new_thread(listener.start, ())

    while 1:time.sleep(0)
    #while 1:pass

if __name__ == "__main__":
    main()


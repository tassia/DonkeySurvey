#!/usr/bin/python

import sys
import getopt
import thread
import time

from Client import Client
from Listener import Listener

# Default values
HOST = "127.0.0.1"
PORT = 4001
USER = "admin"
PASSWORD = ""
DEBUG=0
VERBOSE=0
OUTPUT_FILE=None
GUI_PROTO_VERSION=41

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
    global HOST,PORT,USER,PASSWORD,DEBUG,VERBOSE,OUTPUT_FILE
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdo:H:p:U:P:",
                                   ["help", "debug", "output=", "host=", "port=", "user=", "pass="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--debug"):
            DEBUG = 1
        elif o in ("-v", "--verbose"):
            VERBOSE = 1
        elif o in ("-o", "--output"):
            OUTPUT_FILE = a
        elif o in ("-H", "--host"):
            HOST = a
        elif o in ("-p", "--port"):
            PORT = int(a)
        elif o in ("-U", "--user"):
            USER = a
        elif o in ("-P", "--pass"):
            PASSWORD = a
        else:
            assert False, "unhandled option"

def main():
    get_args()

    # Start mldonkey Connection Phase without pool mode
    # Connect and start listener thread
    mldonkey = Client(HOST, PORT, USER, PASSWORD, GUI_PROTO_VERSION, DEBUG, VERBOSE, OUTPUT_FILE)
    mldonkey.connect()

    while 1:time.sleep(0)
    #while 1:pass

if __name__ == "__main__":
    main()


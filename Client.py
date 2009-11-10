#!/usr/bin/python

import sys
import socket
import thread
import struct
import binascii

from GUIProtoDefinitions import *
from Listener import *
from Message import *
from SocketCommon import *

class Client(SocketCommon):
    def __init__(self, config):
        self.config = config

    def connect(self):
        print "* Connecting to mldonkey...",
        for res in socket.getaddrinfo(self.config.HOST, self.config.PORT, socket.AF_UNSPEC,
                                      socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except socket.error, msg:
                s = None
                continue
            try:
                s.connect(sa)
                self.connection = s
            except socket.error, msg:
                s.close()
                s = None
                continue
            break
        if s is None:
            print 'could not open socket: %d - %s' % (msg[0], msg[1])
	    sys.exit(-1)

        print "connected."

        # Read mldonkey server protocol version
        print "* Reading protocol version..."
        self.read()	

        # Send Client Protocol Version
        print "* Sending protocol version..."
        self.send('<lhl', [OPCODE("ProtocolVersion"), self.config.GUI_PROTO_VERSION])

        # Send login and password
        print "* Sending user and password..."
        self.send_login(self.config.USER,self.config.PASSWORD)

        # Set connection non-blocking
        self.connection.setblocking(0)
        
	return s


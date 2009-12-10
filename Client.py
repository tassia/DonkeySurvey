#!/usr/bin/python

import sys
import socket
import thread
import struct
import binascii
import os

from GUIProtoDefinitions import *
from Listener import *
from Message import *
from SocketCommon import *

class Client(SocketCommon):
    def __init__(self, config):
        self.config = config

    def connect(self):
        for res in socket.getaddrinfo(self.config.hostname, self.config.port,
                                      socket.AF_UNSPEC, socket.SOCK_STREAM):
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
            logging.error("Could not open socket with mldonkey server: %d - %s",
                          msg[0], msg[1])
            os.abort()

        logging.info("Connected to mldonkey.")

        # Read mldonkey server protocol version
        logging.info("Reading protocol version...")
        self.read()	

        # Send Client Protocol Version
        logging.info("Sending protocol version...")
        self.send('<lhl', [OPCODE("ProtocolVersion"), GUI_PROTO_VERSION])

        # Send login and password
        logging.info("Sending user and password...")
        self.send_login(self.config.username,self.config.password)

        # Set connection non-blocking
        self.connection.setblocking(1)
        
        return s


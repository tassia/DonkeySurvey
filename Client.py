#!/usr/bin/python

import sys
import socket
import thread
import struct
import binascii

sys.path.append('../guiclient/')
from GUIProtoDefinitions import *
from Listener import Listener
from Message import Message

SIZE_LEN=4
SIZE_OPCODE=2

class Client():
    def __init__(self, HOST, PORT, USER, PASSWORD, GUI_PROTO_VERSION, DEBUG, VERBOSE, OUTPUT_FILE):
        self.host = HOST
        self.port = PORT
        self.user = USER
        self.password = PASSWORD
        self.protocol = GUI_PROTO_VERSION
        self.debug = DEBUG
        self.verbose = VERBOSE
        self.output = OUTPUT_FILE

    def connect(self):
        print "* Connecting to mldonkey...",
        for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC,
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

        print "connected."

        # Read mldonkey server protocol version
        print "* Reading protocol version..."
        self.start_listener()

        # Send Client Protocol Version
        print "* Sending protocol version..."
        self.send('<lhl', [OPCODE("ProtocolVersion"),self.protocol])

        # Send login and password
        print "* Sending user and password..."
        self.send_login(self.user,self.password)

        # Set connection non-blocking
        self.connection.setblocking(0)
        
        return s

    # Start listener thread to receive server msgs 
    def start_listener(self): 
        self.listener = Listener("Listener", self, self.debug, self.output)
        thread.start_new_thread(self.listener.start, ())

    def send_login(self, login, password):
        login_l=len(login)
        password_l=len(password)
        format = "<l h h %ds h %ds" % (password_l, login_l)
        self.send(format, [OPCODE("PassWord"), password_l, password, login_l, login])

    def send(self, format, data):
        length = struct.calcsize(format)-SIZE_LEN
        # TODO
        #self.print_msg("SEND %d bytes | Opcode = %d (%s)", (length, data[0], OPCODE_SENT[str(data[0])]))
        data = struct.pack(format, length, *data)
        self.connection.send(data)

#!/usr/bin/python

import sys
import struct
import socket

sys.path.append('../guiclient/')
from GUIProtoDefinitions import *
from Message import Message

SIZE_LEN=4
SIZE_OPCODE=2

class Listener():
    def __init__(self, name, client, debug, output):
        self.name = name
        self.connection = client.connection
        self.debug = debug
        self.output = output

    def read_length(self):
        try:
            data = struct.unpack('<l', self.connection.recv(SIZE_LEN))[0]
        except socket.error, msg:
            data = None
            # print socket.error, msg
        return data

    def read_opcode(self):
        try:
            data = struct.unpack('<h', self.connection.recv(SIZE_OPCODE))[0]
        except socket.error, msg:
            data = None
            # print socket.error, msg
        return data

    def read_data(self, length):
        try:
            data = self.connection.recv(length-SIZE_OPCODE)
        except socket.error, msg:
            data = None
            # print socket.error, msg
        return data

    def read(self):
        length = self.read_length()
        if length is not None:
            opcode = self.read_opcode()
            raw_data = self.read_data(length)
            msg = Message(opcode, raw_data, self.debug, self.output)
            msg.print_msg("RECV %d bytes | Opcode = %d (%s)", (length, opcode, OPCODE_RECV[str(opcode)]))
            #if opcode is 48:
            #    file_id = msg.decode()
            #    print file_id
            #    self.client.send('<lhl', [OPCODE("GetFileInfo"), file_id])
            #else:
            msg.decode()
            return length
        else:
            return None

    def start(self):
        while(1):
            self.read()

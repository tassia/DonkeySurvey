#!/usr/bin/python

import socket
import struct
import logging

from GUIProtoDefinitions import *
from Config import *
from Message import *

from Constants import *

class SocketCommon():
    def send_login(self, login, password):
        login_l=len(login)
        password_l=len(password)
        format = "<l h h %ds h %ds" % (password_l, login_l)
        self.send(format, [OPCODE("PassWord"), password_l, password, login_l, login])

    def send(self, format, data):
        length = struct.calcsize(format)-SIZE_LEN
        logging.debug("SEND %d bytes | Opcode = %d (%s)", length, data[0], OPCODE_SENT[str(data[0])])
        data = struct.pack(format, length, *data)
        self.connection.send(data)
 
    def send_cmd(self, cmd):
        cmd_l=len(cmd)
        format = "<l h h %ds" % (cmd_l)
        logging.debug("SENDING ConsoleCommand")
        self.send(format, [OPCODE("ConsoleCommand"), cmd_l, cmd])

    def read_length(self):
        # TODO: Fix-me when password is invalid
        try:
            data = struct.unpack('<l', self.connection.recv(SIZE_LEN))[0]
        except socket.error, msg:
            data = None
            #logging.exception("%s: %s", socket.error, str(msg))
        return data

    def read_opcode(self):
        try:
            data = struct.unpack('<h', self.connection.recv(SIZE_OPCODE))[0]
        except socket.error, msg:
            data = None
            #logging.exception("%s: %s", socket.error, str(msg))
        return data

    def read_data(self, length):
        try:
            data = self.connection.recv(length)
        except socket.error, msg:
            data = None
            #logging.exception("%s: %s", socket.error, str(msg))
        return data

    def read(self):
        length = self.read_length()
        if length is not None:
            opcode = self.read_opcode()
            raw_data = self.read_data(length-SIZE_OPCODE)
            #logging.debug("=================OPCODE = %s", opcode)
            msg = Message(opcode, raw_data, self.config, length)
            try:
                logging.debug("RECV %d bytes | Opcode = %d (%s)", length, opcode, OPCODE_RECV[str(opcode)])
            except Exception, err:
                return msg    
            return msg
            #if opcode is 48:
            #    file_id = msg.decode()
            #    self.send('<lhl', [OPCODE("GetFileInfo"), file_id])
            #else:
            #    msg.decode()
            #return length
        else:
            return None



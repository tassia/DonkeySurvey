import socket
import struct

from GUIProtoDefinitions import *
from Config import *
from Message import *

class SocketCommon():
    def send_login(self, login, password):
        login_l=len(login)
        password_l=len(password)
        format = "<l h h %ds h %ds" % (password_l, login_l)
        self.send(format, [OPCODE("PassWord"), password_l, password, login_l, login])

    def send(self, format, data):
        length = struct.calcsize(format)-self.config.SIZE_LEN
        # TODO
        # Message().print_msg("SEND %d bytes | Opcode = %d (%s)", (length, data[0], OPCODE_SENT[str(data[0])]))
        data = struct.pack(format, length, *data)
        self.connection.send(data)

    def read_length(self):
        # TODO: Fix-me when password is invalid
        try:
            data = struct.unpack('<l', self.connection.recv(self.config.SIZE_LEN))[0]
        except socket.error, msg:
            data = None
            # print socket.error, msg
        return data

    def read_opcode(self):
        try:
            data = struct.unpack('<h', self.connection.recv(self.config.SIZE_OPCODE))[0]
        except socket.error, msg:
            data = None
            # print socket.error, msg
        return data

    def read_data(self, length):
        try:
            data = self.connection.recv(length-self.config.SIZE_OPCODE)
        except socket.error, msg:
            data = None
            # print socket.error, msg
        return data

    def read(self):
        length = self.read_length()
        if length is not None:
            opcode = self.read_opcode()
            raw_data = self.read_data(length)
            msg = Message(opcode, raw_data, self.config)
            msg.print_msg("RECV %d bytes | Opcode = %d (%s)", (length, opcode, OPCODE_RECV[str(opcode)]))
            if opcode is 48:
                file_id = msg.decode()
                print file_id
                self.send('<lhl', [OPCODE("GetFileInfo"), file_id])
            else:
                msg.decode()
            return length
        else:
            return None



#!/usr/bin/python

import sys
import struct
import socket
import logging

from GUIProtoDefinitions import *
from Message import Message
from SocketCommon import SocketCommon

sys.path.append('../database')
sys.path.append('../database/entities')
from FileDAO import FileDAO
from File import File

class MessageHandler:

    def __init__(self, listener):
        self.listener = listener

    def start(self):
        logging.info("Starting listener...")
        while(1):
            self.msg = self.listener.read()
            if self.msg is not None:
                self.decode()

    def decode(self):
        if self.msg.opcode is 9:
           self.msg.decode_msg_9(self.msg.raw_data)
        elif self.msg.opcode is 10:
            self.msg.decode_msg_10(self.msg.raw_data)
        elif self.msg.opcode is 15:
            self.msg.decode_msg_15(self.msg.raw_data)
        elif self.msg.opcode is 16:
            self.msg.decode_msg_16(self.msg.raw_data)
        elif self.msg.opcode is 20:
            self.msg.decode_msg_20(self.msg.raw_data)
        elif self.msg.opcode is 46:
            self.msg.decode_msg_46(self.msg.raw_data)
        elif self.msg.opcode is 48:
            file_id = self.msg.decode_msg_48(self.msg.raw_data)
            self.listener.send('<lhl', [OPCODE("GetFileInfo"), file_id])
        elif self.msg.opcode is 50:
            self.msg.decode_msg_50(self.msg.raw_data)
        elif self.msg.opcode is 52:
            file = self.msg.decode_msg_52(self.msg.raw_data)
            fdao = FileDAO()
	    fdao.insertOrUpdate(file)


               


            #TODO check OPCODE
            #TODO create entity
            #TODO store in database through DAO
    

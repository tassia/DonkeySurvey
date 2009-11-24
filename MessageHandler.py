#!/usr/bin/python

import sys
import struct
import socket
import logging

from GUIProtoDefinitions import *
from Message import Message
from SocketCommon import SocketCommon

class MessageHandler:

    def __init__(self, listener):
        self.listener = listener

    def start(self):
        logging.info("Starting listener...")
        while(1):
            self.msg = self.listener.read()
            #TODO check OPCODE
            #TODO create entity
            #TODO store in database through DAO
    

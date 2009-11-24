#!/usr/bin/python

import sys
import struct
import socket
import logging

from GUIProtoDefinitions import *
from Message import Message
from SocketCommon import SocketCommon

class Listener(SocketCommon):
    def __init__(self, name, connection, config):
        self.name = name
        self.connection = connection
        self.config = config

    #def start(self):
    #    logging.info("Starting listener...")
    #    while(1):
    #        self.read()

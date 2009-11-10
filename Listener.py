#!/usr/bin/python

import sys
import struct
import socket

from GUIProtoDefinitions import *
from Message import Message
from SocketCommon import SocketCommon

class Listener(SocketCommon):
    def __init__(self, name, connection, config):
        self.name = name
        self.connection = connection
	self.config = config

    def start(self):
        while(1):
            self.read()

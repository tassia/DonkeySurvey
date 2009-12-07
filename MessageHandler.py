#!/usr/bin/python

import sys
import struct
import socket
import logging

from GUIProtoDefinitions import *
from Message import Message
from SocketCommon import SocketCommon

sys.path.append('./database')
sys.path.append('./database/entities')

from FileDAO import FileDAO
from File import File
from FilenameDAO import FilenameDAO
from FileHasFilenameDAO import FileHasFilenameDAO
from SessionDAO import SessionDAO
from Filename import Filename

class MessageHandler:

    def __init__(self, listener):
        self.listener = listener
        # Dicts to save id-hash values for active files and sources 
        self.file_id_hash = dict()
        self.source_id_hash = dict()
        self.file_sources = dict()

    def start(self):
        logging.info("Starting listener...")
        while(1):
            self.msg = self.listener.read()
            if self.msg is not None:
                self.decode()

    def decode(self):

        # Message: OptionsInfo
        # Action: none
        if self.msg.opcode is 1:
            self.msg.decode_msg_1(self.msg.raw_data)

        # Message: FileUpdateAvailability
        # Action: update file availability for this source
        elif self.msg.opcode is 9:
            self.msg.decode_msg_9(self.msg.raw_data)

        # Message: FileAddSource
        # Action: none
        elif self.msg.opcode is 10:
            file_id, source_id = self.msg.decode_msg_10(self.msg.raw_data)
            logging.debug("Source ID: %d" , source_id)

        # Message: ClientInfo
        # Action: update and persist session on database
        elif self.msg.opcode is 15:
            session = self.msg.decode_msg_15(self.msg.raw_data)
            if session:
                sdao = SessionDAO()
                sessionId = sdao.insert(session)

        # Message: ClientState
        # Action: none
        elif self.msg.opcode is 16:
            self.msg.decode_msg_16(self.msg.raw_data)

        # Message: ConsoleMessage
        # Action: handle wanted info (commands 'vd' and 'vc')
        elif self.msg.opcode is 19:
            cmd, arg, result_list = self.msg.decode_msg_19(self.msg.raw_data)
            if cmd == "vd":
                self.file_sources[arg] = result_list
                for s in result_list:
                    cmd = "vc %d" % (s)
                    self.listener.send_cmd(cmd)
                logging.debug("###############################################")
                logging.debug(self.file_sources)
#            if cmd == "vc":
 #               source_id_hash[source_id]=source.hash

        # Message: NetworkInfo
        # Action: none
        elif self.msg.opcode is 20:
            self.msg.decode_msg_20(self.msg.raw_data)

        # Message: UserInfo
        # Action: never received such message
        elif self.msg.opcode is 21:
            self.msg.decode_msg_21(self.msg.raw_data)

        # Message: ServerInfo
        # Action: none
        elif self.msg.opcode is 26:
            server_id = self.msg.decode_msg_26(self.msg.raw_data)
            self.listener.send('<lhl', [32, server_id])

        # Message: FileDownloadUpdate
        # Action: update and persist session on database
        elif self.msg.opcode is 46:
            self.msg.decode_msg_46(self.msg.raw_data)

        # Message: SharedFileInfo
        # Action: none
        elif self.msg.opcode is 48:
            file_id = self.msg.decode_msg_48(self.msg.raw_data)
            self.listener.send('<lhl', [OPCODE("GetFileInfo"), file_id])

        # Message: FileRemoveSource
        # Action: none
        elif self.msg.opcode is 50:
            self.msg.decode_msg_50(self.msg.raw_data)

        # Message: FileInfo
        # Action: populate file related entities and send 'vd' to get file sources
        elif self.msg.opcode is 52:
            file, file_id = self.msg.decode_msg_52(self.msg.raw_data)
            self.file_id_hash[file_id]=file.hash
            logging.debug("######################################################")
            logging.debug(self.file_id_hash)
            fdao = FileDAO()
	    fileId = fdao.insertOrUpdate(file)
            if fileId is None:
	        logging.debug("FileId is null")
            fnamedao = FilenameDAO() 
            fhasfnamedao = FileHasFilenameDAO()
            for k,v in file.filenames.iteritems():
                filename = Filename()
                filename.name = v
                filenameId = fnamedao.insertOrUpdate(filename)
                if filenameId is None:
                    logging.debug("Filename is null")
                fhasfnamedao.insertOrUpdate(fileId, filenameId); 
            cmd = "vd %d" % (file_id) 
            self.listener.send_cmd(cmd) 

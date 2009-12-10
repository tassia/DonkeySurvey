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

from File import File
from Source import Source
from Filename import Filename
from FileDAO import FileDAO
from FilenameDAO import FilenameDAO
from FileHasFilenameDAO import FileHasFilenameDAO
from AddressHasFileDAO import AddressHasFileDAO
from SourceHasFileDAO import SourceHasFileDAO
from SessionDAO import SessionDAO
from AddressDAO import AddressDAO
from SourceDAO import SourceDAO

class MessageHandler:

    def __init__(self, listener):
        self.listener = listener
        # Id-hash values for active files and sources 
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
            file_id, source_id, availability = self.msg.decode_msg_9(self.msg.raw_data)
            logging.debug("Update Availability: %d (File %d, Source %d)" % (availability, file_id, source_id))
            if source_id in self.source_id_hash:
                sdao = SourceDAO()  
                sourceId = sdao.findByHash(self.source_id_hash[source_id]).id
                fdao = FileDAO()  
                fileId = fdao.findByHash(self.file_id_hash[file_id]).id
                shfdao = SourceHasFileDAO()
                shfdao.insertOrUpdate(fileId, sourceId, availability)

        # Message: FileAddSource
        # Action: none
        elif self.msg.opcode is 10:
            file_id, source_id = self.msg.decode_msg_10(self.msg.raw_data)
            logging.debug("Add Source: %d (File %d)" % (source_id, file_id))

        # Message: ClientInfo
        # Action: update and persist session on database
        elif self.msg.opcode is 15:
            session = self.msg.decode_msg_15(self.msg.raw_data)
            source_id = str(session.source.id) #fake
            adao = AddressDAO()
            addressId = adao.insertOrUpdate(session.address)
            logging.debug(self.source_id_hash)
            fileId = None
            file_id = 0
            logging.debug(self.file_sources)
            logging.debug(self.file_id_hash)
            for file in self.file_sources:
                logging.debug(source_id)
                logging.debug(file)
                if source_id in self.file_sources[file]:
                    file_id = int(file)
                    logging.debug(file_id)
                    if file_id in self.file_id_hash:
                        fdao = FileDAO()
                        fileHash = self.file_id_hash[file_id] 
                        fileId = fdao.findByHash(fileHash).id
                        logging.debug("F-HASH: %s, F-ID: %s, ADDR-ID: %s" % (fileHash, fileId ,addressId))
                        logging.debug("*****File id***: %d" % (file_id))
                        #TODO: consider more than one session with the same source

            logging.debug("*****File id: %d" % (file_id))
            if session is not None and file_id != 0:
                if source_id in self.source_id_hash:
                    session.address.id = addressId
                    session.file.id = fileId
                    logging.debug(self.source_id_hash)
                    logging.debug("*******Sourcehash: %s" % (self.source_id_hash[source_id]))
                    srcdao = SourceDAO()
                    sourceHash = self.source_id_hash[source_id]
                    session.source.id = srcdao.findByHash(sourceHash).id
                    logging.debug("Source %d, File %d: Uploaded(%d), Donwloaded(%d))" % (source_id, file_id, session.uploaded, session.downloaded))
                    logging.debug(session.source.id)
                    sdao = SessionDAO()
                    sessionId = sdao.insertOrUpdate(session)            
                    if sessionId is None:
                        logging.debug("SessionId is null")

                else:
                    logging.debug("****** IP-no-hash: %s",addressId)
                    if fileId is not None:
                        ahf = AddressHasFileDAO()
                        ahf.insert(addressId, fileId)


        # Message: ClientState
        # Action: none
        elif self.msg.opcode is 16:
            self.msg.decode_msg_16(self.msg.raw_data)

        # Message: ConsoleMessage
        # Action: handle wanted info (commands 'vd' and 'vc')
        elif self.msg.opcode is 19:
            cmd, id, result = self.msg.decode_msg_19(self.msg.raw_data)
            if cmd == "vd":
                # cmd = 'vd', id = file_id, result = file_sources
                self.file_sources[id] = result
                logging.debug("###############################################")
                logging.debug(self.file_sources)
                for s in result:
#                if s not in self.source_id_hash:
                    cmd = "vc %d" % (s)
                    self.listener.send_cmd(cmd)
            if cmd == "vc" and result:
                # cmd = 'vc', id = source_id, result = source
                source = result[0]
                address = result[1]
                if source.hash == "00000000000000000000000000000000":
                    logging.debug("****** IP-no-hash: %s",address.ip)
                    adao = AddressDAO()
                    addressId = adao.insertOrUpdate(address)
                    ahf = AddressHasFileDAO()
                    f = FileDAO()
                    for file in self.file_sources:
                        if int(id) in self.file_sources[file]:
                            if int(file) in self.file_id_hash:
                                file_hash = self.file_id_hash[int(file)]
                                logging.debug("F-HASH: %s, F-ID: %s, ADDR-ID: %s" % (file_hash, f.findByHash(file_hash).id,addressId))
                                ahf.insert(addressId, f.findByHash(file_hash).id)
                else:
                    self.source_id_hash[id]=source.hash
                    logging.debug("###############################################")
                    logging.debug(self.source_id_hash)
                    srcdao = SourceDAO()
        	    sourceId = srcdao.insertOrUpdate(source)
                    if sourceId is None:
    	                logging.debug("SourceId is null")
                    shf = SourceHasFileDAO()
                    f = FileDAO()
                    logging.debug(self.file_sources)
                    for file in self.file_sources:
                        logging.debug(self.file_sources[file])
                        logging.debug("##########ID: %s",id)
                        if int(id) in self.file_sources[file]:
                            logging.debug(self.file_id_hash)
                            if int(file) in self.file_id_hash:
                                file_hash = self.file_id_hash[int(file)]
                                logging.debug("F-HASH: %s, F-ID: %s, SRC-ID: %s" % (file_hash, f.findByHash(file_hash).id,sourceId))
                                shf.insertOrUpdate(sourceId, f.findByHash(file_hash).id, "0")

        # Message: NetworkInfo
        # Action: none
        elif self.msg.opcode is 20:
            self.msg.decode_msg_20(self.msg.raw_data)

        # Message: UserInfo
        # Action: never received
        elif self.msg.opcode is 21:
            self.msg.decode_msg_21(self.msg.raw_data)

        # Message: ServerInfo
        # Action: none
        elif self.msg.opcode is 26:
            server_id = self.msg.decode_msg_26(self.msg.raw_data)
            #self.listener.send('<lhl', [32, server_id])

        # Message: FileDownloadUpdate
        # Action: update and persist session on database
        elif self.msg.opcode is 46:
            file_id, size = self.msg.decode_msg_46(self.msg.raw_data)
            file = FileDAO()
            file.hash = self.file_id_hash[file_id]
            file.partialSize = size
            file.insertOrUpdate(file)

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
		# checar se = -1
                if filenameId is None:
                    logging.debug("Filename is null")
                fhasfnamedao.insertOrUpdate(fileId, filenameId); 
            cmd = "vd %d" % (file_id) 
            self.listener.send_cmd(cmd) 

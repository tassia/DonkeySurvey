#!/usr/bin/python

import struct
import binascii
import sys

sys.path.append('../database')
sys.path.append('../database/entities')

from FileDAO import FileDAO
from File import File

class Message():
    def __init__(self, opcode, raw_data, config):
        self.opcode = opcode
        self.raw_data = raw_data
        self.config = config

    def decode_string(self,data, offset):
        str_len = struct.unpack_from('<h', data, offset)
        format = "<%ds" % (str_len)
        string = struct.unpack_from(format, data, offset+2)
        return string[0]

    def decode_int(self,type,data, offset):
        format = "<%s" % (type)
        return struct.unpack_from(format, data, offset)[0]

    def decode_char(self, len, data, offset):
        format = "<%dc" % (len)
        return struct.unpack_from(format, data, offset)[0]

    def decode(self):
        if self.opcode is 9:
            self.decode_msg_9(self.raw_data)
        elif self.opcode is 10:
            self.decode_msg_10(self.raw_data)
        elif self.opcode is 15:
            self.decode_msg_15(self.raw_data)
        elif self.opcode is 16:
            self.decode_msg_16(self.raw_data)
        elif self.opcode is 20:
            self.decode_msg_20(self.raw_data)
        elif self.opcode is 46:
            self.decode_msg_46(self.raw_data)
        elif self.opcode is 48:
            return self.decode_msg_48(self.raw_data)
        elif self.opcode is 50:
            self.decode_msg_50(self.raw_data)
        elif self.opcode is 52:
            self.decode_msg_52(self.raw_data)
    
    # FileUpdateAvailability
    def decode_msg_9(self, raw_data):
        file_number = self.decode_int("l", raw_data, 0) 
        client_number = self.decode_int("l", raw_data, 4) 
        avail_len = self.decode_int("h", raw_data, 8)
        availability = self.decode_string(raw_data, 8)
        self.print_msg("FileNumber: %d | ClientNumber: %d | Availability_len: %d | Availability: %s ", (file_number, client_number, avail_len, availability))
    
    # FileAddSource
    def decode_msg_10(self, raw_data):
        file_id = self.decode_int("l", raw_data, 0)
        source_id = self.decode_int("l", raw_data, 4)
        self.print_msg("FileID: %d | SourceIdentifier: %d ",(file_id, source_id))
    
    # ClientInfo
    def decode_msg_15(self, raw_data):
        client_id = self.decode_int("l", raw_data, 0)
        client_netid = self.decode_int("l", raw_data, 4)
        client_type = self.decode_int("b", raw_data, 8)
        self.print_msg("ClientID: %d | CLientNetworkID: %d | ClientType: %d ", (client_id, client_netid, client_type))
        offset = 9
        if client_type is 1:
            client_name_len = self.decode_int("h", raw_data, offset)
            client_name = self.decode_string(raw_data, offset)
            client_hash = struct.unpack_from("<17s", raw_data, 11 + client_name_len)
            self.print_msg("--- ClientName: %s (%d) | ClientHash: %s", (client_name, client_name_len, str.upper(binascii.hexlify("".join(client_hash)))))
            offset = 28 + client_name_len;
        ip0 = self.decode_int("B", raw_data, offset)
        ip1 = self.decode_int("B", raw_data, offset+1)
        ip2 = self.decode_int("B", raw_data, offset+2)
        ip3 = self.decode_int("B", raw_data, offset+3)
        geoip = self.decode_int("B", raw_data, offset + 4)
        port = self.decode_int("H", raw_data, offset + 5)
        self.print_msg("--- IP: %d.%d.%d.%d | geoip: %d | Port: %d ", (ip0, ip1, ip2, ip3, geoip, port))
        offset += 7
        connection_state = self.decode_int("B", raw_data, offset)
        offset += 1
        self.print_msg("--- ConnectionState: %d ", (connection_state))
        if str(connection_state) in ("3", "5", "9"):
            rank = self.decode_int("l", raw_data, offset)
            self.print_msg("--- Rank: %d ", (rank))
            offset += 4
        client_type = self.decode_int("b", raw_data, offset)
        offset += 1
        self.print_msg("--- ClientType: %d ", (client_type))
        tag_list_len = self.decode_int("h", raw_data, offset)
        self.print_msg("--- TagListLen: %d ", (tag_list_len))
        offset += 2
        for i in range(tag_list_len):
            tag_name_len = self.decode_int("h", raw_data, offset)
            tag_name = self.decode_string(raw_data, offset)
            offset += 2 + tag_name_len
            tag_type = self.decode_int("b", raw_data, offset)
            offset += 1
            if str(tag_type) in ("0", "1", "3", "6"):
                tag_value = self.decode_int("l", raw_data, offset)
                offset += 4
            elif tag_type is 2:
                 tag_value_len = self.decode_int("h", raw_data, offset)
                 tag_value = self.decode_string(raw_data, offset)
                 offset += 2 + tag_value_len
            elif tag_type is 4:
                tag_value = self.decode_int("h", raw_data, offset)
                offset += 2
            elif tag_type is 5:
                tag_value = self.decode_int("b", raw_data, offset)
                offset += 1
            self.print_msg("--- Tag %d -> %s = %s", (i, tag_name, str(tag_value)))
        client_name_len = self.decode_int("h", raw_data, offset)
        client_name = self.decode_string(raw_data,offset)
        offset += 2 + client_name_len
        self.print_msg("--- ClientName: %s", (client_name))
        client_rating = self.decode_int("l", raw_data, offset)
        offset += 4
        self.print_msg("--- ClientRating: %d", (client_rating))
        client_software_len = self.decode_int("h", raw_data, offset)
        client_software = self.decode_string(raw_data, offset)
        offset += 2 + client_software_len
        self.print_msg("--- ClientSoftware: %s", (client_software))
        downloaded = self.decode_int("L", raw_data, offset)
        offset += 8
        uploaded = self.decode_int("L", raw_data, offset)
        offset += 8
        self.print_msg("--- Downloaded: %d | Uploaded: %d", (downloaded, uploaded))
        upload_filename_len = self.decode_int("h", raw_data, offset)
        upload_filename = self.decode_string(raw_data, offset)
        offset += 2 + upload_filename_len
        self.print_msg("--- UploadFileName: %s", (upload_filename))
        connected_time = self.decode_int("l", raw_data, offset)
        offset += 4
        self.print_msg("--- ConnectedTime: %d", (connected_time))
        emule_mod_len = self.decode_int("h", raw_data, offset)
        emule_mod = self.decode_string(raw_data, offset)
        offset += 2 + emule_mod_len
        self.print_msg("--- EMuleMod: %s", (emule_mod))
        client_version_len = self.decode_int("h", raw_data, offset)
        client_version = self.decode_string(raw_data, offset)
        offset += 2 + client_version_len
        self.print_msg("--- ClientVersion: %s", (client_version))
        sui_verified = self.decode_int("b", raw_data, offset)
        self.print_msg("--- SuiVerified: %d", (sui_verified))
	if downloaded is not 0 or uploaded is not 0:
	    print "ClientID: %d | ClientName: %s | ClientIP: %d.%d.%d.%d | ClientPort: %d | ClientSoftware: %s | ConnectionState: %d | FileName: %s | Down: %d | Up: %d " % (client_id, client_name, ip0, ip1, ip2, ip3, port, client_software, connection_state, upload_filename, downloaded, uploaded)

    # ClientState
    def decode_msg_16(self, raw_data):
        client_id = self.decode_int("l", raw_data, 0) 
        connection_state = self.decode_int("b", raw_data, 4) 
        self.print_msg("ClientID: %d | ConnectionState: %d ", (client_id, connection_state))
        if str(connection_state) in ("3", "5", "9"):
            rank = self.decode_int("l", raw_data, 5) 
            self.print_msg("--- Rank: %d ", (rank))

    # NetworkInfo
    def decode_msg_20(self, raw_data):
        network_id = self.decode_int("l", raw_data, 0)
        network_name_len = self.decode_int("h", raw_data, 4)
        network_name = self.decode_string(raw_data, 4)
        enable = self.decode_int("b", raw_data, 6 + network_name_len)
        offset = 7 + network_name_len
        network_config_file_len = self.decode_int("h", raw_data, offset)
        network_config_file = self.decode_string(raw_data, offset)
        offset += 2 + network_config_file_len
        bytes_downloaded = self.decode_int("L", raw_data, offset)
        offset += 8
        bytes_uploaded = self.decode_int("L", raw_data, offset)
        offset += 8
        connected_servers = self.decode_int("l", raw_data, offset)
        offset += 4
        self.print_msg("NetworkID: %d | NetworkName: %s | Enable: %d | NetworkConfigFile: %s | Down: %d | Up: %d | ConnServers: %d ", 
                      (network_id, network_name, enable, network_config_file, bytes_downloaded, bytes_uploaded, connected_servers))
        tags_len = self.decode_int("h", raw_data, offset)
        offset += 2
        self.print_msg("--- NetworkFlags: %d", (tags_len))
        for i in range(tags_len):
            tag = self.decode_int("h", raw_data, offset)
            offset += 2
            self.print_msg("--- NetworkFlag: %d", (tag))

    # FileDownloadUpdate
    def decode_msg_46(self, raw_data):
        file_id = self.decode_int("l", raw_data, 0) 
        downloaded_size = self.decode_int("q", raw_data, 4) 
        rate_len = self.decode_int("h", raw_data, 12)
        download_rate = self.decode_string(raw_data, 12)
        last_seen = self.decode_int("l", raw_data, 14 + rate_len)
        self.print_msg("FileID: %d | Downloaded: %d | Download_rate: %s | Seconds since last seen: %d ", (file_id, downloaded_size, download_rate, last_seen))

    # SharedFileInfo
    def decode_msg_48(self, raw_data):
        file_id = self.decode_int("l", raw_data, 0) 
        netid = self.decode_int("l", raw_data, 4) 
        file_len = self.decode_int("h", raw_data, 8)
        file = self.decode_string(raw_data, 8)
        file_size = self.decode_int("q", raw_data, 10 + file_len) 
        uploaded = self.decode_int("q", raw_data, 18 + file_len) 
        requests = self.decode_int("l", raw_data, 26 + file_len) 
        self.print_msg("FileID: %d | NetworkID: %d | FileName: %s | FileSize: %d | Uploaded: %d | Requests: %d ", (file_id, netid, file, file_size, uploaded, requests))
        # TODO
        # self.send('<lhl', [OPCODE("GetFileInfo"), file_id])
        return file_id

    # FileRemoveSource
    def decode_msg_50(self, raw_data):
        file_id = self.decode_int("l", raw_data, 0)
        source_id = self.decode_int("l", raw_data, 4)
        self.print_msg("FileID: %d | SourceIdentifier: %d ", (file_id, source_id))

    # FileInfo
    def decode_msg_52(self, raw_data):
        file_id = self.decode_int("l", raw_data, 0) 
        net_id = self.decode_int("l", raw_data, 4)
        pfile_names_len = self.decode_int("h", raw_data, 8)
	offset = 10
        self.print_msg("FileID: %d | NetworkID: %d | Possible File Names: %d", (file_id, net_id, pfile_names_len))
        for i in range(pfile_names_len):
	    file_name_len = self.decode_int("h", raw_data, offset)
	    file_name = self.decode_string(raw_data, offset)
	    file_name2 = file_name
	    offset += 2 + file_name_len
	    self.print_msg("--- PossibleFileName: %s", (file_name))
        file_md4 = struct.unpack_from("<16c", raw_data, offset)
	offset += 16
        file_size = self.decode_int("L", raw_data, offset)
	offset += 8
	downloaded = self.decode_int("L", raw_data, offset)
	offset += 8
	sources = self.decode_int("l", raw_data, offset)
	offset += 4
	clients = self.decode_int("l", raw_data, offset)
	offset += 4
	file_state = self.decode_int("b", raw_data, offset)
	offset += 1
	self.print_msg("--- FileMD4: %s | FileSize: %d | Sources: %d | Clients: %d | FileState: %d ", (str.upper(binascii.hexlify("".join(file_md4))), file_size, sources, clients, file_state))
	if file_state is 6:
	    reason_len = self.decode_int("h", raw_data, offset)
	    reason = self.decode_string(raw_data, offset)
	    offset += 2 + reason_len
	    self.print_msg("--- Reason: %s", (reason))
        chunks_len = self.decode_int("h", raw_data, offset)
	chunks = self.decode_string(raw_data, offset)
	offset += 2 + chunks_len
        self.print_msg("--- Chunks: %s ", (chunks))
	availability_len = self.decode_int("h", raw_data, offset)
	offset += 2
	self.print_msg("--- AvailabilityLen: %d", (availability_len))
	for i in range(availability_len):
	    network_number = self.decode_int("l", raw_data, offset)
	    offset += 4
	    source_chunks_len = self.decode_int("h", raw_data, offset)
	    source_chunks = self.decode_string(raw_data, offset)
	    offset += 2 + source_chunks_len
	    self.print_msg("--- NetworkNumber: %d | SourceChunksLen: %d | SourceChunks: %s ", (network_number, source_chunks_len, source_chunks))
        float_len = self.decode_int("h", raw_data, offset)
	offset += 2
	format_float = "<%dc" % float_len
	float = struct.unpack_from(format_float, raw_data, offset)
	offset += float_len
	self.print_msg("Tamanho: %d | Float: %s", (float_len, float))
	chunks_ages_len = self.decode_int("h", raw_data, offset)
	offset += 2
	for i in range(chunks_ages_len):
	    chunk_age = self.decode_int("l", raw_data, offset)
	    offset += 4
	    self.print_msg("--- ChunkAge: %d", (chunk_age))
        file_age = self.decode_int("l", raw_data, offset)
	offset += 4
        print "FileID: %d | FileMD4 %s | FileSize: %d | DownloadState: %d" % (file_id, str.upper(binascii.hexlify("".join(file_md4))), file_size, file_state)
        fdao = FileDAO()
	file = File()
	file.hash = str.upper(binascii.hexlify("".join(file_md4)))
	file.size = file_size
	file.bestName = file_name2
	fdao.insert(file)

    def print_msg(self, msg, args):
        if self.config.debug:
            if self.config.output_filename is None:
                print "DEBUG: " + msg % args
            else:
                try:
                    FILE = open(self.config.output_filename, "a")
                    FILE.write("DEBUG: " + msg % args + "\n")
                    FILE.close()
                except IOError, msg:
                    print "Unable to open output file: %d - %s" % (msg[0], msg[1])
                    sys.exit(1)


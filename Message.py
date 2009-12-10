#!/usr/bin/python

import struct
import binascii
import sys
import logging
import re

sys.path.append('./database')
sys.path.append('./database/entities')

from File import *
from Address import *
from Session import *
from Source import *
from datetime import *

class Message():

    def __init__(self, opcode, raw_data, config, length):
        self.opcode = opcode
        self.raw_data = raw_data
        self.config = config
        self.length = length

    def decode_string(self,data, offset):
        str_len = struct.unpack_from('<h', data, offset)
        format = "<%ds" % (str_len)
        try:
            string = struct.unpack_from(format, data, offset+2)
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return ""
        return string[0]

    def decode_int(self,type,data, offset):
        format = "<%s" % (type)
        return struct.unpack_from(format, data, offset)[0]

    def decode_char(self, len, data, offset):
        format = "<%dc" % (len)
        return struct.unpack_from(format, data, offset)[0]
   
    # GuiOptionsInfo 
    def decode_msg_1(self, raw_data):
        list_len = self.decode_int("h", raw_data, 0)
        offset = 2
        for i in range(list_len):
            option_len = self.decode_int("h", raw_data, offset)
            option = self.decode_string(raw_data, offset)
            offset += 2 + option_len
            option2_len = self.decode_int("h", raw_data, offset)
            option2 = self.decode_string(raw_data, offset)
            offset += 2 + option2_len
            #logging.debug("Option: %s | Value: %s", option, option2)
 
    # FileUpdateAvailability
    def decode_msg_9(self, raw_data):
        file_number = self.decode_int("l", raw_data, 0) 
        client_number = self.decode_int("l", raw_data, 4) 
        avail_len = self.decode_int("h", raw_data, 8)
        availability = self.decode_string(raw_data, 8)
        logging.debug(('FileNumber: %d | ClientNumber: %d | '
                       'Availability_len: %d | Availability: %s "'),
                       file_number, client_number, avail_len, availability)
        logging.debug("%s, %s, %s", file_number, client_number, 
                      float(availability.count('1')) / len(availability))
        return file_number, client_number, \
               float(availability.count('1')) / len(availability)

    # FileAddSource
    def decode_msg_10(self, raw_data):
        file_id = self.decode_int("l", raw_data, 0)
        source_id = self.decode_int("l", raw_data, 4)
        logging.debug("FileID: %d | SourceIdentifier: %d ",file_id, source_id)
        return (file_id, source_id)
    
    # ClientInfo
    def decode_msg_15(self, raw_data):
        session = Session()

        client_id = self.decode_int("l", raw_data, 0)
        client_netid = self.decode_int("l", raw_data, 4)
        client_type = self.decode_int("b", raw_data, 8)
        logging.debug("ClientID: %d | CLientNetworkID: %d | ClientType: %d ", 
                      client_id, client_netid, client_type)
        offset = 9
        if client_type is 1:
            client_name_len = self.decode_int("h", raw_data, offset)
            client_name = self.decode_string(raw_data, offset)
            client_hash = struct.unpack_from("<17s", raw_data, 
                                             11 + client_name_len)

            logging.debug("--- ClientName: %s (%d) | ClientHash: %s",
                          client_name, client_name_len, 
                          str.upper(binascii.hexlify("".join(client_hash))))

            offset = 28 + client_name_len;

        ip0 = self.decode_int("B", raw_data, offset)
        ip1 = self.decode_int("B", raw_data, offset+1)
        ip2 = self.decode_int("B", raw_data, offset+2)
        ip3 = self.decode_int("B", raw_data, offset+3)
        geoip = self.decode_int("B", raw_data, offset + 4)
        port = self.decode_int("H", raw_data, offset + 5)
        logging.debug("--- IP: %d.%d.%d.%d | geoip: %d | Port: %d ", ip0, ip1, 
                      ip2, ip3, geoip, port)
        offset += 7
        connection_state = self.decode_int("B", raw_data, offset)
        offset += 1
        logging.debug("--- ConnectionState: %d ", connection_state)
        if str(connection_state) in ("3", "5", "9"):
            rank = self.decode_int("l", raw_data, offset)
            logging.debug("--- Rank: %d ", rank)
            offset += 4
        client_type = self.decode_int("b", raw_data, offset)
        offset += 1
        logging.debug("--- ClientType: %d ", client_type)
        tag_list_len = self.decode_int("h", raw_data, offset)
        logging.debug("--- TagListLen: %d ", tag_list_len)
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
            logging.debug("--- Tag %d -> %s = %s", i, tag_name, str(tag_value))

        client_name_len = self.decode_int("h", raw_data, offset)
        client_name = self.decode_string(raw_data,offset)
        offset += 2 + client_name_len
        logging.debug("--- ClientName: %s", client_name)
        client_rating = self.decode_int("l", raw_data, offset)
        offset += 4
        logging.debug("--- ClientRating: %d", client_rating)
        client_software_len = self.decode_int("h", raw_data, offset)
        client_software = self.decode_string(raw_data, offset)
        offset += 2 + client_software_len
        logging.debug("--- ClientSoftware: %s", client_software)
        downloaded = self.decode_int("L", raw_data, offset)
        offset += 8
        uploaded = self.decode_int("L", raw_data, offset)
        offset += 8
        logging.debug("--- Downloaded: %d | Uploaded: %d", downloaded, uploaded)
        upload_filename_len = self.decode_int("h", raw_data, offset)
        upload_filename = self.decode_string(raw_data, offset)
        offset += 2 + upload_filename_len
        logging.debug("--- UploadFileName: %s", upload_filename)
        connected_time = self.decode_int("l", raw_data, offset)
        offset += 4
        logging.debug("--- ConnectedTime: %d", connected_time)
        emule_mod_len = self.decode_int("h", raw_data, offset)
        emule_mod = self.decode_string(raw_data, offset)
        offset += 2 + emule_mod_len
        logging.debug("--- EMuleMod: %s", emule_mod)
        client_version_len = self.decode_int("h", raw_data, offset)
        client_version = self.decode_string(raw_data, offset)
        offset += 2 + client_version_len
        logging.debug("--- ClientVersion: %s", client_version)
        sui_verified = self.decode_int("b", raw_data, offset)
        logging.debug("--- SuiVerified: %d", sui_verified)
	if downloaded is not 0 or uploaded is not 0:
	    logging.debug(('ClientID: %d | ClientName: %s | '
                           'ClientIP: %d.%d.%d.%d | ClientPort: %d | '
                           'ClientSoftware: %s | ConnectionState: %d | '
                           'FileName: %s | Down: %d | Up: %d '), 
                           client_id, client_name, ip0, ip1, ip2, ip3, 
                           port, client_software, connection_state, 
                           upload_filename, downloaded, uploaded)

        session.address.ip = "%d.%d.%d.%d" % (ip0, ip1, ip2, ip3)
        session.address.port = port 
        session.downloaded = downloaded
        session.uploaded = uploaded
        session.source.id = client_id
        if client_type==0:
            session.kind = "lowID"
        else:
            session.kind = "highID"
    	return session

    # ClientState
    def decode_msg_16(self, raw_data):
        client_id = self.decode_int("l", raw_data, 0) 
        connection_state = self.decode_int("b", raw_data, 4) 
        #logging.debug("ClientID: %d | ConnectionState: %d ", 
        #               client_id, connection_state)
        if str(connection_state) in ("3", "5", "9"):
            rank = self.decode_int("l", raw_data, 5) 
            logging.debug("--- Rank: %d ", rank)

    # ConsoleMessage
    def decode_msg_19(self, raw_data):
        msg = self.decode_string(raw_data,0)
        logging.debug("ConsoleMessage: %s", msg)
        m = re.compile("Eval command: (.*) (.*)")
        if m.search(msg):
            cmd = m.search(msg).group(1)
            arg = m.search(msg).group(2)
            if (cmd == "vd"):
                try:
                    sources = re.split("sources:\n", msg)[1]
                    #logging.debug(sources)
                    m = re.compile("^  \[( *?\d+)\]", re.M)
                    result =  m.findall(sources)
                    #logging.debug(result)
                    b = [int(x) for x in result]
                    logging.debug("Sources RESULT (VD): %s" % (b))
                except Exception, err:
                    return None, None, None
                return cmd, int(arg), b
            if (cmd == "vc"):
                source = Source()
                address = Address()
                regex = "Client %s:.*" % (arg)
                try:
                    m = re.compile(regex)
                    result = re.split("\(|\)| '|'| ", 
                                      m.findall(msg)[0])
                    result2 = re.split("\(|\)| '|'| |:", 
                                       m.findall(msg)[0])
                except Exception, err:
                    return None, None, None

                try:
                    m = re.compile("MD4: .*")
                    md4 = re.split(" ", m.findall(msg)[0])
                except Exception, err:
                    md4 = ['', '']

                try:
                    m = re.compile("osinfo: .*")
                    osinfo = re.split(" ", m.findall(msg)[0])
                except Exception, err:
                    osinfo = ['','']
                logging.debug("RESULT (VC): %s" % (result))
                if result2[3] == "0.0.0.0":
                    return None, None, None
                source.name = result[9] 
                source.hash = md4[1]
                source.software = "%s %s" % (result[6], result[7])
                source.so = osinfo[1]
                address.ip = result2[3]
                address.port = result2[4]
                return cmd, int(arg), (source, address)
        return None, None, None

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
        #logging.debug(('NetworkID: %d | NetworkName: %s | Enable: %d | '
        #               'NetworkConfigFile: %s | Down: %d | Up: %d | '
        #               'ConnServers: %d '), network_id, network_name, 
        #                enable, network_config_file, bytes_downloaded, 
        #                bytes_uploaded, connected_servers)

        tags_len = self.decode_int("h", raw_data, offset)
        offset += 2
        #logging.debug("--- NetworkFlags: %d", tags_len)
        for i in range(tags_len):
            tag = self.decode_int("h", raw_data, offset)
            offset += 2
            #logging.debug("--- NetworkFlag: %d", tag)

    # GuiUserInfo
    def decode_msg_21(self, raw_data):
        user_id = self.decode_int("l", raw_data, 0)
        offset = 4
        user_md4 = struct.unpack_from("<16c", raw_data, offset)
	offset += 16
        user_name_len = self.decode_int("h", raw_data, offset)
        user_name = self.decode_string(raw_data, offset)
        offset += 2 + user_name_len
        user_addr_type = self.decode_int("b", raw_data, offset)
        offset += 1
        logging.debug(('UserID: %d | UserMD4: %s | UserName: %s | '
                       'UserAddrType: %d'), user_id,
                      str.upper(binascii.hexlify("".join(user_md4))),
                      user_name, user_addr_type)
        if user_addr_type is 0:
            user_ip = self.decode_int("l", raw_data, offset)
            offset += 4
            logging.debug("--- UserIP: %d", user_ip)
        if user_addr_type is 1:
            user_geoip = self.decode_int("b", raw_data, offset)
            offset += 1
            user_name_addr_len = self.decode_int("h", raw_data, offset)
            user_name_addr = self.decode_string(raw_data, offset)
            offset += 2 + user_name_addr_len
            logging.debug("--- UserGEOIP: %d | UserNameAddr: %s", 
                          user_geoip, user_name_addr)
        blocked = self.decode_int("b", raw_data, offset)
        offset += 1
        logging.debug("--- Blocked: %d ", blocked)
      
    # ServerInfo (Partial)
    def decode_msg_26(self, raw_data):
        server_id = self.decode_int("h", raw_data, 0)
        #logging.debug("ServerID: %d ", server_id)
        return server_id
 
    # FileDownloadUpdate
    def decode_msg_46(self, raw_data):
        file_id = self.decode_int("l", raw_data, 0) 
        downloaded_size = self.decode_int("q", raw_data, 4) 
        rate_len = self.decode_int("h", raw_data, 12)
        download_rate = self.decode_string(raw_data, 12)
        last_seen = self.decode_int("l", raw_data, 14 + rate_len)
        #logging.debug(('FileID: %d | Downloaded: %d | Download_rate: %s | '
        #               'Seconds since last seen: %d '), file_id, 
        #               downloaded_size, download_rate, last_seen)
        return file_id, downloaded_size

    # SharedFileInfo
    def decode_msg_48(self, raw_data):
        file_id = self.decode_int("l", raw_data, 0) 
        netid = self.decode_int("l", raw_data, 4) 
        file_len = self.decode_int("h", raw_data, 8)
        file = self.decode_string(raw_data, 8)
        file_size = self.decode_int("q", raw_data, 10 + file_len) 
        uploaded = self.decode_int("q", raw_data, 18 + file_len) 
        requests = self.decode_int("l", raw_data, 26 + file_len) 
        #logging.debug(('FileID: %d | NetworkID: %d | FileName: %s | '
        #               'FileSize: %d | Uploaded: %d | Requests: %d '),
        #               file_id, netid, file, file_size, uploaded, requests)
        return file_id

    # FileRemoveSource
    def decode_msg_50(self, raw_data):
        file_id = self.decode_int("l", raw_data, 0)
        source_id = self.decode_int("l", raw_data, 4)
        logging.debug("FileID: %d | SourceIdentifier: %d ", file_id, source_id)

    # FileInfo
    def decode_msg_52(self, raw_data):
	file = File()

        file_id = self.decode_int("l", raw_data, 0) 
        net_id = self.decode_int("l", raw_data, 4)
        pfile_names_len = self.decode_int("h", raw_data, 8)
	offset = 10
        logging.debug("FileID: %d | NetworkID: %d | Possible File Names: %d",
                      file_id, net_id, pfile_names_len)
        for i in range(pfile_names_len):
	    file_name_len = self.decode_int("h", raw_data, offset)
	    file_name = self.decode_string(raw_data, offset)
	    offset += 2 + file_name_len
	    logging.debug("--- PossibleFileName: %s", file_name)
            file.filenames[i] = file_name
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
	logging.debug(('--- FileMD4: %s | FileSize: %d | Sources: %d | '
                       'Clients: %d | FileState: %d '), 
                      str.upper(binascii.hexlify("".join(file_md4))), 
                      file_size, sources, clients, file_state)
	if file_state is 6:
	    reason_len = self.decode_int("h", raw_data, offset)
	    reason = self.decode_string(raw_data, offset)
	    offset += 2 + reason_len
	    logging.debug("--- Reason: %s", reason)
        chunks_len = self.decode_int("h", raw_data, offset)
	chunks = self.decode_string(raw_data, offset)
	offset += 2 + chunks_len
        logging.debug("--- Chunks: %s ", chunks)
	availability_len = self.decode_int("h", raw_data, offset)
	offset += 2
	logging.debug("--- AvailabilityLen: %d", availability_len)
	for i in range(availability_len):
	    network_number = self.decode_int("l", raw_data, offset)
	    offset += 4
	    source_chunks_len = self.decode_int("h", raw_data, offset)
	    source_chunks = self.decode_string(raw_data, offset)
	    offset += 2 + source_chunks_len
	    logging.debug(('--- NetworkNumber: %d | SourceChunksLen: %d | '
                           'SourceChunks: %s '), network_number, 
                           source_chunks_len, source_chunks)
        float_len = self.decode_int("h", raw_data, offset)
	offset += 2
	format_float = "<%dc" % float_len
	float = struct.unpack_from(format_float, raw_data, offset)
	offset += float_len
	logging.debug("--- Size: %d | Float: %s", float_len, float)
	chunks_ages_len = self.decode_int("h", raw_data, offset)
	offset += 2
	for i in range(chunks_ages_len):
	    chunk_age = self.decode_int("l", raw_data, offset)
	    offset += 4
	    #logging.debug("--- ChunkAge: %d", chunk_age)
        file_age = self.decode_int("l", raw_data, offset)
	offset += 4
        logging.debug(('--- FileID: %d | FileMD4 %s | FileSize: %d | '
                       'DownloadState: %d'), file_id, 
                       str.upper(binascii.hexlify("".join(file_md4))), 
                       file_size, file_state)
        file_format = self.decode_int("b", raw_data, offset)
        offset += 1
        logging.debug("--- FileFormat: %d ", file_format)
        if file_format is 1:
            extension_len = self.decode_int("h", raw_data, offset)
            extension = self.decode_string(raw_data, offset)
            offset += 2 + extension_len
            kind_len = self.decode_int("h", raw_data, offset)
            kind = self.decode_string(raw_data, offset)
            offset += 2 + kind_len
	    logging.debug("--- Extension: %s | Kind %s ", extension, kind)
        if file_format is 2:
            video_codec_len = self.decode_int("h", raw_data, offset)
            video_codec = self.decode_string(raw_data, offset)
            offset += 2 + video_codec_len
            video_width = self.decode_int("l", raw_data, offset)
            offset += 4
            video_height = self.decode_int("l", raw_data, offset)
            offset += 4
            video_fps = self.decode_int("l", raw_data, offset)
            offset += 4
            video_rate = self.decode_int("l", raw_data, offset)
            offset += 4
	    logging.debug(('--- VideoCodec: %s | VideoWidth %d | '
                           'VideoHeight: %d | VideoFPS: %d | VideoRate: %d'), 
                          video_codec, video_width, video_height, 
                          video_fps, video_rate)
        if file_format is 3:
            mp3_title_len = self.decode_int("h", raw_data, offset)
            mp3_title = self.decode_string(raw_data, offset)
            offset += 2 + mp3_title_len
            mp3_artist_len = self.decode_int("h", raw_data, offset)
            mp3_artist = self.decode_string(raw_data, offset)
            offset += 2 + mp3_artist_len
            mp3_album_len = self.decode_int("h", raw_data, offset)
            mp3_album = self.decode_string(raw_data, offset)
            offset += 2 + mp3_album_len
            mp3_year_len = self.decode_int("h", raw_data, offset)
            mp3_year = self.decode_string(raw_data, offset)
            offset += 2 + mp3_year_len
            mp3_comment_len = self.decode_int("h", raw_data, offset)
            mp3_comment = self.decode_string(raw_data, offset)
            offset += 2 + mp3_comment_len
            mp3_track = self.decode_int("l", raw_data, offset)
            offset += 4
            mp3_genre = self.decode_int("l", raw_data, offset)
            offset += 4
            logging.debug(('--- Mp3Title: %s | Mp3Artist: %s |  Mp3Album: %s | '
                           'Mp3Year: %s | Mp3Comment: %s | Mp3Track: %d | '
                           'Mp3Genre: %d'), mp3_title, mp3_artist, mp3_album, 
                           mp3_year, mp3_comment, mp3_track, mp3_genre)
        if file_format is 4:
            list_len = self.decode_int("h", raw_data, offset)
            offset += 2
            for i in range(list_len):
                stream_number = self.decode_int("l", raw_data, offset)
                offset += 4
                stream_type = self.decode_int("b", raw_data, offset)
                offset += 1
                ogg_tags_len = self.decode_int("h", raw_data, offset)
                offset += 2
                tags = dict()
                for j in range(ogg_tags_len):
                    tags[0] = self.decode_int("b", raw_data, offset)
                    offset += 1
                    tag_01_len = self.decode_int("h", raw_data, offset)
                    tags[1] = self.decode_string(raw_data, offset)
                    offset += 2 + tag_01_len
                    tags[2] = self.decode_int("h", raw_data, offset)
                    offset += 2
                    tags[3] = self.decode_int("h", raw_data, offset)
                    offset += 2
                    tags[4] = self.decode_int("h", raw_data, offset)
                    offset += 2
                    tags[5] = self.decode_int("h", raw_data, offset)
                    offset += 2
                    tags[6] = self.decode_int("h", raw_data, offset)
                    offset += 2
                    float_len = self.decode_int("h", raw_data, offset)
                    offset += 2
	            format_float = "<%dc" % float_len
	            tags[7] = struct.unpack_from(format_float, raw_data, 
                                                 offset)
	            offset += float_len
                    tags[8] = self.decode_int("h", raw_data, offset)
                    offset += 2
                    float_len = self.decode_int("h", raw_data, offset)
                    offset += 2
	            format_float = "<%dc" % float_len
	            tags[9] = struct.unpack_from(format_float, raw_data,
                                                 offset)
	            offset += float_len
                    float_len = self.decode_int("h", raw_data, offset)
                    offset += 2
	            format_float = "<%dc" % float_len
	            tags[10] = struct.unpack_from(format_float, raw_data, 
                                                  offset)
	            offset += float_len
                    float_len = self.decode_int("h", raw_data, offset)
                    offset += 2
	            format_float = "<%dc" % float_len
	            tags[11] = struct.unpack_from(format_float, raw_data,
                                                  offset)
	            offset += float_len
                    list_len = self.decode_int("h", raw_data, offset)
                    offset += 2
                    # TODO: Fix
                    tags[12] = None
                    for k in range(list_len):
                        list1 = seld.decode_int("b",raw_data, offset)
                        offset += 1
                        float_len = self.decode_int("h", raw_data, offset)
                        offset += 2
                        format_float = "<%dc" % float_len
                        list2 = struct.unpack_from(format_float, raw_data, 
                                                   offset)
                        offset += float_len
                    tags[13] = self.decode_int("h", raw_data, offset)
                    offset += 4
                    tags[14] = self.decode_int("h", raw_data, offset)
                    offset += 4
                    float_len = self.decode_int("h", raw_data, offset)
                    offset += 2
                    format_float = "<%dc" % float_len
                    tags[15] = struct.unpack_from(format_float, raw_data,
                                                  offset)
                    offset += float_len
		    float_len = self.decode_int("h", raw_data, offset)
                    offset += 2
                    format_float = "<%dc" % float_len
                    tags[16] = struct.unpack_from(format_float, raw_data,
                                                  offset)
                    offset += float_len
                    float_len = self.decode_int("h", raw_data, offset)
                    offset += 2
                    format_float = "<%dc" % float_len
                    tags[17] = struct.unpack_from(format_float, raw_data,
                                                  offset)
                    offset += float_len
                    float_len = self.decode_int("h", raw_data, offset)
                    offset += 2
                    format_float = "<%dc" % float_len
                    tags[18] = struct.unpack_from(format_float, raw_data,
                                                  offset)
                    offset += float_len
                    tags[19] = self.decode_int("b", raw_data, offset)
                    offset += 1
                    tags[20] = self.decode_int("l", raw_data, offset)
                    offset += 4
        file_pref_name_len = self.decode_int("h", raw_data, offset)
        file_pref_name = self.decode_string(raw_data,offset)
        offset += 2 + file_pref_name_len
        logging.debug("--- File Preferred Name: %s ", file_pref_name)
	file.hash = str.upper(binascii.hexlify("".join(file_md4)))
	file.size = file_size
        file.partialSize = downloaded
	file.bestName = file_pref_name
        return file, file_id


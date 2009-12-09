import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO
from Filename import Filename

class FileHasFilenameDAO(CommonDAO):

    jointable = "file_has_filename"

    def __init__(self):
        CommonDAO.__init__(self)
    
    def insertOrUpdate(self, fileId, filenameId):
        try:
            rs = self.findByFileFilename(fileId, filenameId)
            if not rs:
                query = "INSERT INTO %s(file_id, filename_id) VALUES(%s, %s)" % (self.jointable, fileId, filenameId)
                logging.debug(query)
                self.cursor.execute(query)
                #self.lastID(self.jointable)
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return None 

    def delete(self, fileId, filenameId):
        self.cursor.execute("""DELETE FROM """+self.jointable+""" WHERE file_id = %s AND filename_id = %s""", (fileId, filenameId))

    def findByFileFilename(self, fileId, filenameId):
        self.cursor.execute("""SELECT * FROM """+self.jointable+""" WHERE file_id = %s AND filename_id = %s""", (fileId, filenameId))
        rs = self.cursor.fetchall()
        return rs

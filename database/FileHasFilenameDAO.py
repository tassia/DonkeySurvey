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
        rs = self.fileHasFilename(fileId, filenameId)
        if not rs:
            query = "INSERT INTO %s(file_id, filename_id) VALUES(%s, %s)" % (self.jointable, fileId, filenameId)
            logging.debug(query)
            self.cursor.execute(query)
        #CommonDAO.lastID(self, self.jointable)

    def delete(self, fileId, filenameId):
        self.cursor.execute("""DELETE FROM """+self.jointable+""" WHERE file_id = %s AND filename_id = %s""", (fileId, filenameId))

    def fileHasFilename(self, fileId, filenameId):
        self.cursor.execute("""SELECT * FROM """+self.jointable+""" WHERE file_id = %s AND filename_id = %s""", (fileId, filenameId))
        rs = self.cursor.fetchall()
        return rs

    #def findByName(self, name):
    #    self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE name = %s""", (name,))
    #    rs = self.cursor.fetchall()
    #    if not rs:
    #        return None
    #    filename = Filename()
    #    for row in rs:
    #        filename.id = row[0]
    #        filename.name = row[1] 
    #    return filename

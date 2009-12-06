import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO

class SourceHasFile(CommonDAO):

    jointable = "source_has_file"

    def __init__(self):
        CommonDAO.__init__(self)
    
    def insertOrUpdate(self, sourceId, fileId, firstSeen):
        rs = self.sourceHasFile(sourceId, fileId)
        if not rs:
            query = "INSERT INTO %s(source_id, file_id, first_seen) VALUES(%d, %d, '%s')" % (self.jointable, sourceId, fileId, firstSeen)
            logging.debug(query)
            self.cursor.execute(query)
        #CommonDAO.lastID(self, self.jointable)

    def delete(self, sourceId, fileId):
        self.cursor.execute("""DELETE FROM """+self.jointable+""" WHERE source_id = %s AND file_id = %s""", (sourceId, fileId))

    def sourceHasFile(self, sourceId, fileId):
        self.cursor.execute("""SELECT * FROM """+self.jointable+""" WHERE source_id = %s AND file_id = %s""", (sourceId, fileId))
        rs = self.cursor.fetchall()
        return rs

    #def findByName(self, name):
    #    self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE name = %s""", (name,))
    #    rs = self.cursor.fetchall()
    #    if not rs:
    #        return None
    #    file = File()
    #    for row in rs:
    #        file.id = row[0]
    #        file.name = row[1] 
    #    return file

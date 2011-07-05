import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO
from datetime import datetime, date, time

class SourceHasFileDAO(CommonDAO):

    jointable = "source_has_file"

    def __init__(self):
        CommonDAO.__init__(self)
    
    def insertOrUpdate(self, sourceId, fileId, availability):
        try:
            rs = self.findBySourceFile(sourceId, fileId)
            if rs is not None:
                queryUpdate = "UPDATE %s SET availability = %s WHERE source_id = %s and file_id = %s" % (self.jointable, availability, sourceId, fileId)
                logging.debug(queryUpdate)
	        self.cursor.execute(queryUpdate) 
            else:
                firstSeen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                queryInsert = "INSERT INTO %s(source_id, file_id, first_seen, availability) VALUES(%s, %s, '%s', %s)" % (self.jointable, sourceId, fileId, firstSeen, availability)
                logging.debug(queryInsert)
                self.cursor.execute(queryInsert)
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return None  
        
        #self.lastID(self.jointable)

    def delete(self, sourceId, fileId):
        self.cursor.execute("""DELETE FROM """+self.jointable+""" WHERE source_id = %s AND file_id = %s""", (sourceId, fileId))

    def findBySourceFile(self, sourceId, fileId):
        query = "SELECT * FROM %s WHERE source_id = %s AND file_id = %s" % (self.jointable, sourceId, fileId)
        logging.debug(query)
        self.cursor.execute(query)
        rs = self.cursor.fetchall()
        if not rs:
            return None
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

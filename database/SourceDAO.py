import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO
from Source import Source

class SourceDAO(CommonDAO):

    tablename = "source"

    def __init__(self):
        CommonDAO.__init__(self)

    def insert(self, source):
        query = "INSERT INTO %s (name, hash, software, osinfo) values('%s', '%s', '%s', '%s')" % (self.tablename, source.name, source.hash, source.software, source.osinfo)
        logging.debug(query)
        self.cursor.execute(query)
        last = self.lastID(self.tablename)
        return last

    def delete(self, id):
        self.cursor.execute("""DELETE FROM """+self.tablename+""" WHERE id = %s""", (id,))

    def find(self, id):
        query = "SELECT * FROM %s WHERE id = %s" % (self.tablename, id)
        self.cursor.execute(query)
        rs = self.cursor.fetchall()
        if not rs:
            return None
        source = Source()
        for row in rs:
            source.id = row[0]
            source.name = row[1] 
            source.hash = row[2] 
            source.software = row[3] 
            source.osinfo = row[4] 
        return source 

    def findByHash(self, hash):
        query = "SELECT * FROM %s WHERE hash = '%s'" % (self.tablename, hash)
        self.cursor.execute(query)
        rs = self.cursor.fetchall()
        if not rs:
            return None
        source = Source()
        for row in rs:
            source.id = row[0]
            source.name = row[1] 
            source.hash = row[2] 
            source.software = row[3] 
            source.osinfo = row[4] 
        return source 

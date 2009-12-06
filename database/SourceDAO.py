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
        query = "INSERT INTO %s(name, hash, software, version, so, availability) values('%s', '%s', '%s', '%s', '%s', %f)" % (self.tablename, source.name, source.hash, source.software, source.version, source.so, source.availability)
        logging.debug(query)
        self.cursor.execute(query)
        last = CommonDAO.lastID(self, self.tablename)
        return last

    def delete(self, id):
        self.cursor.execute("""DELETE FROM """+self.tablename+""" WHERE id = %s""", (id,))

    def find(self, id):
        self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE id = %s""", (id,))
        rs = self.cursor.fetchall()
        source = Source()
        for row in rs:
            source.id = row[0]
            source.name = row[1] 
            source.hash = row[2] 
            source.software = row[3] 
            source.version = row[4] 
            source.so = row[5] 
            source.availability = row[6] 
        return source 

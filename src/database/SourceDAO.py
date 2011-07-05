import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO
from Source import Source

class SourceDAO(CommonDAO):

    tablename = "source"

    def __init__(self):
        CommonDAO.__init__(self)

    def insertOrUpdate(self, source):
        try:
            s = self.findByHash(source.hash)
            if s is not None:
                queryUpdate = "UPDATE %s SET osinfo = '%s' WHERE id = %s" % (self.tablename, source.osinfo, s.id)
                logging.debug(queryUpdate)
                self.cursor.execute(queryUpdate)
                return s.id
            else:
                queryInsert = "INSERT INTO %s (name, hash, software, osinfo) values('%s', '%s', '%s', '%s')" % (self.tablename, source.name, source.hash, source.software, source.osinfo)
                logging.debug(queryInsert)
                self.cursor.execute(queryInsert)
                last = self.lastID(self.tablename)
                return last
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return None  

    def delete(self, id):
        query = "DELETE FROM %s WHERE id = %s" % (self.tablename, id)
        logging.debug(query)
        self.cursor.execute(query)

    def find(self, id):
        query = "SELECT * FROM %s WHERE id = %s" % (self.tablename, id)
        logging.debug(query)
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
        logging.debug(query)
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

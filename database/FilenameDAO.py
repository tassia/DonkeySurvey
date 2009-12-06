import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO
from Filename import Filename

class FilenameDAO(CommonDAO):

    tablename = "filename"

    def __init__(self):
        CommonDAO.__init__(self)
    
    def insert(self, filename):
        query = "INSERT INTO %s(name) VALUES(%s)" % (self.tablename, filename.name)
        logging.debug(query)
        self.cursor.execute(query)
        last = CommonDAO.lastID(self, self.tablename)
        return last

    def insertOrUpdate(self, filename):
        query = "INSERT INTO %s (name) VALUES ('%s')" % (self.tablename, filename.name)
        try:
            fname = self.findByName(filename.name)
            if fname is None:
                logging.debug("INSERT INTO %s(name) VALUES(%s)", self.tablename, filename.name)
                self.cursor.execute(query)
            else:
                return fname.id
            
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return -1
        last = CommonDAO.lastID(self, self.tablename)
        return last

    def delete(self, id):
        self.cursor.execute("""DELETE FROM """+self.tablename+""" WHERE id = %s""", (id,))

    def find(self, id):
        self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE id = %s""", (id,))
        rs = self.cursor.fetchall()
        filename = Filename()
        for row in rs:
            filename.id = row[0]
            filename.name = row[1] 
        return filename

    def findByName(self, name):
        self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE name = %s""", (name,))
        rs = self.cursor.fetchall()
        if not rs:
            return None
        filename = Filename()
        for row in rs:
            filename.id = row[0]
            filename.name = row[1] 
        return filename

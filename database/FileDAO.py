import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO
from File import File

class FileDAO(CommonDAO):

    tablename = "file"

    def __init__(self):
        CommonDAO.__init__(self)

    def insert(self, file):
        try:
            query = "INSERT INTO %s(hash, size, partial_size, best_name) VALUES(%s, %s, %s, %s)" % (self.tablename, file.hash, file.size, file.partialSize, file.bestName);
            logging.debug(query);
            self.cursor.execute(query)
            last = CommonDAO.lastID(self, self.tablename)
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return -1
        return last

    def insertOrUpdate(self, file):
        try:
            f = self.findByHash(file.hash)
            if f is not None:
                if f.partialSize < file.partialSize:
                    self.cursor.execute("""UPDATE """+self.tablename+""" SET partial_size = %s WHERE id = %s""", (file.partialSize, f.id))
                return f.id
            else:
                logging.debug("INSERT INTO "+self.tablename+"(hash, size, partial_size, best_name) VALUES(%s, %s, %s, %s)", file.hash, file.size, file.partialSize, file.bestName);
                self.cursor.execute("""INSERT INTO """+self.tablename+"""(hash, size, partial_size, best_name) VALUES(%s, %s, %s, %s)""", (file.hash, file.size, file.partialSize, file.bestName))
                last = CommonDAO.lastID(self, self.tablename)
                return last
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return -1

    def delete(self, id):
        self.cursor.execute("""DELETE FROM """+self.tablename+""" WHERE id = %s""", (id,))

    def find(self, id):
        self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE id = %s""", (id,))
        rs = self.cursor.fetchall()
        file = File()
        for row in rs:
            file.id = row[0]
            file.hash = row[1] 
            file.size = row[2] 
            file.partialSize = row[3] 
            file.bestName = row[4] 
        return file

    def findByHash(self, hash):
        self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE hash = %s""", (hash,))
        rs = self.cursor.fetchall()
        if not rs:
            return None
        file = File()
        for row in rs:
            file.id = row[0]
            file.hash = row[1] 
            file.size = row[2] 
            file.partialSize = row[3] 
            file.bestName = row[4] 
        return file

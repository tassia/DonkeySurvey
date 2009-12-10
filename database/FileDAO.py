import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO
from File import File
from Filename import Filename
from FilenameDAO import FilenameDAO
from FileHasFilenameDAO import FileHasFilenameDAO

class FileDAO(CommonDAO):

    tablename = "file"

    def __init__(self):
        CommonDAO.__init__(self)

    def insert(self, file):
        try:
	    query = "INSERT INTO %s(hash, size, partial_size, best_name) VALUES('%s', %s, %s, \"%s\")" % (self.tablename, file.hash, file.size, file.partialSize, file.bestName)
            logging.debug(query)
            self.cursor.execute(query)
            last = self.lastID(self.tablename)
            return last
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return None 

    def insertOrUpdate(self, file):
        try:
            f = self.findByHash(file.hash)
            if f is not None:
                if file.filenames:
                    file.id = f.id
                    self.setFileNames(file)
                if f.partialSize < file.partialSize:
                    queryUpdate = "UPDATE %s SET partial_size = %s WHERE id = %s" % (self.tablename, file.partialSize, f.id)
		    logging.debug(queryUpdate)
		    self.cursor.execute(queryUpdate)
                if file.bestName:
                    queryUpdate = "UPDATE %s SET best_name = \"%s\" WHERE id = %s" % (self.tablename, file.bestName, f.id)
                    logging.debug(queryUpdate)
                    self.cursor.execute(queryUpdate)
                return f.id
            else:
	        queryInsert = "INSERT INTO %s(hash, size, partial_size, best_name) VALUES('%s', %s, %s, \"%s\")" % (self.tablename, file.hash, file.size, file.partialSize, file.bestName)
		logging.debug(queryInsert)
		self.cursor.execute(queryInsert)
                last = self.lastID(self.tablename)
                file.id = last
                self.setFileNames(file)
                return last
            
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return None 

    def setFileNames(self, file):
        try:
            fnamedao = FilenameDAO() 
            fhasfnamedao = FileHasFilenameDAO()
            for k,v in file.filenames.iteritems():
                filename = Filename()
                filename.name = v
                filenameId = fnamedao.insertOrUpdate(filename)
                if filenameId is None:
                    logging.debug("Filename is null")
                fhasfnamedao.insertOrUpdate(file.id, filenameId); 

        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return None
    
    def delete(self, id):
        self.cursor.execute("""DELETE FROM """+self.tablename+""" WHERE id = %s""", (id,))

    def find(self, id):
        self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE id = %s""", (id,))
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

    def findByHash(self, hash):
        query = "SELECT * FROM %s WHERE hash = '%s'" % (self.tablename, hash)
        self.cursor.execute(query)
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

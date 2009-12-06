import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO
from Address import Address

class AddressDAO(CommonDAO):

    tablename = "address"

    def __init__(self):
        CommonDAO.__init__(self)
    
    def insert(self, address):
        query = "INSERT INTO %s(ip, port) VALUES('%s', %d)" % (self.tablename, address.ip, address.port)
        logging.debug(query)
        self.cursor.execute(query)
        last = CommonDAO.lastID(self, self.tablename)
        return last

    def insertOrUpdate(self, address):
        query = "INSERT INTO %s(ip, port) VALUES('%s', %d)" % (self.tablename, address.ip, address.port)
        try:
            add = self.findByIpPort(address.ip, address.port)
            if add is None:
                logging.debug(query)
                self.cursor.execute(query)
            else:
                return add.id
            
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
        address = Address()
        for row in rs:
            address.id = row[0]
            address.name = row[1] 
        return address

    def findByIpPort(self, ip, port):
        self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE ip = '%s' and port = %d""", (ip, port))
        rs = self.cursor.fetchall()
        if not rs:
            return None
        address = Address()
        for row in rs:
            address.id = row[0]
            address.ip = row[1] 
            address.port = row[2] 
        return address

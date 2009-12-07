import sys
import logging

sys.path.append('./entities')
from Address import Address
from CommonDAO import CommonDAO

class AddressDAO(CommonDAO):

    tablename = "address"

    def __init__(self):
        CommonDAO.__init__(self)
    
    def insertOrUpdate(self, address):
        add = self.findByIpPort(address.ip, address.port)
        if add is not None:
            queryUpdate = "UPDATE %s SET ip = '%s', port = %s" % (self.tablename, add.ip, add.port)
            self.cursor.execute(queryUpdate)
            return add.id
        else:
	    queryInsert = "INSERT INTO %s(ip, port) VALUES('%s', %s)" % (self.tablename, address.ip, address.port)
            logging.debug(queryInsert)
            self.cursor.execute(queryInsert)
            last = CommonDAO.lastID(self, self.tablename)
            return last

    def delete(self, id):
	query = "DELETE FROM %s WHERE id = %s" % (self.tablename, id)
	self.cursor.execute(query)

    def findByIpPort(self, ip, port):
	query = "SELECT * FROM %s WHERE ip = '%s' AND port = %s" % (self.tablename, ip, port)
	self.cursor.execute(query) 
        rs = self.cursor.fetchall()
        if not rs:
            return None
        address = Address()
        for row in rs:
            address.id = row[0]
            address.ip = row[1]
            address.port = row[2]
        return address 


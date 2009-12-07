import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO

class AddressHasFileDAO(CommonDAO):

    jointable = "address_has_file"

    def __init__(self):
        CommonDAO.__init__(self)
    
    def insertOrUpdate(self, addressId, fileId, firstSeen):
        rs = self.sourceHasFile(addressId, fileId)
        if not rs:
	    query = "INSERT INTO %s(address_id, file_id, first_seen) VALUES(%d, \
                %d, '%s')" % (self.jointable, addressId, fileId, firstSeen)
logging.debug(query)
            self.cursor.execute(query)
        #CommonDAO.lastID(self, self.jointable)

    def delete(self, addressId, fileId):
	self.cursor.execute("""DELETE FROM """+self.jointable+""" WHERE \
            address_id = %s AND file_id = %s""", (addressId, fileId))

    def sourceHasFile(self, addressId, fileId):
	self.cursor.execute("""SELECT * FROM """+self.jointable+""" WHERE \
            address_id = %s AND file_id = %s""", (addressId, fileId)) rs = \
            self.cursor.fetchall()
        return rs


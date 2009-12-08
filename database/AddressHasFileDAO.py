import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO

class AddressHasFileDAO(CommonDAO):

    jointable = "address_has_file"

    def __init__(self):
        CommonDAO.__init__(self)
    
    def insert(self, addressId, fileId):
        try:
            rs = self.findByAddressFile(addressId, fileId)
            if not rs:
                firstSeen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	        query = "INSERT INTO %s(address_id, file_id, first_seen) VALUES(%s, %s,'%s')" % (self.jointable, addressId, fileId, firstSeen)
                logging.debug(query)
                self.cursor.execute(query)
                last = CommonDAO.lastID(self, self.tablename)
                return last 
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return None

        #CommonDAO.lastID(self, self.jointable)

    def delete(self, addressId, fileId):
	query = "DELETE FROM %s WHERE address_id = %s AND file_id = %s" % (self.jointable, addressId, fileId)
	self.cursor.execute(query)

    def findByAddressFile(self, addressId, fileId):
	query = "SELECT * FROM %s WHERE address_id = %s AND file_id = %s" % (self.jointable, addressId, fileId) 
        logging.debug(query)
        self.cursor.execute(query)
        rs = self.cursor.fetchall()
        if not rs:
            return None
        return rs


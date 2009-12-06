import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO
from Ed2kuser import Ed2kuser

class Ed2kuserDAO(CommonDAO):

    tablename = "ed2kuser"

    def __init__(self):
        CommonDAO.__init__(self)

    def insert(self, ed2kuser):
        query = "INSERT INTO %s(hash) values('%s')" % (self.tablename, ed2kuser.hash)
        logging.debug(query)
        self.cursor.execute(query)
        CommonDAO.lastID(self, self.tablename)

    def delete(self, id):
        self.cursor.execute("""DELETE FROM """+self.tablename+""" WHERE id = %s""", (id,))

    def find(self, id):
        self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE id = %s""", (id,))
        rs = self.cursor.fetchall()
        ed2kuser = Ed2kuser()
        for row in rs:
            ed2kuser.id = row[0]
            ed2kuser.hash = row[1] 
        return ed2kuser 

import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO
from Session import Session

class SessionDAO(CommonDAO):

    tablename = "session"

    def __init__(self):
        CommonDAO.__init__(self)

    def insert(self, session):
        query = "INSERT INTO %s(start_date, last_update, downloaded, uploaded, source_id, file_id, address_id) VALUES('%s', '%s', %d, %d, %d, %d, %d)" % (self.tablename, session.startDate, session.lastUpdate, session.downloaded, session.uploaded, session.source.id, session.file.id, session.address.id)
        logging.debug(query);\
        print query
        self.cursor.execute(query)
        session.id = CommonDAO.lastID(self, self.tablename)
        return session.id 

    def delete(self, id):
        self.cursor.execute("""DELETE FROM """+self.tablename+""" WHERE id = %s""", (id,))

    def find(self, id):
        self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE id = %s""", (id,))
        rs = self.cursor.fetchall()
        session = Session()
        for row in rs:
            session.id = row[0]
            session.startDate = row[1] 
            session.lastUpdate = row[2] 
            session.downloaded = row[3] 
            session.uploaded = row[4] 
            session.source.id = row[5] 
            session.file.id = row[6] 
            session.address.id = row[7] 
        return session 

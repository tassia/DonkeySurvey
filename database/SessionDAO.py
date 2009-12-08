import sys
import logging

sys.path.append('./entities')
from CommonDAO import CommonDAO
from Session import Session
from datetime import datetime, date, time

class SessionDAO(CommonDAO):

    tablename = "session"

    def __init__(self):
        CommonDAO.__init__(self)

    def insert(self, session):
        startDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	query = "INSERT INTO %s(start_date, last_update, downloaded, uploaded, \
            source_id, file_id, address_id) VALUES('%s', '%s', %s, %s, %s, %s, %s)" % \
            (self.tablename, startDate, startDate, session.downloaded, \
            session.uploaded, session.source.id, session.file.id, session.address.id)
        try:
            logging.debug(query);
            self.cursor.execute(query)
            session.id = self.lastID(self.tablename)
            return session.id 
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % std(err))
            return None

    def insertOrUpdate(self, session):
        try:
            s = self.findBySourceFileAddress(session.source.id, session.file.id, session.address.id)
            if s is not None:
                lastUpdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                queryUpdate = "UPDATE %s SET last_update = %s, downloaded = %s, uploaded = %s \
                    WHERE id = %s" % (self.tablename, lastUpdate, session.downloaded, \
                    session.uploaded, s.id)
                self.cursor.execute(queryUpdate)
                return s.id
            else:
                startDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                queryInsert = "INSERT INTO %s(start_date, last_update, downloaded, uploaded, \
                    source_id, file_id, address_id) VALUES('%s', '%s', %s, %s, %s, %s, %s)" % \
                    (self.tablename, startDate, startDate, session.downloaded, \
                    session.uploaded, session.source.id, session.file.id, session.address.id)
                logging.debug(queryInsert)
                self.cursor.execute(queryInsert)
                last = self.lastID(self.tablename)
                return last
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
            return None 

    def delete(self, id):
        self.cursor.execute("""DELETE FROM """+self.tablename+""" WHERE id = %s""", (id,))

    def find(self, id):
        self.cursor.execute("""SELECT * FROM """+self.tablename+""" WHERE id = %s""", (id,))
        rs = self.cursor.fetchall()
        session = Session()
        if not rs:
            return None
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

    def findBySourceFileAddress(self, sourceId, fileId, addressId):
        query = "SELECT * FROM %s WHERE source_id = %s and file_id = %s and address_id = %s " % (self.tablename, sourceId, fileId, addressId)
	self.cursor.execute(query)
        rs = self.cursor.fetchall()
        if not rs:
            return None
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

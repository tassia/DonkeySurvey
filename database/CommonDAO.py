import sys
sys.path.append('./entities')
from DBConnection import DefaultDBConnection

###################################################
# Common class to be inherited from all DAO classes
# It holds a connection and a cursor object
###################################################
class CommonDAO:

    connection = None
    cursor = None

    def __init__(self):
        self.connection = DefaultDBConnection()
        self.connection.connect()
        self.cursor = self.connection.getCursor()

    # Get the id from the last inserted row
    def lastID(self, tablename):
        self.cursor.execute("SELECT max(id) as id FROM " + tablename)
        rs = self.cursor.fetchone()
        return rs[0]

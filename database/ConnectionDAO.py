import sys
sys.path.append('./entities')
from CommonDAO import CommonDAO

class ConnectionDAO(CommonDAO):

    tablename = "connection"

    def __init__(self):
        CommonDAO.__init__(self)

    def insert(self, connection):
        self.cursor.execute("""INSERT INTO """+self.tablename+"""(client_name, client_ip, client_port, client_software, client_so, """
                            + """ start_date, end_date, total_transferred, is_download, availability, ed2kuser_id, file_id) """
                            + """VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                            , (connection.clientName, connection.clientIP, connection.clientPort, connection.clientSoftware
                            , connection.clientSO, connection.startDate, connection.endDate, connection.totalTransferred
                            , connection.isDownload, connection.availability, connection.ed2kuser.id, connection.file.id))
        CommonDAO.lastID(self, self.tablename)

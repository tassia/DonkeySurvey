from ConnectionDAO import ConnectionDAO
from Connection import Connection

cdao = ConnectionDAO()
conn = Connection()
conn.clientIP = '123.123.123.123' 
conn.clientPort = 123 
conn.clientName = 'Joca' 
conn.clientSoftware = 'MLDONKEY' 
conn.clientSO = 'Linux'
conn.startDate = '2009-10-10' 
conn.endDate = '2009-10-10' 
conn.ed2kuser.id = 1 
conn.file.id = 1 
cdao.insert(conn)
print conn.id

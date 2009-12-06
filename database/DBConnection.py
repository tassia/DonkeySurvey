import MySQLdb

class _DBConnection(object):
    
    host = '192.168.0.137'
    database = 'donkeysurvey'
    user = 'donkeysurvey'
    password = 'donkeysurvey'
    con = None

    def __init__(self):
        self.instance = "Instance at %d" % self.__hash__()

    def connect(self):
        self.con = MySQLdb.connect(self.host, self.user, self.password)
        self.con.select_db(self.database)

    def getCursor(self):
        return self.con.cursor()
        
_connection = _DBConnection()

def DefaultDBConnection(): 
    return _connection

def DBConnection(host, database, user, password):
    _newConnection = _DBConnection()
    _newConnection.host = host
    _newConnection.database = database
    _newConnection.user = user
    _newConnection.password = password
    return _newConnection

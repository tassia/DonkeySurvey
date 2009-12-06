import MySQLdb

class _Connection(object):
    
    host = 'localhost'
    database = 'donkeystats'
    user = 'vinicius'
    password = '123'
    con = None

    def __init__(self):
        self.instance = "Instance at %d" % self.__hash__()

    def connect(self):
        self.con = MySQLdb.connect(self.host, self.user, self.password)
        self.con.select_db(self.database)

    def getCursor(self):
        #return self.con.cursor(MySQLdb.cursors.DictCursor)
        return self.con.cursor()
        
_connection = _Connection()

def DefaultConnection(): 
    return _connection

def Connection(host, database, user, password):
    _newConnection = _Connection()
    _newConnection.host = host
    _newConnection.database = database
    _newConnection.user = user
    _newConnection.password = password
    return _newConnection

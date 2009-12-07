import MySQLdb

class DBConnection:

    instance = None
    host = '192.168.0.137'
    database = 'donkeysurvey'
    user = 'donkeysurvey'
    password = 'donkeysurvey'
    con = None

    def __init__(self, host, database, user, password):
        self.host
        self.database
        self.user
        self.password

    def setHost(self, host):
        self.host = host

    def setDatabase(self, database):
        self.database = database

    def setUser(self, user):
        self.user = user

    def setPassword(self, password):
        self.password = password

    def setConection(self, connection):
        self.con = connection

    def connect(self):
         self.con = MySQLdb.connect(self.host, self.user, self.password)
         self.con.select_db(self.database)

    def getCursor(self):
        return self.con.cursor()


    class SingletonHelper :

        def __call__( self, *args, **kw ) :

            # If an instance of TestSingleton does not exist,
            # create one and assign it to TestSingleton.instance.

            if DBConnection.instance is None :
                object = DBConnection()
                DBConnection.instance = object

            # Return TestSingleton.instance, which should contain
            # a reference to the only instance of TestSingleton
            # in the system.

            return DBConnection.instance

    getInstance = SingletonHelper()

    def __init__( self ) :

        # Optionally, you could go a bit further to guarantee
        # that no one created more than one instance of TestSingleton:

        if not DBConnection.instance == None :
            raise RuntimeError, 'Only one instance of DBConnection is allowed!'


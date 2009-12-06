import unittest
import sys
sys.path.append('../')
sys.path.append('../entities')

from SessionDAO import SessionDAO
from Session import Session

class InsertSessionTestCase(unittest.TestCase):

    id = None;

    def runTest(self):
        fdao = FilenameDAO()
        file = Filename()
        file.name = 'test'
        fid = fdao.insert(file)
        self.id = file.id
        assert self.id != None, 'error inserting filename'

    def tearDown(self):
        fdao = FilenameDAO()
        fdao.delete(self.id)

suite = unittest.makeSuite(InsertFilenameTestCase,'test')
runner = unittest.TextTestRunner()
runner.run(suite)

sdao = SessionDAO()
session = Session()
session.clientIP = '123.123.123.123' 
session.clientPort = 123 
session.clientName = 'Joca' 
session.clientSoftware = 'MLDONKEY' 
session.clientSO = 'Linux'
session.startDate = '2009-10-10' 
session.endDate = '2009-10-10' 
session.ed2kuser.id = 1 
session.file.id = 1 
sdao.insert(session)
print session.id

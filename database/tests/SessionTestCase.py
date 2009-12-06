import unittest
import sys
sys.path.append('../')
sys.path.append('../entities')

from SessionDAO import SessionDAO
from Session import Session

class SessionTestCase(unittest.TestCase):

    id = None;

    def testInsert(self):
        sdao = SessionDAO()
        session = Session()
        session.startDate = '2009-10-10' 
        session.lastUpdate = '2009-10-10' 
        session.source.id = 1 
        session.file.id = 1 
        session.address.id = 1 
        self.id = sdao.insert(session)
        assert self.id != None, 'error inserting session'

    def testSelect(self):
        sdao = SessionDAO()
        session = Session()
        session.startDate = '1500-04-22' 
        session.lastUpdate = '2009-10-10' 
        session.source.id = 1 
        session.file.id = 1 
        session.address.id = 1 
        sid = sdao.insert(session)
        session = sdao.find(sid)
        sdao.delete(session.id)
        assert session.startDate == '1500-04-22', 'error selecting file'
 
    def tearDown(self):
        sdao = SessionDAO()
        sdao.delete(self.id)

suite = unittest.TestSuite()
suite.addTest(SessionTestCase("testSelect"))
suite.addTest(SessionTestCase("testInsert"))

runner = unittest.TextTestRunner()
runner.run(suite)

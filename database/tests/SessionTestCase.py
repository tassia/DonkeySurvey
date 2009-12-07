import unittest
import sys
sys.path.append('../')
sys.path.append('../entities')

from SessionDAO import SessionDAO
from Session import Session

class SessionTestCase(unittest.TestCase):

    sourceId = 0
    fileId = 0
    addressId = 0

    def testInsert(self):
        sdao = SessionDAO()
        session = Session()
        session.startDate = '2009-10-10' 
        session.lastUpdate = '2009-10-10' 
        session.source.id = self.sourceId
        session.file.id = self.fileId
        session.address.id = self.addressId
        sid = sdao.insert(session)
        assert sid != -1, 'error inserting session'

    def testSelect(self):
        sdao = SessionDAO()
        session = sdao.findBySourceFileAddress(self.sourceId, self.fileId, self.addressId)
        s = sdao.find(session.id)
        assert s is not None, 'error selecting session'
 
    def testDelete(self):
        sdao = SessionDAO()
        session = sdao.findBySourceFileAddress(self.sourceId, self.fileId, self.addressId)
        sdao.delete(session.id)
        s = sdao.find(session.id)
        assert s is None, 'error deleting session'

suite = unittest.TestSuite()
suite.addTest(SessionTestCase("testInsert"))
suite.addTest(SessionTestCase("testSelect"))
suite.addTest(SessionTestCase("testDelete"))

runner = unittest.TextTestRunner()
runner.run(suite)

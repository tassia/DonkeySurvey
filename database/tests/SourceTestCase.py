import unittest
import sys
sys.path.append('../')
sys.path.append('../entities')

from SourceDAO import SourceDAO
from Source import Source

class SourceTestCase(unittest.TestCase):

    hash = 'fake_hash_3453k24j5hk234j5h32kj5kjb345'

    def testInsert(self):
        sdao = SourceDAO()
        source = Source()
        source.name = 'zezinho'
        source.hash = self.hash 
        source.software = 'mldonkey 3.1.2'
        source.osinfo = 'Linux'
        sid = sdao.insert(source)
        assert sid != -1, 'error inserting source'
        
 
    def testSelect(self):
        sdao = SourceDAO()
        source = sdao.findByHash(self.hash) 
        s = sdao.find(source.id)
        assert s is not None, 'error selecting source'
   
    def testDelete(self):
        sdao = SourceDAO()
        source = sdao.findByHash(self.hash)
        sdao.delete(source.id)
        s = sdao.find(source.id)
        assert s is None, 'error deleting source'

suite = unittest.TestSuite()
suite.addTest(SourceTestCase("testInsert"))
suite.addTest(SourceTestCase("testSelect"))
suite.addTest(SourceTestCase("testDelete"))

#unittest.main("SourceTestCase.suite")

runner = unittest.TextTestRunner()
runner.run(suite)

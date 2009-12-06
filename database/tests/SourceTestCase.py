import unittest

import sys
sys.path.append('../')
sys.path.append('../entities')

from SourceDAO import SourceDAO
from Source import Source

class SourceTestCase(unittest.TestCase):

    id = None;

    def testInsert(self):
        sdao = SourceDAO()
        s = Source()
        s.name = 'zezinho'
        s.hash = '394cyawjchq2s7687s6d8f7s8d7f6sdf'
        s.software = 'mldonkey'
        s.version = '3.1.2'
        s.so = 'Linux'
        s.availability = 0.2
        self.id = sdao.insert(s)
        sdao.delete(self.id)
        assert self.id != None, 'error inserting source'
        
 
    def testSelect(self):
        sdao = SourceDAO()
        s = Source()
        s.name = 'test'
        s.hash = '394cyawjchq2s7687s6d8f7s8d7f6sdf'
        s.software = 'mldonkey'
        s.version = '3.1.2'
        s.so = 'Linux'
        s.availability = 0.2

        sid = sdao.insert(s)
        e = sdao.find(s.id)
        sdao.delete(s.id)
        assert s.name == 'test', 'error selecting filename'
   
    def tearDown(self):
        sdao = SourceDAO()
        sdao.delete(self.id)

suite = unittest.TestSuite()
suite.addTest(SourceTestCase("testSelect"))
suite.addTest(SourceTestCase("testInsert"))

#unittest.main("SourceTestCase.suite")

runner = unittest.TextTestRunner()
runner.run(suite)

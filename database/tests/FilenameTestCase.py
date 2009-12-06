import unittest
import sys
sys.path.append('../')
sys.path.append('../entities')

from FilenameDAO import FilenameDAO
from Filename import Filename
 
class FilenameTestCase(unittest.TestCase):

    id = None;


    def testInsert(self):
        fdao = FilenameDAO()
        file = Filename()
        file.name = 'test'
        fid = fdao.insert(file)
        self.id = file.id
        fdao.delete(self.id)
        assert self.id != None, 'error inserting filename'
        
 
    def testSelect(self):
        fdao = FilenameDAO()
        file = Filename()
        file.name = 'test'
        fid = fdao.insert(file)
        f = fdao.find(file.id)
        fdao.delete(file.id)
        assert f.name == 'test', 'error selecting filename'
   
    def tearDown(self):
        fdao = FilenameDAO()
        fdao.delete(self.id)


suite = unittest.TestSuite()
suite.addTest(FilenameTestCase("testSelect"))
suite.addTest(FilenameTestCase("testInsert"))

#suite = unittest.makeSuite(FilenameTestCase,'test')
runner = unittest.TextTestRunner()
runner.run(suite)

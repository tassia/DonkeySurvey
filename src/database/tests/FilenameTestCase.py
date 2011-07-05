import unittest
import sys

sys.path.append('../')
sys.path.append('../entities')

from FilenameDAO import FilenameDAO
from Filename import Filename
 
class FilenameTestCase(unittest.TestCase):

    name = 'impossible.name-vinicius.pinheiro.tassia.camoes.beraldo.leal' 

    def testInsert(self):
        fdao = FilenameDAO()
        file = Filename()
        file.name = self.name 
        fid = fdao.insert(file)
        assert fid != -1, 'error inserting filename'
        
 
    def testSelect(self):
        fdao = FilenameDAO()
        file = fdao.findByName(self.name)
        f = fdao.find(file.id)
        assert f is not None, 'error selecting filename'
   
    def testDelete(self):
        fdao = FilenameDAO()
        file = fdao.findByName(self.name)
        fdao.delete(file.id)
        f = fdao.find(file.id)
        assert f is None, 'error deleting filename'

suite = unittest.TestSuite()
suite.addTest(FilenameTestCase("testInsert"))
suite.addTest(FilenameTestCase("testSelect"))
suite.addTest(FilenameTestCase("testDelete"))

#suite = unittest.makeSuite(FilenameTestCase,'test')
runner = unittest.TextTestRunner()
runner.run(suite)

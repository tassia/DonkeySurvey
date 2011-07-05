import unittest
import sys
sys.path.append('../')
sys.path.append('../entities')

from FileDAO import FileDAO
from FilenameDAO import FilenameDAO
from File import File
from Filename import Filename
 
class FileTestCase(unittest.TestCase):

    hash = 'qwertyuiop'

    def testInsert(self):
        fdao = FileDAO()
        file = File()
        file.hash = self.hash
        file.size = 555555 
        file.partialSize = 55555
        file.bestname = 'nomedoarquivonarede.ext'
        fid = fdao.insert(file)
        assert fid != -1, 'error inserting file'
 
    def testSelect(self):
        fdao = FileDAO()
        file = fdao.findByHash(self.hash)
        f = fdao.find(file.id)
        assert f is not None, 'error selecting file'

    def testInsertOrUpdate(self):
        fdao = FileDAO()
        file = fdao.findByHash(self.hash)
        file.partialSize = 100000 
        fid = fdao.insertOrUpdate(file)
        assert file.id == fid, 'error updating file'

    def testDelete(self):
        fdao = FileDAO()
        file = fdao.findByHash(self.hash)
        fdao.delete(file.id)
        f = fdao.find(file.id)
        assert f is None, 'error deleting file'
        
suite = unittest.TestSuite()
suite.addTest(FileTestCase("testInsert"))
suite.addTest(FileTestCase("testSelect"))
suite.addTest(FileTestCase("testInsertOrUpdate"))
suite.addTest(FileTestCase("testDelete"))

runner = unittest.TextTestRunner()
runner.run(suite)

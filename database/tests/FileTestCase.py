import unittest
import sys
sys.path.append('../')
sys.path.append('../entities')

from FileDAO import FileDAO
from FilenameDAO import FilenameDAO
from File import File
from Filename import Filename
 
class FileTestCase(unittest.TestCase):

    id = None;


    def testInsert(self):
        fdao = FileDAO()
        file = File()
        file.hash = '34ce3rf'
        file.size = 523434
        file.partialSize = 52372
        file.bestName = 'nomeDoArquivoNaRede.ext'
        fid = fdao.insert(file)
        self.id = file.id
        fdao.delete(self.id)
        assert self.id != None, 'error inserting file'
 
#    def testInsertFilename(self):
#        fdao = FileDAO()
#        file = File()
#        file.hash = '34ce3rf'
#        file.size = 523434
#        file.partialSize = 52372
#        file.bestName = 'nomeDoArquivoNaRede.ext'
#        fid = fdao.insert(file)
#
#        fnamedao = FilenameDAO()
#        filename = Filename()
#        filename.name = 'test'
#        fnameid = fnamedao.insert(filename)
#            
#        fdao.insertFilename(file, filename)

 
    def testSelect(self):
        fdao = FileDAO()
        file = File()
        file.hash = '65f4gs'
        fid = fdao.insert(file)
        f = fdao.find(file.id)
        fdao.delete(file.id)
        assert f.hash == '65f4gs', 'error selecting file'
   
    def tearDown(self):
        fdao = FileDAO()
        fdao.delete(self.id)


suite = unittest.TestSuite()
suite.addTest(FileTestCase("testSelect"))
suite.addTest(FileTestCase("testInsert"))
#suite.addTest(FileTestCase("testInsertFilename"))

runner = unittest.TextTestRunner()
runner.run(suite)

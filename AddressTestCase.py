import unittest
import sys
sys.path.append('../')
sys.path.append('../entities')

from AddressDAO import AddressDAO
from Address import Address
 
class AddressTestCase(unittest.TestCase):

    id = None;


    def testInsert(self):
        adao = AddressDAO()
        address = Address()
        address.ip = '192.168.0.1'
        address.port = 3567
        aid = adao.insert(address)
        self.id = aid
        adao.delete(self.id)
        assert self.id != None, 'error inserting address'
        
 
    def testSelect(self):
        adao = AddressDAO()
        address = Address()
        address.ip = '192.168.255.255'
        address.port = 3567
        aid = adao.insert(address)
        a = adao.find(aid)
        adao.delete(aid)
        assert a.ip == '192.168.255.255', 'error selecting address'
   
    def tearDown(self):
        adao = AddressDAO()
        adao.delete(self.id)

suite = unittest.TestSuite()
suite.addTest(AddressTestCase("testSelect"))
suite.addTest(AddressTestCase("testInsert"))

#suite = unittest.makeSuite(AddressTestCase,'test')
runner = unittest.TextTestRunner()
runner.run(suite)

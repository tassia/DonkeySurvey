import unittest
import sys

sys.path.append('../')
sys.path.append('../entities')

from AddressDAO import AddressDAO
from Address import Address
 
class AddressTestCase(unittest.TestCase):

    ip = '666.666.666.666'
    port = 6666

    def testInsert(self):
        adao = AddressDAO()
        address = Address()
        address.ip = self.ip 
        address.port = self.port 
        aid = adao.insertOrUpdate(address)
        assert aid != None, 'error inserting address'
        
    def testSelect(self):
        adao = AddressDAO()
        address = adao.findByIpPort(self.ip, self.port)
        a = adao.find(address.id)
        assert a is not None, 'error selecting address'
   
    def testDelete(self):
        adao = AddressDAO()
        address = adao.findByIpPort(self.ip, self.port)
        adao.delete(address.id)
        a = adao.find(address.id)
        assert a is None, 'error deleting address'

suite = unittest.TestSuite()
suite.addTest(AddressTestCase("testInsert"))
suite.addTest(AddressTestCase("testSelect"))
suite.addTest(AddressTestCase("testDelete"))

#suite = unittest.makeSuite(AddressTestCase,'test')
runner = unittest.TextTestRunner()
runner.run(suite)

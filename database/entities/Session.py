from Source import Source
from File import File
from Address import Address

class Session:

    id = None;
    startDate = None
    lastUpdate = None
    downloaded = 0
    uploaded = 0
    source = Source()
    file = File()
    address = Address() 

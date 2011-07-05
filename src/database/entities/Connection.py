from Ed2kuser import Ed2kuser
from File import File

class Connection:

    id = None;
    clientName = ''
    clientIP = ''
    clientPort = 0
    clientSoftware = ''
    clientSO = ''
    startDate = None
    endDate = None
    totalTransferred = 0
    isDownload = 0
    availability = 0.00
    ed2kuser = Ed2kuser()
    file = File()

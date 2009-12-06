from FilenameDAO import FilenameDAO
from Filename import Filename

fdao = FilenameDAO()
file = Filename()
file.name = 'teste'
fid = fdao.insert(file)
print file.id

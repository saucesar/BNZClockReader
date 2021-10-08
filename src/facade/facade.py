import sys,time
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), 'models')))
sys.path.insert(0, abspath(join(dirname(__file__), 'database')))
from models._models import Spreadsheet as Excel
from models._models import KeyValue
from read_afd import ReadAFDFile
from database.create_tables import *

class Facade:
    def __init__(self) -> None:
        pass

    def read_afd(self, afd_file_path, progressBar):
        try:
            afd_path = KeyValue.get(KeyValue.key == KeyValue.AFD_FILE_PATH).value
        except:
            afd_path = afd_file_path

        readADF = ReadAFDFile(afd_file_path=afd_path, progressBar=progressBar)
        readADF.read_and_save_in_database()
import sys,time
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), 'models')))
from models._models import Spreadsheet as Excel
from models._models import KeyValue
from read_afd import ReadAFDFile
from database.create_tables import *
from models._models import Spreadsheet as Excel

class Facade:
    def __init__(self) -> None:
        pass

    def read_afd(self, afd_file_path, progressBar):
        ReadAFDFile(afd_file_path=afd_file_path, progressBar=progressBar).read_and_save_in_database()
    
    def create_spreadsheet(self, month, year, progressBar = None):
        if not progressBar is None:
            progressBar.update(50)
        Excel().save_month_db_spreadsheet(int(year), int(month))
        if not progressBar is None:
            progressBar.update(100)
    
    def save_afd_file_path(self, afd_path):
        try:
            KeyValue.create(key=KeyValue.AFD_FILE_PATH, value=self.file_path)
        except:
            kv = KeyValue.get(KeyValue.key == KeyValue.AFD_FILE_PATH)
            kv.value = afd_path
            kv.save()
    
    def get_afd_file_path(self):
        return KeyValue.get(KeyValue.key == KeyValue.AFD_FILE_PATH).value
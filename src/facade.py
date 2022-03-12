import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), 'models')))
from models._models import Spreadsheet as Excel
from models._models import KeyValue
from models._models import Employee
from read_afd import ReadAFDFile
from database.create_tables import *

class Facade:

    def read_afd(self, afd_file_path, progressBar):
        ReadAFDFile(afd_file_path=afd_file_path, progressBar=progressBar).read_and_save_in_database()
    
    def create_spreadsheet(self, start_date, final_date, destiny_folder, progressBar = None):
        if not progressBar is None:
            progressBar.update(50)
        Excel().save_period_db_spreadsheet(start_date, final_date, destiny_folder)
        if not progressBar is None:
            progressBar.update(100)
    
    def save_afd_file_path(self, afd_path):
        try:
            KeyValue.create(key=KeyValue.AFD_FILE_PATH, value=afd_path)
        except:
            kv = KeyValue.get(KeyValue.key == KeyValue.AFD_FILE_PATH)
            kv.value = afd_path
            kv.save()
    
    def get_afd_file_path(self):
        try:
            return KeyValue.get(KeyValue.key == KeyValue.AFD_FILE_PATH).value
        except:
            return ''

    def save_spreadsheet_folder(self, spreadsheet_folder):
        try:
            KeyValue.create(key=KeyValue.DEFAULT_SPREADSHEET_FOLDER, value=spreadsheet_folder)
        except:
            kv = KeyValue.get(KeyValue.key == KeyValue.DEFAULT_SPREADSHEET_FOLDER)
            kv.value = spreadsheet_folder
            kv.save()
    
    def get_spreadsheet_folder(self):
        try:
            return KeyValue.get(KeyValue.key == KeyValue.DEFAULT_SPREADSHEET_FOLDER).value
        except:
            return ''
        
    def get_employees(self):
        return Employee.all_to_list()
    
    def get_auto_read(self):
        try:
            return KeyValue.get(KeyValue.key == KeyValue.AUTOREAD_AFD_FILE).value == 'True'
        except:
            KeyValue.create(key=KeyValue.AUTOREAD_AFD_FILE, value=True)
            return True
    
    def set_auto_read(self, value):
        try:
            kv = KeyValue.get(KeyValue.key == KeyValue.AUTOREAD_AFD_FILE)
            kv.value = value
            kv.save()
        except:
            KeyValue.create(key=KeyValue.AUTOREAD_AFD_FILE, value=True)
            return True
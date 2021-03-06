import sys,time
from datetime import datetime
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), 'models')))
sys.path.insert(0, abspath(join(dirname(__file__), 'exceptions')))
from models._models import *
from exceptions.peewee_exceptions import *
from log.log_config import *

class ReadAFDFile:
    def __init__(self, afd_file_path, progressBar = None) -> None:
        self.file_path = afd_file_path
        self.progressBar = progressBar
        self.open_afd_file()
        self.afd_file = self.open_afd_file()
        if(self.afd_file is None):
            raise Exception('Arquivo afd não encontrado!')
        
    def open_afd_file(self):
        try:
            afd_file = open(self.file_path, 'r')
            logging.info("OPEN FILE: "+self.file_path)
            return afd_file
        except Exception as e:
            logging.error('EXCEPTION: '+ e.__class__.__name__+' MESSAGE:  '+e.__str__())

    def close_afd_file(self):
        try:
            self.afd_file.close()
            logging.info("CLOSE FILE: "+self.file_path)
        except Exception as e:
            logging.error('EXCEPTION: '+ e.__class__.__name__+' MESSAGE:  '+e.__str__())

    def get_afd_lines_key_value(self):
        try:
            return KeyValue.get(KeyValue.key == KeyValue.AFD_LINES_READED_COUNT_KEY)
        except:
            kv = KeyValue.create(key=KeyValue.AFD_LINES_READED_COUNT_KEY, value='0')
            logging.info('CREATED LINES_READED')
            return kv
    
    def create_employee(self, line):
        try:
            name = line[35:].strip()
            pis = line[24:35]

            if not name.isnumeric() and pis.isnumeric():
                Employee.create(name=name, pis=pis)

            return True
        except Exception as e:
            logging.error('EXCEPTION: '+ e.__class__.__name__+' MESSAGE:  '+e.__str__())
            return False

    def create_time_clock_marking(self, line):    
        pis = line[23:34]
        date = {'y':int(line[14:18]), 'm':int(line[12:14]),"d":int(line[10:12])}
        time = line[18:20]+":"+line[20:22]
    
        try:
            ep = Employee.get(Employee.pis==pis)
            tc = TimeClockMarking.get(TimeClockMarking.date == datetime(date['y'], date['m'], date['d']), TimeClockMarking.employee == ep)
            if tc.first_exit is None:
                tc.first_exit = time
            elif tc.second_entry is None:
                tc.second_entry = time
            elif tc.second_exit is None:
                tc.second_exit = time
            tc.save()
        except Exception as e:
            try:
                TimeClockMarking.create(date=datetime(date['y'], date['m'], date['d']), first_entry=time, pis=pis, employee=ep)
            except UnboundLocalError:
                pass
            logging.error('EXCEPTION: '+ e.__class__.__name__+' MESSAGE:  '+e.__str__())
    
    def start_time_count(self):
        logging.info('START TIME COUNT: '+datetime.now().__str__());
        self.time_start = time.time()
    
    def end_time_count(self):
        self.time_end = time.time()
        diff_in_seconds = self.time_end - self.time_start
        minutes = int(diff_in_seconds/60)
        logging.info('END TIME COUNT: '+datetime.now().__str__());
        if minutes > 0:
            return str(minutes)+" minutes "+str(round(diff_in_seconds%60, 2))+" seconds"
        else:
            return str(round(diff_in_seconds%60, 2))+" seconds"
    
    def jump_lines(self, amount):
        j = 0
        while(j < amount):
            self.afd_file.readline()
            j += 1

    def read_and_save_in_database(self):
        file_line_amount = self.afd_file.readlines().__len__()
        kv_lines = self.get_afd_lines_key_value()
        
        try:
            KeyValue.create(key=KeyValue.AFD_FILE_PATH, value=self.file_path)
        except:
            pass

        lines_count = int(kv_lines.value)

        self.afd_file.seek(0)
        self.jump_lines(lines_count)
        percent_count = 0
        
        for line in self.afd_file.readlines():
            lines_count += 1
            percent_count += 1
            
            if not self.progressBar is None:
                percent = (lines_count/file_line_amount*100)
                self.progressBar.update(current_count=percent)
            
            try:
                kv_lines.value = lines_count
                kv_lines.save()
            except Exception as e:
                logging.error('EXCEPTION: '+ e.__class__.__name__+' MESSAGE:  '+e.__str__())

            if(line.__len__() > 35):
                self.create_employee(line) 

            if line.__len__() == 35:
                self.create_time_clock_marking(line)

        self.close_afd_file()
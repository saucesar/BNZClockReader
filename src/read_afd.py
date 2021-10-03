import sys
import peewee
from datetime import datetime
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), 'models')))
from models._models import *
from log.log_config import *

file_name = "/home/cesars/Dropbox/Arquivos/Projects/BNZClockPoint/AFD00009003650016557.txt"
file = open(file_name, 'r')
pis_search = "  "
logging.info("OPEN FILE: "+file_name)

for line in file.readlines():

    if(line.__len__() > 35):
        
        name = line[35:].strip()
        pis = line[24:35]

        if not name.isnumeric() and pis.isnumeric():
            try:
                Employee.create(name=name, pis=pis)
            except peewee.IntegrityError as e:
                logging.error(e)

    if line.__len__() == 35:
        pis = line[23:34]
        date = line[14:18]+"/"+line[12:14]+"/"+line[10:12]
        time = line[18:20]+":"+line[20:22]

        try:
            e = Employee.get(Employee.pis==pis)
            TimeClockMarking.create(time=time,date=datetime.strptime(date, '%Y/%m/%d'), pis=pis, employee=e)
        except:
            print('EXCEPTION')

file.close()
logging.info("CLOSE FILE: "+file_name)

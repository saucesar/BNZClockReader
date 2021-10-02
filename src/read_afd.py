from models.employee import Employee
import logging

logging.basicConfig(format='%(levelname)s %(asctime)s : %(message)s', level=logging.DEBUG)

file_name = "/home/cesars/Dropbox/Arquivos/Projects/BNZClockPoint/AFD00009003650016557.txt"
file = open(file_name, 'r')
pis = "20753507018"
logging.info("OPEN FILE: "+file_name)
count = 0
for line in file.readlines():
    if(line.__len__() > 35):
        pis = line[24:35]
        name = line[35:].strip()
            
        if not name.isnumeric():
            Employee.create(name, pis)
    if line.__len__() == 35 and pis in line:
        date = line[10:12]+"/"+line[12:14]+"/"+line[14:18]
        time = line[18:20]+":"+line[20:22]
        print(date, time)
        if(count == 10):
            break
    count+=1
file.close()
logging.info("CLOSE FILE: "+file_name)

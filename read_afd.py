from src.models.employee import Employee

file_name = "/home/cesars/Dropbox/Arquivos/Projects/BNZClockPoint/AFD00009003650016557.txt"
file = open(file_name, 'r')
count = 0
for line in file.readlines():
    if(line.__len__() > 35):
        pis = line[24:35]
        name = line[35:].strip()
            
        if not name.isnumeric():
            print(pis, name, name.__len__())
    elif line.__len__() == 35 and "20753507018" in line:
        date = line[10:12]+"/"+line[12:14]+"/"+line[14:18]
        time = line[18:20]+":"+line[20:22]
        print(date, time)
        if(count == 10):
            break

file.close()
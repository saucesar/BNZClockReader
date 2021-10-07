import os

class BuildExecutable:
    
    def __init__(self) -> None:
        if os.name == 'nt':
            os.system('pyinstaller src/main.py src/database/create_tables.py src/read_afd.py '+\
                      'src/models/_imports.py src/models/_models.py src/models/_openpyxl.py src/models/_peewee_orm.py --onefile')    
        else:
            os.system('pyinstaller src/main.py src/database/create_tables.py src/read_afd.py src/models/*.py  --onefile')
        #os.system('ls')

if __name__ == '__main__':
    BuildExecutable()

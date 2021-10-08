import os

class BuildExecutable:
    
    WINDOWS = 'nt'
    LINUX = 'posix'
    
    def __init__(self) -> None:
        if os.name == BuildExecutable.LINUX:
            os.system('pip3 install pyinstaller')
            os.system('pyinstaller src/main.py src/database/create_tables.py src/read_afd.py src/models/*.py -n ClockReader --clean --onefile')
        if os.name == BuildExecutable.WINDOWS:
            os.system('pip install pyinstaller')
            os.system('pyinstaller src/main.py src/database/create_tables.py src/read_afd.py '+\
                      'src/models/_imports.py src/models/_models.py src/models/_openpyxl.py src/models/_peewee_orm.py -n ClockReader --clean --onefile')    
        else:
            os.system('echo "OS not supported."')

if __name__ == '__main__':
    BuildExecutable()

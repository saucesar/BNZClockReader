import os, sys

class BuildExecutable:
    
    WINDOWS = 'nt'
    LINUX = 'posix'
    
    def __init__(self) -> None:
        try:
            mode = sys.argv[1]
        except:
            mode = '--gui'
        
        if mode == '--gui':
            self.gui()
        elif mode == '--cli':
            self.cli()
        else:
            print('Opção inválida')
        sys.exit(0)

    def gui(self):
        if os.name == BuildExecutable.LINUX:
            os.system('pip3 install pyinstaller')
            os.system('pyinstaller src/menu.py src/database/create_tables.py src/models/*.py -n ClockReader --clean --onefile')
            os.system('mkdir dist/src/')
            os.system('cp -r src/assets dist/src/assets')
        elif os.name == BuildExecutable.WINDOWS:
            os.system('pip install pyinstaller')
            os.system('pyinstaller src/menu.py src/database/create_tables.py src/models/_imports.py src/models/_models.py '+\
                      'src/models/_openpyxl.py src/models/_peewee_orm.py -n ClockReader --clean --onefile')
            os.system('mkdir dist/src/')
            os.system('copy src\\assets\\* dist\\src\\assets')
        else:
            os.system('echo "OS not supported."')

    def cli(self):
        if os.name == BuildExecutable.LINUX:
            os.system('pip3 install pyinstaller')
            os.system('pyinstaller src/*.py src/database/*.py src/models/*.py -n ClockReader --clean --onefile')
        elif os.name == BuildExecutable.WINDOWS:
            os.system('pip install pyinstaller')
            os.system('pyinstaller src/main.py src/database/create_tables.py src/read_afd.py '+\
                      'src/models/_imports.py src/models/_models.py src/models/_openpyxl.py src/models/_peewee_orm.py -n ClockReader --clean --onefile')    
        else:
            os.system('echo "OS not supported."')

if __name__ == '__main__':
    BuildExecutable()

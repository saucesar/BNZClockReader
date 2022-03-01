import os, sys
from unicodedata import name

class BuildExecutable:
    
    WINDOWS = 'nt'
    LINUX = 'posix'
    
    def __init__(self) -> None:
        self.install_dependencies()

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
            os.system('pyinstaller src/menu.py src/database/create_tables.py src/log/*.py src/models/*.py -n ClockReader --noconsole --clean --onefile')
            os.system('mkdir logs')
            os.system('mkdir -p dist/src/')
            os.system('cp -r src/assets dist/src/assets')
        elif os.name == BuildExecutable.WINDOWS:
            os.system('pip install pyinstaller')
            os.system('pyinstaller src/menu.py src/facade.py src/read_afd.py '+\
                      'src/database/create_tables.py src/exceptions/peewee_exceptions.py src/log/log_config.py '+\
                      'src/models/_imports.py src/models/_models.py src/models/_openpyxl.py src/models/_peewee_orm.py '+\
                      '-n ClockReader --clean --onefile')
        else:
            os.system('echo "OS not supported."')

    def cli(self):
        if os.name == BuildExecutable.LINUX:
            os.system('pyinstaller src/*.py src/database/*.py src/models/*.py -n ClockReader --clean --onefile')
        elif os.name == BuildExecutable.WINDOWS:
            os.system('pyinstaller src/main.py src/database/create_tables.py src/read_afd.py '+\
                      'src/models/_imports.py src/models/_models.py src/models/_openpyxl.py src/models/_peewee_orm.py -n ClockReader --clean --onefile')    
        else:
            os.system('echo "OS not supported."')
    
    def install_dependencies(self):
        pip = ('pip3' if os.name == BuildExecutable.LINUX else 'pip')
        os.system('{} install pysimplegui'.format(pip))
        os.system('{} install rich'.format(pip))
        os.system('{} install openpyxl'.format(pip))
        os.system('{} install peewee'.format(pip))

if __name__ == '__main__':
    BuildExecutable()

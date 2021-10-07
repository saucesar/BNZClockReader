import os

class BuildExecutable:
    
    def __init__(self) -> None:
        os.system('pyinstaller src/main.py src/database/create_tables.py src/read_afd.py src/models/*.py  --onefile')
        #os.system('ls')

if __name__ == '__main__':
    BuildExecutable()
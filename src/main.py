import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), 'models')))
from models._models import Spreadsheet as Excel
from read_afd import ReadAFDFile
from rich import print
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

class Main:
    
    def __init__(self) -> None:
        self.console = Console()       
        self.layout = Layout(name="Menu")
        msg = "=========================================================\n 1 - Ler Arquide AFD\n99 - Sair\n========================================================="
        options = Layout(name='Opções', renderable=self.create_panel_option(msg))
        self.layout.split_row(options, Layout(name='Example'))

    def create_panel_option(self, option):
        return Panel(Text(option))

    def read_afd(self):
        self.console.log("[green]Lendo arquivo AFD\n")
        readADF = ReadAFDFile('/home/cesars/Dropbox/Arquivos/Projects/BNZClockPoint/AFD00009003650016557.txt')
        readADF.read_and_save_in_database()
        self.console.log('\n')

    def show(self):
        print(self.layout)
        self.console.log("Menu!")
    
    def exit(self):
        print(Panel('[red]Exit', title='Bye Bye!', subtitle='Come back again!'))

if __name__ == '__main__':
    main = Main()
    
    while True:
        main.show()
        option = input('Opção: ')
        if option == '1':
            main.read_afd()
        if option == '99':
            main.exit()
            break
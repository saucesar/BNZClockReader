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
        msg = "1 - Ler Arquide AFD\n2 - Gerar Planilha de Marcações\n99 - Sair\n"
        options = Layout(name='Opções', renderable=self.create_panel_option(msg))
        self.layout.split_row(options, Layout(name=''))

    def create_panel_option(self, option):
        return Panel(Text(option))

    def read_afd(self):
        afd_path = input('Caminho do Arquivo AFD: ')
        self.console.log("[green]Lendo arquivo AFD\n")
        readADF = ReadAFDFile(afd_path)
        readADF.read_and_save_in_database()
        self.console.log('\n')

    def create_spreadsheet(self):
        month = input('Mês (de 1 a 12): ')
        year =input('Ano (com 4 dígitos): ')
        excel = Excel()
        excel.save_month_db_spreadsheet(int(year), int(month))
        
    def show(self):
        print(self.layout)
    
    def exit(self):
        print(Panel('[red]Saindo!', title='Até breve!', subtitle='Volte sempre!'))

if __name__ == '__main__':
    main = Main()
    
    while True:
        main.show()
        option = input('Opção: ')
        if option == '1':
            main.read_afd()
        if option == '2':
            main.create_spreadsheet()
        if option == '99':
            main.exit()
            break

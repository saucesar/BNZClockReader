import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), 'models')))
sys.path.insert(0, abspath(join(dirname(__file__), 'database')))
from models._models import Spreadsheet as Excel
from models._models import KeyValue
from read_afd import ReadAFDFile
from database.create_tables import *
from rich import print
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from time import sleep

class Main:
    
    def __init__(self) -> None:
        self.console = Console()       
        self.layout = Layout(name="Menu")
        msg = "1  - Ler Arquide AFD\n2  - Gerar Planilha de Marcações\n3  - Alterar caminho do arquivo AFD\n99 - Sair\n"
        options = Layout(name='Opções', renderable=self.create_panel_option(msg))
        self.layout.split_row(options, Layout(name='', renderable= self.create_panel_option('')))
        TableManager().create_tables()

    def create_panel_option(self, option):
        return Panel(Text(option))

    def read_afd(self):
        try:
            try:
                afd_path = KeyValue.get(KeyValue.key == KeyValue.AFD_FILE_PATH).value
            except:
                afd_path = input('Caminho do Arquivo AFD: ')
            self.console.log("[green]Lendo arquivo AFD\n")
            readADF = ReadAFDFile(afd_path)
            readADF.read_and_save_in_database()
            self.console.log('\n')
        except AttributeError:
            print(Panel('[red]Arquivo inválido!', title='Erro!', subtitle='tente novamente!'))
            sleep(3)
    
    def create_spreadsheet(self):
        month = input('Mês (de 1 a 12): ')
        year =input('Ano (com 4 dígitos): ')
        excel = Excel()
        excel.save_month_db_spreadsheet(int(year), int(month))
    
    def change_afd_file_path(self):
        try:
            kv = KeyValue.get(KeyValue.key == KeyValue.AFD_FILE_PATH)
            print("[green]Arquivo atual: {}".format(kv.value))
            path = input('Novo caminho do arquivo AFD: ')
            if path.isspace() or path == '':
                print(Panel('[red]Arquivo inválido!', title='Erro!', subtitle='tente novamente!'))
                sleep(3)
            else:
                kv.value = path
                kv.save()
                print("[green]Arquivo modificado: {}".format(kv.value))
                sleep(3)
        except:
            print(Panel('[red]Arquivo inválido!', title='Erro!', subtitle='tente novamente!'))
            sleep(3)

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
        elif option == '2':
            main.create_spreadsheet()
        elif option == '3':
            main.change_afd_file_path()
        elif option == '99':
            main.exit()
            sys.exit(0)
            break

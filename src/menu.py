import sys
import PySimpleGUI as sg
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
sys.path.insert(0, abspath(join(dirname(__file__), 'database')))
from main import Main
from facade import Facade
from datetime import datetime
from database.create_tables import TableManager

class MenuScreen:
    def __init__(self) -> None:
        sg.theme('Tan')
        self.layout = self.get_layout()
        self.title = 'Clock Reader'
        self.window = self.get_window()
        self.main = Main()
        self.facade = Facade()
        TableManager().create_tables()
    
    def get_window(self):
        return sg.Window(self.title, self.layout, size=(600, 500), margins=(100, 50), location=(400,100), element_justification='c',resizable=True,finalize=True)

    def show(self):
        while True:
            event, values = self.window.read()
            if event == 'readAFDFile':
                ReadAFDScreen(main=self.main, facade=self.facade).show()
            if event == 'createSpreadsheet':
                CreateSpreadsheet(main=self.main, facade=self.facade).show()
            if event == 'exit' or event == sg.WIN_CLOSED:
                break
        self.window.close()

    def get_layout(self):
        layout = [
            [
                sg.Button('', key='readAFDFile', tooltip='Ler Arquivo AFD', size=(20, 10), image_filename='src/assets/file3-96px.png'),
                sg.Button('', key='createSpreadsheet', tooltip='Gerar Planilha', size=(20, 10), image_filename='src/assets/excel-96px.png'),
                sg.Button('', key='exit', tooltip='Sair do Sistema', size=(20,10), image_filename='src/assets/exit2-96px.png'),
            ],
            [ sg.Image(source='src/assets/clock2.png', size=(100,100),key="image", expand_x=True, expand_y=True)],
            [ sg.Text(text='- Geração planilhas', font=("Helvetica", 20)) ],
            [ sg.Text(text='- Calculo de horários', font=("Helvetica", 20)) ],
            [ sg.Text(text='- Erros de ponto', font=("Helvetica", 20)) ],
        ]
        return layout
    
    def oKbutton(self, btn_key='ok', btn_tooltype = ''):
        return sg.Button('', key=btn_key, tooltip=btn_tooltype, image_filename='src/assets/confirm-96px.png')
    
    def exitButton(self, btn_key='exit', btn_tooltype = ''):
        return sg.Button('', key=btn_key, tooltip=btn_tooltype, image_filename='src/assets/exit3-96px.png')

class ReadAFDScreen(MenuScreen):
    def __init__(self, main = None, facade = None) -> None:
        if not main is None and not facade is None:
            self.layout = self.get_layout()
            self.title = 'ADF Read Screen'
            self.window = self.get_window()
            self.main = main
            self.facade = facade
        else:
            raise Exception('ReadAFDScreen - Infome o main e a facade')

    def show(self):
        while True:
            event, values = self.window.read()
            if event == 'ok':
                if values['afd_file'] != '':
                    self.window['progressBar'].update(visible=True, current_count=0)
                    self.window.Element('progressText').update('Lendo arquivo... Aguarde...')
                    sg.popup_notify(title='Lendo arquivo, aguarde ...', display_duration_in_ms=1500)
                    self.facade.read_afd(values['afd_file'], self.window['progressBar'])
                else:
                    sg.popup_error('Selecione o arquivo AFD')
            if event == 'exit':
                break
            if  event == sg.WIN_CLOSED:
                sys.exit(0)

        self.window.close()

    def get_layout(self):
        layout = [
            [sg.Text(text="Leitura de arquivo AFD",font=30)],
            [
                sg.Text(text="Selecione o arquivo AFD: "),
                sg.FileBrowse(button_text='Selecione',key='afd_file', tooltip='Arquivo AFD', ),
            ],
            [sg.ProgressBar(100, key='progressBar', visible=False, size=(30,30), bar_color=('green', 'gray'),)],
            [sg.Text(text="", key='progressText')],
            [
                self.oKbutton(btn_tooltype='Pressione ok Para ler o arquivo'),
                self.exitButton(btn_tooltype='Sair desta tela.'),
            ],
        ]
        return layout

class CreateSpreadsheet(MenuScreen):
    months = {'Janeiro':1, 'Fevereiro':2, 'Março':3, 'Abril':4, 'Maio':5, 'Junho':6, 'Julho':7,'Agosto':8,'Setembro':9,'Outubro':10,'Novembro':11, 'Dezembro':12}

    def __init__(self, main = None, facade = None) -> None:
        if not main is None and not facade is None:
            sg.theme('Tan')
            self.layout = self.get_layout()
            self.title = 'Create Spreadsheet'
            self.window = self.get_window()
            self.main = main
            self.facade = facade
        else:
            raise Exception('CreateSpreadsheet - Infome o main e a facade')

    def show(self):
        while True:
            event, values = self.window.read()
            if event == 'ok':
                try:
                    year = int(values['year'][0])
                    month = CreateSpreadsheet.months[values['month'][0]]
                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(month, year, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada', display_duration_in_ms=3000, location=(500,100))
                except:
                    sg.popup_notify(title='Selecione o Mês e o Ano', location=(500, 200))
            if event == 'exit' or event == sg.WIN_CLOSED:
                break
        self.window.close()
        
    def get_layout(self):
        date =  datetime.now()
        months = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
        layout = [
            [sg.Text("Selecione o período",font=('Times', 20))],
            [
                sg.Listbox(key='month',values= months, default_values=[months[date.month-1]], size=(20, 12)),
                sg.Listbox(key='year',values=range(2018, date.year+1), default_values=[date.year,], size=(20, 12))
            ],
            [sg.ProgressBar(100, key='progressBar', visible=False, bar_color=('green', 'gray'), size=(30,30))],
            [
                self.oKbutton(btn_tooltype='Pressione ok para gerar a planilha'),
                self.exitButton(btn_tooltype='Sair desta tela.'),
            ]
        ]
        return layout

if __name__ == '__main__':
    MenuScreen().show()

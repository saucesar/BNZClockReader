import sys
from PySimpleGUI.PySimpleGUI import Slider
import PySimpleGUI as sg
from main import Main
from facade import Facade
from datetime import datetime

class MenuScreen:
    def __init__(self) -> None:
        sg.theme('Tan')
        self.layout = self.get_layout()
        self.window = self.get_window()
        self.main = Main()
        self.facade = Facade()
    
    def get_window(self):
        window = sg.Window('Clock Reader', self.layout, size=(600, 500))
        return window

    def show(self):
        while True:
            event, values = self.window.read()
            if event == 'Ler Arquivo AFD':
                ReadAFDScreen(main=self.main, facade=self.facade).show()
            if event == 'Gerar planilha \nde marcações':
                CreateSpreadsheet(main=self.main, facade=self.facade).show()
            if event == 'Saír' or event == sg.WIN_CLOSED:
                self.window.close()
                break
            print(values)

    def get_layout(self):
        layout = [
            [
                sg.Button('Ler Arquivo AFD', size=(20, 10)),
                sg.Button('Gerar planilha \nde marcações', size=(20, 10)),
                sg.Button('Saír', size=(20,10)),
            ],
        ]
        return layout

class ReadAFDScreen:
    def __init__(self, main = None, facade = None) -> None:
        if not main is None and not facade is None:
            sg.theme('Tan')
            self.layout = self.get_layout()
            self.window = self.get_window()
            self.main = main
            self.facade = facade
        else:
            raise Exception('ReadAFDScreen - Infome o main e a facade')
        
    def get_window(self):
        window = sg.Window('ADF Read Screen', self.layout, size=(600, 300))
        return window

    def show(self):
        while True:
            event, values = self.window.read()
            if event == 'Ok':
                if values['afd_file'] != '': 
                    self.window.Element('progressText').update('Lendo arquivo... Aguarde...')
                    sg.popup_notify(title='Lendo arquivo, aguarde ...', display_duration_in_ms=3000)
                    self.facade.read_afd(values['afd_file'], self.window['progressBar'])
                else:
                    sg.popup_error('Selecione o arquivo AFD')
            if event == 'Saír':
                self.window.close()
                break
            if event == sg.WIN_CLOSED:
                sys.exit(0)
            print(values)

    def get_layout(self):
        layout = [
            [sg.Text(text="Leitura de arquivo AFD",font=30)],
            [sg.Text(text="Selecione o arquivo AFD: "), sg.FileBrowse(button_text='Selecione',key='afd_file')],
            [sg.ProgressBar(100, key='progressBar', size=(20,20)), sg.Text(text="", key='progressText')],
            [sg.Button('Ok'), sg.Button('Saír')],
        ]
        return layout

class CreateSpreadsheet:
    def __init__(self, main = None, facade = None) -> None:
        if not main is None and not facade is None:
            sg.theme('Tan')
            self.layout = self.get_layout()
            self.window = self.get_window()
            self.main = main
            self.facade = facade
        else:
            raise Exception('CreateSpreadsheet - Infome o main e a facade')
        
    def get_window(self):
        window = sg.Window('Create Spreadsheet', self.layout, size=(600, 300))
        return window

    def show(self):
        while True:
            event, values = self.window.read()
            if event == 'Ok':
                self.facade.create_spreadsheet(int(values['month']), int(values['year']), self.window['progressBar'])
                sg.popup_notify(title='Planilha gerada', display_duration_in_ms=3000)
            if event == 'Saír':
                self.window.close()
                break
            if event == sg.WIN_CLOSED:
                sys.exit(0)
            print(values)

    def get_layout(self):
        date =  datetime.now()
        layout = [
            [sg.Text("O período",font=30)],
            [sg.Text("Mês: "), Slider(range=(1, 12), default_value=date.month, key='month', orientation='h')],
            [sg.Text("Ano: "), Slider(range=(2000, date.year), default_value=date.year, key='year', orientation='h')],
            [sg.ProgressBar(100, key='progressBar', size=(20,20))],
            [sg.Button('Ok'), sg.Button('Saír')],
        ]
        return layout

if __name__ == '__main__':
    menu = MenuScreen()
    menu.show()

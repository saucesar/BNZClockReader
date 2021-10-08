import sys
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
sys.path.insert(0, abspath(join(dirname(__file__), 'facade')))
import PySimpleGUI as sg
from main import Main
from facade.facade import Facade


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
            if event == 'Saír' or event == sg.WIN_CLOSED:
                self.window.close()
                break
            print(values)

    def get_layout(self):
        layout = [
            [
                sg.Button('Ler Arquivo AFD', size=(20, 10)),
            ],
            [
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
            raise Exception('Infome o main e a facade')
        
    def get_window(self):
        window = sg.Window('Clock Reader', self.layout, size=(600, 300))
        return window

    def show(self):
        while True:
            event, values = self.window.read()
            if event == 'Ok':
                if values['afd_file'] != '': 
                    self.facade.read_afd(values['afd_file'], self.window['progressBar'])
                else:
                    sg.popup_error('Selecione o arquivo AFD')
            if event == 'Saír' or event == sg.WIN_CLOSED:
                self.window.close()
                break
            print(values)

    def get_layout(self):
        layout = [
            [sg.Text("Opções disponíveis",font=30)],
            [sg.Text("Selecione o arquivo AFD: "), sg.FileBrowse(button_text='Selecione',key='afd_file')],
            [sg.ProgressBar(100, key='progressBar', size=(20,20))],
            [sg.Button('Ok'), sg.Button('Saír')],
        ]
        return layout

if __name__ == '__main__':
    menu = MenuScreen()
    menu.show()

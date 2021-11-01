from re import split
import sys,os
import PySimpleGUI as sg
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
sys.path.insert(0, abspath(join(dirname(__file__), 'database')))
from facade import Facade
from datetime import datetime
from database.create_tables import TableManager

class Screen:
    def show(self):
        sg.popup_notify(title='Implement Show in {}'.format(self.__class__.__name__), display_duration_in_ms=1000, location=(500,100))

    def show_notifycation(self, msg, duration_in_seconds=1):
        sg.popup_notify(title=msg, display_duration_in_ms=duration_in_seconds*1000, location=(500,100))

    def show_error(self, msg, duration_in_seconds=1):
        sg.popup_notify(title=msg, display_duration_in_ms=duration_in_seconds*1000, location=(500,100))

    def set_size(self, size=(700, 500)):
        return size

    def get_window(self):
        return sg.Window(self.title, self.layout, size=self.set_size(), margins=(50, 50), location=(300,100), element_justification='c', resizable=True, finalize=True)

    def oKbutton(self, btn_key='ok', btn_tooltype = ''):
        return sg.Button('', key=btn_key, tooltip=btn_tooltype, image_filename='src/assets/confirm-96px.png')
    
    def exitButton(self, btn_key='exit', btn_tooltype = ''):
        return sg.Button('', key=btn_key, tooltip=btn_tooltype, image_filename='src/assets/exit3-96px.png')

class MenuScreen(Screen):

    READ_AFD_FILE = 'Ler Arquivo AFD'
    CHANGE_AFD_PATH = 'Alterar arquivo AFD'
    CHOOSE_SPREADSHEET_PATH = 'Alterar pasta destino de Planilhas'
    ABOUT = 'Sobre'
    CREATE_SPREADSHEET = 'Gerar Planilha'
    EXIT = 'Sair'

    def __init__(self) -> None:
        #sg.theme('Tan')
        #sg.theme("Dark Blue 3")
        #sg.theme("DarkBlack")
        #sg.theme("DefaultNoMoreNagging")
        #sg.theme("LightBrown1")
        #sg.theme("LightGray")
        sg.theme("Reddit")
        self.layout = self.get_layout()
        self.title = 'Clock Reader'
        self.window = self.get_window()
        self.facade = Facade()
        TableManager().create_tables()
    
    def show(self):
        while True:
            event, values = self.window.read()
            if event == MenuScreen.READ_AFD_FILE:
                ReadAFDScreen(facade=self.facade).show()
            elif event == MenuScreen.CREATE_SPREADSHEET:
                CreateSpreadsheet(facade=self.facade).show()
            elif event == MenuScreen.CHOOSE_SPREADSHEET_PATH:
                FolderSelect(facade=self.facade).show()
            elif event == MenuScreen.CHANGE_AFD_PATH:
                self.change_afd_file_path()
            elif event == MenuScreen.ABOUT:
                self.show_about()
            elif event == 'exit' or event == sg.WIN_CLOSED or event == MenuScreen.EXIT:
                break

        self.window.close()

    def show_about(self):
        sg.popup('About this program', 'Version 1.0', 'PySimpleGUI rocks...', location=(500,100))

    def change_afd_file_path(self):
        try:
            afd_path = FileSelect(facade=self.facade).show()
            if afd_path == '' or afd_path is None:
                pass
            else:
                self.facade.save_afd_file_path(afd_path)
                self.show_error('Modificação salva\n Novo arquivo:{}'.format(afd_path))
        except Exception as e:
            sg.popup_error()
            self.show_notifycation(e.__str__())

    def get_layout(self):
        menu_options = [
            ['Menu', [ MenuScreen.READ_AFD_FILE, MenuScreen.CHANGE_AFD_PATH, MenuScreen.CHOOSE_SPREADSHEET_PATH, MenuScreen.CREATE_SPREADSHEET, MenuScreen.ABOUT, MenuScreen.EXIT],],
        ]

        layout = [
            [ sg.Menu(menu_options) ],
            [
                sg.Button('', key=MenuScreen.READ_AFD_FILE, tooltip='Ler Arquivo AFD', size=(20, 10), image_filename='src/assets/file3-96px.png'),
                sg.Button('', key=MenuScreen.CHANGE_AFD_PATH, tooltip='Alterar arquivo AFD', size=(20, 10), image_filename='src/assets/change-file-96px.png'),
                sg.Button('', key=MenuScreen.CREATE_SPREADSHEET, tooltip='Gerar Planilha', size=(20, 10), image_filename='src/assets/excel-96px.png'),
                sg.Button('', key=MenuScreen.CHOOSE_SPREADSHEET_PATH, tooltip='Selecionar pasta destino de Planilhas', size=(20, 10), image_filename='src/assets/folder-96px.png'),
                sg.Button('', key=MenuScreen.EXIT, tooltip='Sair do Sistema', size=(20,10), image_filename='src/assets/exit2-96px.png'),
            ],
            [ sg.Image(source='src/assets/clock2.png', size=(100,100),key="image", expand_x=True, expand_y=True)],
            [ sg.Text(text='- Geração planilhas', font=("Helvetica", 20)) ],
            [ sg.Text(text='- Calculo de horários', font=("Helvetica", 20)) ],
            [ sg.Text(text='- Erros de ponto', font=("Helvetica", 20)) ],
        ]
        return layout

class ReadAFDScreen(Screen):

    def __init__(self, facade = None) -> None:
            self.layout = self.get_layout()
            self.title = 'ADF Read Screen'
            self.window = self.get_window()
            self.facade = facade
            self.file_path = self.get_afd_path()

    def set_size(self, size=(600, 250)):
        return super().set_size(size=size)

    def show(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break

        self.window.close()

    def get_afd_path(self):
            try:
                afd_path = self.facade.get_afd_file_path()
            except:
                file_select = FileSelect(facade=self.facade)
                afd_path = file_select.show()

                if afd_path == '' or afd_path is None:
                    file_select.window.close()

            if afd_path == '' or afd_path is None:
                self.window.close()
            else:
                self.window.Element('progressBar').update(visible=True, current_count=0)
                self.show_notifycation('Lendo arquivo, por favor aguarde ...')
                self.facade.read_afd(afd_path, self.window['progressBar'])
                self.facade.save_afd_file_path(afd_path)
                self.show_notifycation('Leitura do arquivo concluída.')
                self.window.close()

    def get_layout(self):
        return [
            [sg.Text(text="Leitura de arquivo AFD",font=30)],
            [sg.ProgressBar(100, key='progressBar', visible=False, size=(30,30), bar_color=('green', 'gray'),)],
        ]

class FileSelect(Screen):
    
    def __init__(self, facade = None) -> None:
        self.layout = self.get_layout()
        self.title = 'Seleção de Arquivo'
        self.window = self.get_window()
        self.facade = facade

    def show(self):
        while True:
            event, values = self.window.read()

            if event == 'ok':
                if values['afd_file'] == '' or values['afd_file'] is None:
                    sg.popup_notify(title='Selecione o arquivo', location=(500, 200))
                else:
                    self.window.close()
                    return values['afd_file']
            if event == 'exit' or event == sg.WIN_CLOSED:
                self.window.close()
                return None
            
    def get_layout(self):
        return [
            [sg.Text(text="Seleção de Arquivo",font=30)],
            [
                sg.Text(text="Selecione o arquivo AFD: "),
                sg.FileBrowse(button_text='Selecione', key='afd_file', tooltip='Arquivo AFD', ),
            ],
            [
                self.oKbutton(btn_tooltype='Pressione ok Para ler o arquivo'),
                self.exitButton(btn_tooltype='Sair desta tela.'),
            ],
        ]

class FolderSelect(Screen):
    
    def __init__(self, facade = None) -> None:
        self.layout = self.get_layout()
        self.title = 'Pasta padrão para planilhas'
        self.window = self.get_window()
        self.facade = facade

    def show(self):
        while True:
            event, values = self.window.read()
            if event == 'ok':
                if values['spreadsheet_path'] == '' or values['spreadsheet_path'] is None:
                    self.show_error('Selecione uma pasta.')
                else:
                    self.facade.save_spreadsheet_folder(values['spreadsheet_path'])
                    self.show_notifycation('Pasta padrão selecionada.')
                    break

            elif event == 'exit' or event == sg.WIN_CLOSED:
                break

        self.window.close()

    def get_layout(self):
        return [
            [sg.Text(text="Selecione a Pasta",font=30)],
            [
                sg.Text(text="Selecione a pasta: "),
                sg.FolderBrowse(button_text='Selecione', key='spreadsheet_path', tooltip='Salvar a planilha em ...', ),
            ],
            [
                self.oKbutton(btn_tooltype='Selecionar esta pasta'),
                self.exitButton(btn_tooltype='Sair desta tela.'),
            ],
        ]
        
class CreateSpreadsheet(Screen):

    months = {'Janeiro':1, 'Fevereiro':2, 'Março':3, 'Abril':4, 'Maio':5, 'Junho':6, 'Julho':7,'Agosto':8,'Setembro':9,'Outubro':10,'Novembro':11, 'Dezembro':12}

    def __init__(self,facade = None) -> None:
        self.layout = self.get_layout()
        self.title = 'Gerar Planilha'
        self.window = self.get_window()
        self.facade = facade

    def show(self):
        while True:
            event, values = self.window.read()

            if event == 'ok':
                destiny_folder = self.facade.get_spreadsheet_folder()
                
                if destiny_folder == '' or destiny_folder is None:
                    FolderSelect(self.facade).show()
                    destiny_folder = self.facade.get_spreadsheet_folder()

                try:
                    start_split = split('/', values['start_date'])
                    final_split = split('/', values['final_date'])
                    
                    start_date = {'day':int(start_split[0]),'month':int(start_split[1]),'year':int(start_split[2])}
                    final_date = {'day':int(final_split[0]),'month':int(final_split[1]),'year':int(final_split[2])}
                        
                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(start_date, final_date, destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(destiny_folder), display_duration_in_ms=3000, location=(500,100))
                except:
                    pass
                    #self.show_error('Selecione o periodo corretamente.')

            elif event == 'exit' or event == sg.WIN_CLOSED:
                break

        self.window.close()
        
    def get_layout(self):
        date =  datetime.now()
        months = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']

        return [
            [sg.Text("Selecione mês e ano",font=('Times', 20))],
            [
                #sg.Listbox(key='month',values=months, default_values=[months[date.month-1]], size=(20, 12)),
                #sg.Listbox(key='year',values=range(2018, date.year+1), default_values=[date.year,], size=(20, 12)),
                [sg.InputText(key='start_date', size=(20,1)), sg.CalendarButton('Data Inicial', size=(10,1), title='Inicial', target='start_date', format='%d/%m/%Y')],
                [sg.InputText(key='final_date', size=(20,1)), sg.CalendarButton('Data Final', size=(10,1), title='Final', target='final_date', format='%d/%m/%Y')],
            ],
            [sg.ProgressBar(100, key='progressBar', visible=False, bar_color=('green', 'gray'), size=(30,30))],
            [
                self.oKbutton(btn_tooltype='Pressione ok para gerar a planilha'),
                self.exitButton(btn_tooltype='Sair desta tela.'),
            ]
        ]

if __name__ == '__main__':
    MenuScreen().show()

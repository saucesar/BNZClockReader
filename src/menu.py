from re import split
import sys
import PySimpleGUI as sg
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
sys.path.insert(0, abspath(join(dirname(__file__), 'database')))
from facade import Facade
from datetime import date, timedelta
from database.create_tables import TableManager
from calendar import monthrange

class Screen:

    ASSET_VERSION='v2'

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
        return sg.Button('', key=btn_key, tooltip=btn_tooltype, image_filename=f'src/assets/{Screen.ASSET_VERSION}/confirm-96px.png')
    
    def exitButton(self, btn_key='exit', btn_tooltype = ''):
        return sg.Button('', key=btn_key, tooltip=btn_tooltype, image_filename=f'src/assets/{Screen.ASSET_VERSION}/exit3-96px.png')

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
        #sg.theme("SystemDefaultForReal")
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
                sg.Button('', key=MenuScreen.READ_AFD_FILE, tooltip='Ler Arquivo AFD', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/file3-96px.png'),
                sg.Button('', key=MenuScreen.CHANGE_AFD_PATH, tooltip='Alterar arquivo AFD', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/change-file-96px.png'),
                sg.Button('', key=MenuScreen.CREATE_SPREADSHEET, tooltip='Gerar Planilha', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/excel-96px.png'),
                sg.Button('', key=MenuScreen.CHOOSE_SPREADSHEET_PATH, tooltip='Selecionar pasta destino de Planilhas', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/folder-96px.png'),
                sg.Button('', key=MenuScreen.EXIT, tooltip='Sair do Sistema', size=(20,10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/exit2-96px.png'),
            ],
            [ sg.Image(source=f'src/assets/{Screen.ASSET_VERSION}/clock2.png', size=(100,100),key="image", expand_x=True, expand_y=True)],
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
                #self.show_notifycation('Lendo arquivo, por favor aguarde ...')
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
    
    def set_size(self, size=(500, 300)):
        return super().set_size(size=size)

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
        
    def set_size(self, size=(500, 300)):
        return super().set_size(size=size)

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

    TODAY = 'Hoje'
    YESTERDAY = 'Ontem'
    LAST_WEEK = 'Ultima Semana'
    MONTH = 'Mes'

    def __init__(self,facade = None) -> None:
        self.layout = self.get_layout()
        self.title = 'Gerar Planilha'
        self.window = self.get_window()
        self.facade = facade

    def show(self):
        while True:
            event, values = self.window.read()
            destiny_folder = self.facade.get_spreadsheet_folder()
            try:
                if event == 'ok':
                    
                    if destiny_folder == '' or destiny_folder is None:
                        FolderSelect(self.facade).show()
                        destiny_folder = self.facade.get_spreadsheet_folder()

                    start_date = self.date_to_dict(values['start_date'])
                    final_date = self.date_to_dict(values['final_date'])
                            
                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(start_date, final_date, destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(destiny_folder), display_duration_in_ms=3000, location=(500,100))

                elif event == CreateSpreadsheet.MONTH:
                    start_date =  self.date_to_dict(date.today().replace(day=1).__str__(), '-', year_index=0, day_index=2)
                    final_date =  self.date_to_dict(date.today().replace(day=monthrange(start_date['year'], start_date['month'])[1]).__str__(), '-', year_index=0, day_index=2)

                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(start_date, final_date, destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(destiny_folder), display_duration_in_ms=3000, location=(500,100))
        
                elif event == CreateSpreadsheet.TODAY:
                    today =  self.date_to_dict(date.today().__str__(), '-', year_index=0, day_index=2)

                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(today, today, destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(destiny_folder), display_duration_in_ms=3000, location=(500,100))

                elif event == CreateSpreadsheet.YESTERDAY:
                    yeasterday =  self.date_to_dict((date.today() - timedelta(days=1)).__str__(), '-', year_index=0, day_index=2)

                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(yeasterday, yeasterday, destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(destiny_folder), display_duration_in_ms=3000, location=(500,100))

                elif event == CreateSpreadsheet.LAST_WEEK:
                    start = date.today() - timedelta(days=date.today().weekday()) - timedelta(days=7)
                    final = date.today() - timedelta(days=date.today().weekday()) - timedelta(days=1)
                    start_date = self.date_to_dict(start.__str__(), '-', year_index=0, day_index=2)
                    final_date = self.date_to_dict(final.__str__(), '-', year_index=0, day_index=2)

                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(start_date, final_date, destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(destiny_folder), display_duration_in_ms=3000, location=(500,100))

                elif event == 'exit' or event == sg.WIN_CLOSED:
                    break

            except Exception as e:
                self.show_error(e.__str__())

        self.window.close()

    def date_to_dict(self, date, split_char='/', day_index=0, month_index=1, year_index=2):
        date_split = split(split_char, date)
        return {'day':int(date_split[day_index]), 'month':int(date_split[month_index]), 'year':int(date_split[year_index])}

    def get_layout(self):
        return [
            [sg.HorizontalSeparator()],
            [sg.Text('Opções Rápidas',font=('Times', 20))],
            [
                sg.Button('', key=CreateSpreadsheet.MONTH, tooltip='Mês Atual', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/calendar/month.png'),
                sg.Button('', key=CreateSpreadsheet.TODAY, tooltip='Hoje', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/calendar/today.png'),
                sg.Button('', key=CreateSpreadsheet.YESTERDAY, tooltip='Ontem', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/calendar/yesterday.png'),
                sg.Button('',key=CreateSpreadsheet.LAST_WEEK, tooltip='Semana Anterior', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/calendar/last_week.png'),
            ],
            [sg.ProgressBar(100, key='progressBar', visible=False, bar_color=('green', 'gray'), size=(30,30))],
            [sg.HorizontalSeparator()],
            [sg.Text("Selecione o período desejado",font=('Times', 20))],
            [
                [sg.InputText(key='start_date', size=(20,1), disabled=True), sg.CalendarButton('Data Inicial', size=(10,1), title='Inicial', target='start_date', format='%d/%m/%Y')],
                [sg.InputText(key='final_date', size=(20,1), disabled=True), sg.CalendarButton('Data Final', size=(10,1), title='Final', target='final_date', format='%d/%m/%Y')],
            ],
            [
                self.oKbutton(btn_tooltype='Pressione ok para gerar a planilha'),
                self.exitButton(btn_tooltype='Sair desta tela.'),
            ],
            [sg.HorizontalSeparator()],
        ]

if __name__ == '__main__':
    MenuScreen().show()

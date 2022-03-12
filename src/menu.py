from re import split
import sys
import PySimpleGUI as sg
from os.path import dirname, join, abspath
import logging
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
sys.path.insert(0, abspath(join(dirname(__file__), 'database')))
from facade import Facade
from datetime import date, timedelta
from database.create_tables import TableManager
from calendar import monthrange

class Screen:

    ASSET_VERSION='v2'

    def show(self):
        sg.popup_notify(title='Implement Show in {}'.format(self.__class__.__name__), display_duration_in_ms=1000, location=(600, 100))

    def show_notifycation(self, msg, duration_in_seconds=1):
        sg.popup_notify(title=msg, display_duration_in_ms=duration_in_seconds*1000, location=(600, 100))

    def show_error(self, msg, duration_in_seconds=1):
        sg.popup_notify(title=msg, display_duration_in_ms=duration_in_seconds*1000, location=(600, 100))

    def set_size(self, size=(700, 600)):
        return size

    def get_window(self):
        return sg.Window(self.title, self.layout, size=self.set_size(), margins=(50, 50), location=(400, 50), element_justification='c', resizable=True, finalize=True)

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
    EMPLOYEES = 'Funcionários'
    EXIT = 'Sair'
    CONFIG = 'Configurações'

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
        if self.facade.get_auto_read():
            self.read_afd_file()
    
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
            elif event == MenuScreen.EMPLOYEES:
                EmployeeMenu(self.facade).show()
            elif event == MenuScreen.CONFIG:
                ConfigScreen(self.facade).show()
            elif event == 'exit' or event == sg.WIN_CLOSED or event == MenuScreen.EXIT:
                sys.exit(0)

    def show_about(self):
        sg.popup('Sobre este software', 'Versão 1.0.0', 'Desenvolvido por Saú Cesar<sau.cesarlima2013@gmail.com>', location=(600,100))

    def change_afd_file_path(self):
        try:
            afd_path = FileSelect(facade=self.facade).show()
            if afd_path == '' or afd_path is None:
                pass
            else:
                self.facade.save_afd_file_path(afd_path)
                self.show_error('Modificação salva\n Novo arquivo:{}'.format(afd_path))
        except Exception as e:
            logging.error(e.__str__())
            sg.popup_error()
            self.show_notifycation(e.__str__())

    def read_afd_file(self):
        try:    
            afd_path = self.facade.get_afd_file_path()
            
            if not afd_path in ['', None]:
                progressBar = self.window.Element('progressBar')
                progressBarText = self.window.Element('progressBarText')

                self.show_notifycation('Lendo arquivo AFD.')
                
                progressBar.update(visible=True, current_count=0)
                progressBarText.update(visible=True)
                
                self.facade.read_afd(afd_path, self.window['progressBar'])
                self.facade.save_afd_file_path(afd_path)
                self.show_notifycation('Leitura do arquivo concluída.')

                progressBar.update(visible=False, current_count=0)
                progressBarText.update(visible=False)
            else:
                ReadAFDScreen(self.facade).show()
        except Exception as e:
            logging.error(e.__str__())
            if e.__class__.__name__ == 'KeyValueDoesNotExist':
                ReadAFDScreen(self.facade, True).show()

    def get_layout(self):
        menu_options = [
            [
                'Menu',
                [
                    MenuScreen.CONFIG, MenuScreen.READ_AFD_FILE, MenuScreen.CHANGE_AFD_PATH,
                    MenuScreen.CHOOSE_SPREADSHEET_PATH, MenuScreen.CREATE_SPREADSHEET, MenuScreen.ABOUT, MenuScreen.EXIT
                ],
            ],
        ]

        layout = [
            [ sg.Menu(menu_options) ],
            [
                sg.Button('', key=MenuScreen.READ_AFD_FILE, tooltip='Ler Arquivo AFD', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/file3-96px.png'),
                sg.Button('', key=MenuScreen.CHANGE_AFD_PATH, tooltip='Alterar arquivo AFD', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/change-file-96px.png'),
                sg.Button('', key=MenuScreen.CREATE_SPREADSHEET, tooltip='Gerar Planilha', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/excel-96px.png'),
            ],
            [
                sg.Button('', key=MenuScreen.CHOOSE_SPREADSHEET_PATH, tooltip='Selecionar pasta destino de Planilhas', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/folder-96px.png'),
                sg.Button('', key=MenuScreen.EMPLOYEES, tooltip='Lista de Funcionários', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/employees-96px.png'),
                sg.Button('', key=MenuScreen.EXIT, tooltip='Sair do Sistema', size=(20,10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/exit2-96px.png'),
            ],
            [ sg.Image(source=f'src/assets/{Screen.ASSET_VERSION}/clock2.png', size=(100,100),key="image", expand_x=True, expand_y=True)],
            [ sg.Text(text='- Geração planilhas', font=("Helvetica", 20)) ],
            [ sg.Text(text='- Calculo de horários', font=("Helvetica", 20)) ],
            [ sg.Text(text='- Erros de ponto', font=("Helvetica", 20)) ],
            [ sg.ProgressBar(100, key='progressBar', visible=False, size=(30,30), bar_color=('green', 'gray'),) ],
            [ sg.Text(text='Lendo arquivo AFD, Aguarde ...', key='progressBarText', font=("Helvetica", 10), visible=False) ],
        ]
        return layout

class ReadAFDScreen(Screen):

    def __init__(self, facade, first_time = False) -> None:
        self.layout = self.get_layout()
        self.title = 'Leitura de AFD'
        self.window = self.get_window()
        self.facade = facade
        self.first_time = first_time
        self.file_path = self.get_afd_path()

    def set_size(self, size=(700, 250)):
        return super().set_size(size=size)

    def show(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                break

        self.window.close()

    def get_afd_path(self):
            afd_path = self.facade.get_afd_file_path()
            
            if afd_path == '' or afd_path is None:
                file_select = FileSelect(facade=self.facade)
                afd_path = file_select.show()
                file_select.window.close()

            if afd_path == '' or afd_path is None:
                self.window.close()
            else:
                try:
                    if self.first_time:
                        self.show_notifycation('A primeira leitura pode demorar\n alguns minutos.\nAguarde a finalização do processo.', 2)
                    self.window.Element('progressBar').update(visible=True, current_count=0)
                    self.facade.read_afd(afd_path, self.window['progressBar'])
                    self.facade.save_afd_file_path(afd_path)
                    self.show_notifycation('Leitura do arquivo concluída.')
                    self.window.close()
                except Exception as e:
                    logging.error(e.__str__())
                    self.show_notifycation(e.__str__())

    def get_layout(self):
        return [
            [sg.Text(text="Leitura de arquivo AFD",font=30)],
            [sg.ProgressBar(100, key='progressBar', visible=False, size=(30,30), bar_color=('green', 'gray'),)],
        ]

class FileSelect(Screen):
    
    def __init__(self, facade = None) -> None:
        self.facade = facade
        self.layout = self.get_layout()
        self.title = 'Seleção de Arquivo'
        self.window = self.get_window()

    def show(self):
        while True:
            event, values = self.window.read()

            if event == 'ok':
                if values['afd_file'] == '' or values['afd_file'] is None:
                    sg.popup_notify(title='Selecione o arquivo', location=(600, 100))
                else:
                    self.window.close()
                    return values['afd_file']
            if event == 'exit' or event == sg.WIN_CLOSED:
                self.window.close()
                return None
    
    def set_size(self, size=(700, 300)):
        return super().set_size(size=size)

    def get_layout(self):
        return [
            [sg.Text(text="Seleção de Arquivo",font=30)],
            [sg.Text(text=f"Arquivo atual: {self.facade.get_afd_file_path()}")],
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
        self.facade = facade
        self.layout = self.get_layout()
        self.title = 'Pasta padrão para planilhas'
        self.window = self.get_window()

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
        
    def set_size(self, size=(700, 300)):
        return super().set_size(size=size)

    def get_layout(self):
        return [
            [sg.Text(text="Selecione a Pasta",font=30)],
            [sg.Text(text=f"Pasta atual: {self.facade.get_spreadsheet_folder()}")],
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
    CURRENT_WEEK = 'Semana Atual'
    MONTH = 'Mes'
    LAST_MONTH = 'Mes anterior'

    def __init__(self,facade = None) -> None:
        self.layout = self.get_layout()
        self.title = 'Gerar Planilha'
        self.window = self.get_window()
        self.facade = facade
        self.destiny_folder = self.facade.get_spreadsheet_folder()

    def check_destiny_folder(self):
        if self.destiny_folder == '' or self.destiny_folder is None:
            FolderSelect(self.facade).show()
            self.destiny_folder = self.facade.get_spreadsheet_folder()

    def show(self):
        while True:
            event, values = self.window.read()
            self.check_destiny_folder()
            try:
                if event == 'ok':
                    start_date = self.date_to_dict(values['start_date'])
                    final_date = self.date_to_dict(values['final_date'])
                            
                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(start_date, final_date, self.destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(self.destiny_folder), display_duration_in_ms=3000, location=(600,100))

                elif event == CreateSpreadsheet.MONTH:
                    start_date =  self.date_to_dict(date.today().replace(day=1).__str__(), '-', year_index=0, day_index=2)
                    final_date =  self.date_to_dict(date.today().replace(day=monthrange(start_date['year'], start_date['month'])[1]).__str__(), '-', year_index=0, day_index=2)

                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(start_date, final_date, self.destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(self.destiny_folder), display_duration_in_ms=3000, location=(600,100))
        
                elif event == CreateSpreadsheet.LAST_MONTH:
                    start_date =  self.date_to_dict(date.today().replace(day=1, month=date.today().month-1).__str__(), '-', year_index=0, day_index=2)
                    final_date =  self.date_to_dict(date.today().replace(day=monthrange(start_date['year'], start_date['month'])[1], month=start_date['month']).__str__(), '-', year_index=0, day_index=2)
                    
                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(start_date, final_date, self.destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(self.destiny_folder), display_duration_in_ms=3000, location=(600,100))
                
                elif event == CreateSpreadsheet.TODAY:
                    today =  self.date_to_dict(date.today().__str__(), '-', year_index=0, day_index=2)

                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(today, today, self.destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(self.destiny_folder), display_duration_in_ms=3000, location=(600,100))

                elif event == CreateSpreadsheet.YESTERDAY:
                    yeasterday =  self.date_to_dict((date.today() - timedelta(days=1)).__str__(), '-', year_index=0, day_index=2)

                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(yeasterday, yeasterday, self.destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(self.destiny_folder), display_duration_in_ms=3000, location=(600,100))

                elif event == CreateSpreadsheet.LAST_WEEK:
                    start = date.today() - timedelta(days=date.today().weekday()) - timedelta(days=7)
                    final = date.today() - timedelta(days=date.today().weekday()) - timedelta(days=1)
                    start_date = self.date_to_dict(start.__str__(), '-', year_index=0, day_index=2)
                    final_date = self.date_to_dict(final.__str__(), '-', year_index=0, day_index=2)

                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(start_date, final_date, self.destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(self.destiny_folder), display_duration_in_ms=3000, location=(600,100))

                elif event == CreateSpreadsheet.CURRENT_WEEK:
                    start = date.today() - timedelta(days=date.today().weekday()+1)
                    final = date.today() + timedelta(days=date.today().weekday()-1)

                    start_date = self.date_to_dict(start.__str__(), '-', year_index=0, day_index=2)
                    final_date = self.date_to_dict(final.__str__(), '-', year_index=0, day_index=2)

                    self.window['progressBar'].update(visible=True, current_count=0)

                    self.facade.create_spreadsheet(start_date, final_date, self.destiny_folder, self.window['progressBar'])
                    sg.popup_notify(title='Planilha gerada\nSalva em {}'.format(self.destiny_folder), display_duration_in_ms=3000, location=(600,100))

                elif event == 'exit' or event == sg.WIN_CLOSED:
                    break

            except Exception as e:
                logging.error(e.__str__())
                self.show_error(e.__str__())
                logging.error(e)

        self.window.close()

    def date_to_dict(self, date, split_char='/', day_index=0, month_index=1, year_index=2):
        date_split = split(split_char, date)
        return {'day':int(date_split[day_index]), 'month':int(date_split[month_index]), 'year':int(date_split[year_index])}

    def get_layout(self):
        return [
            [sg.HorizontalSeparator()],
            [sg.Text('Opções Rápidas',font=('Times', 20))],
            [
                sg.Button('', key=CreateSpreadsheet.TODAY, tooltip='Hoje', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/calendar/today.png'),
                sg.Button('',key=CreateSpreadsheet.CURRENT_WEEK, tooltip='Semana Atual', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/calendar/current_week.png'),

                sg.Button('', key=CreateSpreadsheet.MONTH, tooltip='Mês Atual', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/calendar/month.png'),
            ],
            [
                sg.Button('', key=CreateSpreadsheet.YESTERDAY, tooltip='Ontem', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/calendar/yesterday.png'),
                sg.Button('',key=CreateSpreadsheet.LAST_WEEK, tooltip='Semana Anterior', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/calendar/last_week.png'),
                sg.Button('', key=CreateSpreadsheet.LAST_MONTH, tooltip='Mês Anterior', size=(20, 10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/calendar/last_month.png'),
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

class EmployeeMenu(Screen):

    TABLE_EMPLOYEES = 'Lista de Funcionários'
    SHOW_DETAILS = 'Detalhes'
    SHOW_GRAPHICS = 'Gráficos'

    def __init__(self,facade = None) -> None:
        self.facade = facade
        self.layout = self.get_layout()
        self.title = 'Funcionários'
        self.window = self.get_window()
    
    def show(self):
        selected_employee = None

        while True:
            event, values = self.window.read()
            print(selected_employee)
            if event == 'ok':
                pass
            elif event == EmployeeMenu.SHOW_DETAILS:
                if selected_employee is None:
                    self.show_error('Selecione um Funcionário')
                else:
                    EmployeeShow(selected_employee, self.facade).show()
            elif event == EmployeeMenu.SHOW_GRAPHICS:
                if selected_employee is None:
                    self.show_error('Selecione um Funcionário')
                else:
                    print(selected_employee)
            elif isinstance(event, tuple):
                selected_employee = self.window[EmployeeMenu.TABLE_EMPLOYEES].get()[event[2][0]]
            elif event == 'exit' or event == sg.WIN_CLOSED or event == MenuScreen.EXIT:
                break

        self.window.close()

    def get_layout(self):
        layout = [
            [
                self.create_employees_table(self.facade.get_employees()),
            ],
            [
                sg.Button('', key=EmployeeMenu.SHOW_GRAPHICS, tooltip='Gráfico do funcionário', size=(20,10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/employee/graphic-96px.png'),
                sg.Button('', key=EmployeeMenu.SHOW_DETAILS, tooltip='Ver detalhes de um funcionário', size=(20,10), image_filename=f'src/assets/{Screen.ASSET_VERSION}/employee/details-96px.png'),
            ],
            [
                #self.oKbutton(btn_tooltype='Pressione ok para gerar a planilha'),
                #self.exitButton(btn_tooltype='Sair desta tela.'),
            ],
        ]

        return layout
    
    def create_employees_table(self, employees):
        return sg.Table(employees,
                headings=['ID', 'Nome', 'PIS'],
                max_col_width=25,
                auto_size_columns=True,
                display_row_numbers=False,
                justification='left',
                num_rows=10,
                key=EmployeeMenu.TABLE_EMPLOYEES,
                selected_row_colors='red on yellow',
                enable_events=True,
                expand_x=True,
                expand_y=True,
                enable_click_events=True,
                tooltip='Tabela de Funcionários')

class EmployeeShow(Screen):

    def __init__(self, employee,facade = None) -> None:
        self.facade = facade
        self.employee = employee
        self.layout = self.get_layout()
        self.title = 'Funcionários'
        self.window = self.get_window()
    
    def show(self):
        self.draw_graph()
        while True:
            event, values = self.window.read()
            print(self.employee)
            if event == 'ok':
                pass
            elif event == 'exit' or event == sg.WIN_CLOSED or event == MenuScreen.EXIT:
                break

        self.window.close()

    def get_layout(self):
        layout = [
            [
                #sg.Text(self.employee[1])
            ],
            [
                #sg.Graph((500,500), (-250,-250), (500, 500), key='graph', expand_x=True, expand_y=True)
            ],
            [
                #self.oKbutton(btn_tooltype='Pressione ok para gerar a planilha'),
                #self.exitButton(btn_tooltype='Sair desta tela.'),
            ],
        ]
        
        return layout
    
    def draw_graph(self):
        graph = self.window['graph']
        for i in range(10):
            graph.draw_rectangle(top_left=(10+i, 200), bottom_right=(120, 0), fill_color='green')
            graph.draw_text(text=str(i), location=(i*100+15, i+10),color='red')

class ConfigScreen(Screen):

    AUTO_READ_AFD_FILE='auto_read_afd'

    def __init__(self, facade):
        self.facade = facade
        self.layout = self.get_layout()
        self.title = 'Configurações'
        self.window = self.get_window()

    def show(self):
        while True:
            event, values = self.window.read()
            if event == 'ok':
                self.facade.set_auto_read(values[ConfigScreen.AUTO_READ_AFD_FILE])
                self.show_notifycation('Configurações atualizadas')
                break
            elif event == 'exit' or event == sg.WIN_CLOSED or event == MenuScreen.EXIT:
                break

        self.window.close()

    def get_layout(self):
        return [
            [sg.Text(text="Configurações",font=30)],
            [sg.Checkbox('Ler Arquivo AFD ao abrir programa?', key=ConfigScreen.AUTO_READ_AFD_FILE, default=self.facade.get_auto_read())],
            [sg.HorizontalSeparator()],
            [
                self.oKbutton(btn_tooltype='Pressione ok Para ler o arquivo'),
                self.exitButton(btn_tooltype='Sair desta tela.'),
            ],
        ]
    
    def set_size(self, size=(700, 400)):
        return size

if __name__ == '__main__':
    MenuScreen().show()

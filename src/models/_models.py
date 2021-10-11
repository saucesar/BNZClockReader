from openpyxl.workbook import workbook
from _peewee_orm import *
from _imports import *
from _openpyxl import *
from datetime import datetime,date, timedelta
from calendar import monthrange
from rich.progress import track
import os

class Model(BaseModel):
    class Meta:
        database = Connection('db.sqlite3', pragmas={'foreign_keys': 1})

class Employee(Model):

    id = PrimaryKeyColumn()
    name = StringColumn()
    pis = StringColumn(max_length=11, unique=True)
    created_at = TimestampColumn()
    updated_at = TimestampColumn()

    class Meta:
        table_name = "employees"

    def time_clock_marking_by_month(self, year, month):
        return TimeClockMarking.select().where(TimeClockMarking.employee == self,
                                               TimeClockMarking.date >= datetime(year, month, 1).__str__(),
                                               TimeClockMarking.date <= datetime(year, month, monthrange(year, month)[1]).__str__())

    def __str__(self) -> str:
        return "ID: "+str(self.id)+" NAME: "+self.name+" PIS: "+self.pis+" CREATED_AT: "+self.created_at.__str__()+" UPDATED_AT: "+self.updated_at.__str__()

class TimeClockMarking(Model):
    
    date = DateColumn()
    first_entry = TimeColumn(null=True)
    first_exit = TimeColumn(null=True)
    second_entry = TimeColumn(null=True)
    second_exit = TimeColumn(null=True)
    pis = StringColumn(11)
    employee = ForeignKeyColumn(Employee, on_delete='CASCADE', backref='time_clock_markings')
    
    class Meta:
        table_name = "time_clock_markings"
    
    def __str__(self):
        return "DATE: {}  MARKINGS: {} {} {} {} PIS: {}".format(
            self.date,
            '        ' if self.first_entry is None else self.first_entry,
            '        ' if self.first_exit is None else self.first_exit,
            '        ' if self.second_entry is None else self.second_entry,
            '        ' if self.second_exit is None else self.second_exit,
            self.pis)

class KeyValue(Model):
    
    id = PrimaryKeyColumn()
    key = StringColumn(unique=True)
    value = StringColumn()

    AFD_LINES_READED_COUNT_KEY = 'AFD_LINES_READED_COUNT'
    AFD_FILE_PATH = 'DEFAULT_AFD_FILE_PATH'
    DEFAULT_SPREADSHEET_FOLDER = 'DEFAULT_SPREADSHEET_FOLDER'

    class Meta:
        table_name = "key_values"
    
    def __str__(self):
        return "KEY: "+self.key+"\tVALUE: "+self.value

class Spreadsheet:
    
    months = {1:'JAN',2:'FEV',3:'MAR',4:'ABR',5:'MAI',6:'JUN',7:'JUL',8:'AGO',9:'SET',10:'OUT',11:'NOV',12:'DEZ',}
    weekdays = {0:'SEG',1:'TER',2:'QUA',3:'QUI',4:'SEX',5:'SAB',6:'DOM'}

    def __init__(self) -> None:
        pass

    def create_workbook(self):
        workbook = Workbook()
        workbook.epoch = openpyxl.utils.datetime.CALENDAR_MAC_1904
        workbook.iso_dates = True

        return workbook
        

    def save_month_db_spreadsheet(self, year, month, destiny_folder):
        workbook = self.create_workbook()
        markings = workbook.active
        markings.title = 'Marcações'
        errors = workbook.create_sheet('Erros')
        header = ['NOME', 'DIA','DATA', 'E1', 'S1', 'E2', 'S2', '1ª TURNO', 'ALMOÇO', 'INT.ENTRE.JORNADAS', 'HORA. EXTRA', 'OBS']
        #           A       B     C      D     E     F     G          H        I               J                   K          L

        markings.append(header)
        errors.append(header)

        employees = Employee.select()
        total = employees.__len__()
        line = 2
        line_error = 2

        for index in track(range(0, total), 'Processando '):
            e = employees[index]
            previous = None

            for t in e.time_clock_marking_by_month(year, month):
                first_journey = self.calc_time_diff(t.first_entry, t.first_exit)
                lunch = self.calc_time_diff(t.first_exit, t.second_entry)
                break_working = self.calc_break_working_hours(previous, t)
                extra = self.calc_extra_hour(t)

                row = [e.name, Spreadsheet.weekdays[t.date.weekday()], t.date, t.first_entry, t.first_exit, t.second_entry, t.second_exit, first_journey, lunch, break_working, extra ]

                have_error = False
                obs = ''
                
                error_journey, obs_journey = self.check_first_journey(first_journey, markings, errors, line, line_error)
                error_lunch, obs_lunch = self.check_lunch(lunch, markings, errors, line, line_error)
                error_break_working, obs_break_working = self.check_break_working(break_working, markings, errors, line, line_error)
                error_extra, obs_extra = self.check_extra(extra, markings, errors, line, line_error)
                
                obs += obs_journey
                obs += obs_lunch
                obs += obs_break_working
                obs += obs_extra

                row.append(obs)
                markings.append(row)
                
                if error_journey or error_lunch or error_break_working or error_extra:
                    errors.append(row)
                    line_error += 1
                
                previous = t
                line += 1
                    
        markings.add_table(self.create_table('TableStyleMedium9', 'Marcações'))
        errors.add_table(self.create_table('TableStyleMedium9', 'Erros'))

        if os.name == 'posix': destiny_folder += '/'
        elif os.name == 'nt': destiny_folder += '\\'
        
        workbook.save("{}{}_{}.xlsx".format(destiny_folder, Spreadsheet.months[month], str(year)))

    def check_first_journey(self, first_journey, markings, errors, line, line_error):
        if first_journey != '' and first_journey > timedelta(hours=4, minutes=30):
            markings[f'H{line}'].fill = PatternFill('solid', fgColor='FF2000')
            errors[f'H{line_error}'].fill = PatternFill('solid', fgColor='FF2000')
            return (True, 'Mais que 4h 30m no primeiro turno, ')
        else:
            return (False, '')

    def check_lunch(self, lunch, markings, errors, line, line_error):
        if lunch != '' and lunch > timedelta(hours=1, minutes=50):
            markings[f'I{line}'].fill = PatternFill('solid', fgColor='FF2000')
            errors[f'I{line_error}'].fill = PatternFill('solid', fgColor='FF2000')
            #red_fill = PatternFill(bgColor="FF0000", fgColor='FF0000')
            #rule = Rule(type="cellIs", operator='greaterThan', dxf= DifferentialStyle(fill=red_fill), formula=["01:50:00"], stopIfTrue=False)
            #markings.conditional_formatting.add(f'I{line}:I{line}', rule)
            #errors.conditional_formatting.add(f'I{line_error}:I{line_error}', rule)
            
            return (True, 'Mais que 1h 50m de almoço, ')
        else:
            return (False, '')

    def check_break_working(self, break_working, markings, errors, line, line_error):
        if break_working != '' and break_working < timedelta(hours=12):
            markings[f'J{line}'].fill = PatternFill('solid', fgColor='FF2000')
            errors[f'J{line_error}'].fill = PatternFill('solid', fgColor='FF2000')
            return (True, 'Menos que 12h entre Jornadas, ')
        else:
            return (False, '')

    def check_extra(self, extra, markings, errors, line, line_error):
        if extra != '' and extra > timedelta(minutes=30, hours=1):
            markings[f'K{line}'].fill = PatternFill('solid', fgColor='FF2000')
            errors[f'K{line_error}'].fill = PatternFill('solid', fgColor='FF2000')
            
            return (True, 'Mais que 01h 30m extra, ')
        else:
            return (False, '')

    def create_table(self, name, displayName):
        table = Table(displayName=displayName, ref="A1:K5000")
        table.tableStyleInfo = TableStyleInfo(name=name, showFirstColumn=True, showLastColumn=True, showRowStripes=True, showColumnStripes=True)

        return table

    def calc_time_diff(self, start_time, end_time):
        if start_time is None or end_time is None: return ''

        d = date(1,1,1)
        start_date = datetime.combine(d, start_time)
        end_date = datetime.combine(d, end_time)

        return end_date - start_date

    def calc_break_working_hours(self, previous, today):
        if previous is None or previous.second_exit is None or today is None or today.first_entry is None:
            return ''
        else:
            start = datetime.combine(previous.date, previous.second_exit)
            end = datetime.combine(today.date, today.first_entry)

            return end - start

    def calc_extra_hour(self, time_clock_marking):
        if time_clock_marking.first_entry is None or time_clock_marking.second_exit is None:
            return ''
        seven_hours_worked = [0,1,2,3]# SEG a QUI
        day_of_week = time_clock_marking.date.weekday()

        d = date(1,1,1)
        start = datetime.combine(d, time_clock_marking.first_entry)
        end = datetime.combine(d, time_clock_marking.second_exit)
        hours_of_lunch = datetime.combine(d, time_clock_marking.second_entry) - datetime.combine(d, time_clock_marking.first_exit)

        worked_hours = (end - start)-hours_of_lunch

        if day_of_week in seven_hours_worked:
            return worked_hours - timedelta(hours=7)
        else:
            return worked_hours - timedelta(hours=8)
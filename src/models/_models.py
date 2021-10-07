from _peewee_orm import *
from _imports import *
from _openpyxl import *
from datetime import datetime,date
from calendar import monthrange
from rich.progress import track

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

    class Meta:
        table_name = "key_values"
    
    def __str__(self):
        return "KEY: "+self.key+"\tVALUE: "+self.value

class Spreadsheet:
    
    months = {1:'JAN',2:'FEV',3:'MAR',4:'ABR',5:'MAI',6:'JUN',7:'JUL',8:'AGO',9:'SET',10:'OUT',11:'NOV',12:'DEZ',}

    def __init__(self) -> None:
        pass

    def save_month_db_spreadsheet(self, year, month):
        workbook = Workbook()
        workbook.iso_dates = True
        markings = workbook.active
        markings.title = 'markings'

        tab = Table(displayName="Marcações", ref="A1:H50000")
        tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=True, showLastColumn=True, showRowStripes=True, showColumnStripes=True)

        markings.append(['NOME', 'DATA', 'E1', 'S1', 'E2', 'S2', '1ª JORNADA', 'ALMOÇO'])
        employees = Employee.select()
        count = 0
        total = employees.__len__()

        for progress in track(range(total), 'Processando marcações'):
            e = employees[progress]
            for t in e.time_clock_marking_by_month(year, month):
                markings.append([e.name, t.date, t.first_entry, t.first_exit, t.second_entry, t.second_exit,\
                                 self.calc_time_diff(t.first_entry, t.first_exit),\
                                 self.calc_time_diff(t.first_exit, t.second_entry)
                                ])
            count += 1

        markings.add_table(tab)
        workbook.save("{} {}.xlsx".format(Spreadsheet.months[month], str(year)))

    def calc_time_diff(self, start_time, end_time):
        if start_time is None or end_time is None: return ''

        d = date(1,1,1)
        start_date = datetime.combine(d, start_time)
        end_date = datetime.combine(d, end_time)

        return end_date - start_date

if __name__ == '__main__':
    Spreadsheet().save_month_db_spreadsheet(2019, 9)
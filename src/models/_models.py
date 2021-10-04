from peewee import Model as BaseModel
from peewee import SqliteDatabase as Connection
from peewee import CharField as StringColumn
from peewee import TimestampField as TimestampColumn
from peewee import TimeField as TimeColumn
from peewee import DateField as DateColumn
from peewee import PrimaryKeyField as PrimaryKeyColumn
from peewee import ForeignKeyField as ForeignKeyColumn
from datetime import datetime;
from calendar import monthrange
from _imports import *
from openpyxl import Workbook

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
                                               TimeClockMarking.date >= datetime(year, month, 1),
                                               TimeClockMarking.date <= datetime(year, month, monthrange(year, month)[1]), )

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
            '' if self.first_entry is None else self.first_entry,
            '' if self.first_exit is None else self.first_exit,
            '' if self.second_entry is None else self.second_entry,
            '' if self.second_exit is None else self.second_exit,
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
        database = workbook.active
        database.title = 'database'
        
        database.append(['PIS', 'DATA', 'HORA'])

        for e in Employee.select():
            for t in e.time_clock_marking_by_month(year, month):
                database.append([e.pis, t.date, t.time])
        workbook.save("{}-{}.xlsx".format(Spreadsheet.months[month], str(year)))

if __name__ == '__main__':
    Spreadsheet().save_month_db_spreadsheet(2019, 8)
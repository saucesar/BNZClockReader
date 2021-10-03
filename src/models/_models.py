from peewee import Model as BaseModel
from peewee import SqliteDatabase as Connection
from peewee import CharField as StringColumn
from peewee import TimestampField as TimestampColumn
from peewee import TimeField as TimeColumn
from peewee import DateField as DateColumn
from peewee import PrimaryKeyField as PrimaryKeyColumn
from peewee import ForeignKeyField as ForeignKeyColumn
from _imports import *

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

    def __str__(self) -> str:
        return "ID: "+str(self.id)+" NAME: "+self.name+" PIS: "+self.pis+" CREATED_AT: "+self.created_at.__str__()+" UPDATED_AT: "+self.updated_at.__str__()

class TimeClockMarking(Model):
    
    time = TimeColumn()
    date = DateColumn()
    pis = StringColumn(11)
    employee = ForeignKeyColumn(Employee, on_delete='CASCADE', backref='time_clock_markings')
    
    class Meta:
        table_name = "time_clock_markings"
    
    def __str__(self):
        return "DATE: "+self.date.__str__()+" TIME: "+self.time.__str__()+" PIS: "+self.pis

class KeyValue(Model):
    
    id = PrimaryKeyColumn()
    key = StringColumn()
    value = StringColumn()

    class Meta:
        table_name = "key_values"
    
    def __str__(self):
        return "KEY: "+self.key+"\tVALUE: "+self.value

if __name__ == "__main__":
    try:
        KeyValue.create(key='LINES_READED', value="THE VALUE")
        k = KeyValue.get(KeyValue.key == 'LINES_READEwD')
        print(k.value)
    except KeyValue.KeyValueDoesNotExist as e:
        print(e)
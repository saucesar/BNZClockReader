from peewee import Model as BaseModel
from peewee import SqliteDatabase as Connection
from peewee import CharField as StringColumn
from peewee import TimestampField as TimestampColumn
from peewee import TimeField as TimeColumn
from peewee import DateField as DateColumn
from peewee import PrimaryKeyField as PrimaryKeyColumn

class Model(BaseModel):
    class Meta:
        database = Connection('db.sqlite3', pragmas={'foreign_keys': 1})
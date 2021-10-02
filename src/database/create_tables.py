import logging
from connection import Connection

db = Connection()

tables = [
    ''' CREATE TABLE IF NOT EXISTS employees 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255) NOT NULL, pis VARCHAR(11) UNIQUE NOT NULL,created_at DATETIME, updated_at DATETIME) ''',
    ''' CREATE TABLE IF NOT EXISTS time_clock_markings 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, pis VARCHAR(11) NOT NULL, date DATE NOT NULL, time TIME NOT NULL) ''',
]
logging.info("START CREATING TABLES")

for table in tables:
    db.create_table(table)

logging.info("END CREATING TABLES")

db.close()
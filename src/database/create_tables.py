import sys
import logging
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
sys.path.insert(0, abspath(join(dirname(__file__), '../models')))
from models._models import *

class TableManager:
    def __init__(self) -> None:
        pass

    def create_tables(self):
        logging.info("START CREATING TABLES")

        Employee.create_table()
        TimeClockMarking.create_table()
        KeyValue.create_table()

        logging.info("END CREATING TABLES")

if __name__ == '__main__':
    TableManager().create_tables()
import logging
import sqlite3
from datetime import datetime
#logging.basicConfig(filename='dev.log', format='%(levelname)s %(asctime)s : %(message)s', level=logging.DEBUG)
logging.basicConfig(format='%(levelname)s %(asctime)s : %(message)s', level=logging.DEBUG)

class Connection:

    instance = None

    def __init__(self) -> None:
        self.data_base_path='src/database/data_base.sqlite3'
        self.connection = sqlite3.connect(self.data_base_path)
        logging.info(datetime.now().strftime("%m/%d/%Y %H:%M:%S")+" CONNECTION OPEN DATA BASE : "+self.data_base_path+" ")
        
    def create_table(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
    
    def insert(self, table, qmark, values):
        try:
            cursor = self.connection.cursor()
            sql = "INSERT INTO "+table+" "+qmark+" VALUES "+str(values)
            cursor.execute(sql)
            self.connection.commit()
            logging.info("INSERT INTO "+table)
        except sqlite3.OperationalError as e:
            logging.error(e.__class__.__name__+" -> "+str(e))
        except sqlite3.IntegrityError as e:
            logging.error(e.__class__.__name__+" -> "+str(e))
    
    def select(self, sql):
        try:
            logging.info(sql)
            return self.connection.cursor().execute(sql).fetchall()
        except sqlite3.OperationalError as e:
            logging.error(e.__class__.__name__+" -> "+str(e))
        
    def close(self):
        self.connection.close()
        logging.info(datetime.now().strftime("%m/%d/%Y %H:%M:%S")+" CONNECTION CLOSE DATA BASE : "+self.data_base_path)
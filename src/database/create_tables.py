import sys
import logging
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
sys.path.insert(0, abspath(join(dirname(__file__), '../models')))
from models.employee import Employee
from models.time_clock_marking import TimeClockMarking

logging.info("START CREATING TABLES")

Employee.create_table()
TimeClockMarking.create_table()

logging.info("END CREATING TABLES")

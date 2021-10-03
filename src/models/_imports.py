import sys
from os.path import dirname, join, abspath
from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
sys.path.insert(0, abspath(join(dirname(__file__), 'log')))
from log.log_config import *
from datetime import datetime
from _model import *
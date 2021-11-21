from datetime import date
import logging
#logging.basicConfig(format='%(levelname)s %(asctime)s : %(message)s', level=logging.DEBUG)
#logger = logging.getLogger('peewee')
#logger.addHandler(logging.StreamHandler())
logging.basicConfig(filename='logs/{}.log'.format(date.today().strftime('%Y-%m-%d')), format='%(levelname)s %(asctime)s : %(message)s', level=logging.DEBUG)
import logging
logging.basicConfig(filename='dev.log', format='%(levelname)s %(asctime)s : %(message)s', level=logging.DEBUG)
#logging.basicConfig(format='%(levelname)s %(asctime)s : %(message)s', level=logging.DEBUG)
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
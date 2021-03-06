import os
from time import time
from datetime import datetime as date
import logging


log_fmt = '%(levelname)-6s %(asctime)s %(name)-20s %(message)s'
log_dir = 'log'

if not os.path.exists(log_dir):
    os.mkdir(log_dir)

logfile_name = date.fromtimestamp(time()).strftime('%Y%m%d-%H%M%S') + '.log'
log_file = os.path.join(log_dir, logfile_name)

formatter = logging.Formatter(log_fmt)

def create_logger(name):
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    return logger

import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logs(log_file='telemetry.log'):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(format)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
    file_handler.setFormatter(format)
    logger.addHandler(file_handler)

    return logger

def function_logs(func, logger, *args):

    try:
        telemetrydata = func(*args)
        logger.info(f"{func.__name__} sucessfully excuted")
        return telemetrydata
    except Exception as e:
        logger.error(f"{func.__name__} unsucessfully executed", exc_info=True)
        return None 
    
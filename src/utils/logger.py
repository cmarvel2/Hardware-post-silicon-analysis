import logging.config
from src.utils import config_loader

def logging_setup(loggingfile: str='logging.yml') -> None:
    try:
        logging_config = config_loader.load_conf(loggingfile)
        logging.config.dictConfig(config=logging_config)
    except Exception as e:
        raise e


import logging.config
from pipeline_utils import config_loader

def logging_setup(loggingfile: str='logging.yml') -> None:
    try:
        logging_config = config_loader.load_conf(loggingfile)
        logging.config.dictConfig(config=logging_config)
    except Exception as e:
        raise e


import logging.config
import config_loader

def logging_setup(loggingfile: str='logging.yml'):
    logging_config = config_loader.load_conf(loggingfile)
    logging.config.dictConfig(config=logging_config)


import logging.config

from hardware_data_pipeline.utils import config_loader

def logging_setup(loggingfile: str=r'C:\courses_and_personal_projects\hardware_data_pipeline\conf\logging.yml') -> None:
    try:
        logging_config = config_loader.load_conf(loggingfile)
        logging.config.dictConfig(config=logging_config)
    except Exception as e:
        raise e


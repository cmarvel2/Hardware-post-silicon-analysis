import logging.config

from local_data_collection.utils import config_loader

def logging_setup(loggingfile: str=r'C:\courses_and_personal_projects\hardware_data_pipeline\src\local_data_collection\conf\logging.yml') -> None:
    logging_config = config_loader.load_conf(loggingfile)
    logging.config.dictConfig(config=logging_config)


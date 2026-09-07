import logging.config

import pytest

from local_data_collection.utils import logger


def test_logging_setup_when_config_loads_applies_dict_config(mocker):
    fake_config = {"version": 1, "disable_existing_loggers": False}
    mock_load_conf = mocker.patch.object(logger.config_loader, "load_conf", return_value=fake_config)
    mock_dict_config = mocker.patch.object(logging.config, "dictConfig")

    logger.logging_setup("logging.yml")

    mock_load_conf.assert_called_once_with("logging.yml")
    mock_dict_config.assert_called_once_with(config=fake_config)


def test_logging_setup_when_config_file_is_missing_propagates_error(mocker):
    mocker.patch.object(logger.config_loader, "load_conf", side_effect=FileNotFoundError)
    mock_dict_config = mocker.patch.object(logging.config, "dictConfig")

    with pytest.raises(FileNotFoundError):
        logger.logging_setup("missing.yml")

    mock_dict_config.assert_not_called()


def test_logging_setup_when_no_filename_given_defaults_to_logging_yml(mocker):
    mock_load_conf = mocker.patch.object(logger.config_loader, "load_conf", return_value={"version": 1})
    mocker.patch.object(logging.config, "dictConfig")

    logger.logging_setup()

    mock_load_conf.assert_called_once_with("logging.yml")
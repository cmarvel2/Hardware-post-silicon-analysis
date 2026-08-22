from local_data_collection.utils.config_loader import load_conf
import yaml
import pytest

def test_load_conf(tmp_path):
    config_file = tmp_path / "test_config_load.yml"

    config_file.write_text(
        "OCCT:\n"
        "   stability_test:\n"
        "       mode: test\n"
        "       load_type: test\n"
    )

    loaded_config = load_conf(config_file)

    assert loaded_config == {"OCCT": 
                             {"stability_test": 
                              {"mode": "test", 
                               "load_type": "test"}}}

def test_load_conf_error(tmp_path):
    config_file = tmp_path / "test_config_load_error.yml"

    config_file.write_text("Hi: hi:")

    with pytest.raises(yaml.YAMLError):
        load_conf(config_file)

def test_load_conf_nonexist(tmp_path):

    with pytest.raises(FileNotFoundError):
        load_conf("FileNotExist.yml")

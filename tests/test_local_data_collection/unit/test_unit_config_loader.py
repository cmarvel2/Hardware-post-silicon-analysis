from pathlib import Path

import pytest
import yaml

from local_data_collection.utils import config_loader


@pytest.fixture
def conf_dir(tmp_path, monkeypatch):
    """Redirect config_loader's root resolution to a throwaway tree so no real conf/ file is read."""
    fake_module = tmp_path / "pkg" / "local_data_collection" / "utils" / "config_loader.py"
    fake_module.parent.mkdir(parents=True)
    fake_module.touch()
    monkeypatch.setattr(config_loader, "__file__", str(fake_module))

    root = Path(str(fake_module)).resolve().parents[3]
    conf = root / "conf" / "conf_local_data_collection"
    conf.mkdir(parents=True)
    return conf


def write_conf(conf_dir, filename, content):
    target = conf_dir / filename
    target.write_text(yaml.safe_dump(content))
    return target


def test_load_conf_when_yaml_is_valid_returns_parsed_dict(conf_dir):
    write_conf(conf_dir, "sensors.yml", {"occt": {"stability_test": {"length_in_minutes": 5}}})

    result = config_loader.load_conf("sensors.yml")

    assert result == {"occt": {"stability_test": {"length_in_minutes": 5}}}


def test_load_conf_when_file_is_missing_raises_file_not_found_error(conf_dir):
    with pytest.raises(FileNotFoundError):
        config_loader.load_conf("does_not_exist.yml")


def test_load_conf_when_yaml_is_malformed_raises_yaml_error(conf_dir):
    (conf_dir / "broken.yml").write_text("occt:\n  - 'unbalanced")

    with pytest.raises(yaml.YAMLError):
        config_loader.load_conf("broken.yml")


@pytest.mark.parametrize(
    "filename",
    ["sensors.yml", Path("sensors.yml")],
    ids=["as_str", "as_path"],
)
def test_load_conf_when_filename_given_as_str_or_path_returns_parsed_dict(conf_dir, filename):
    write_conf(conf_dir, "sensors.yml", {"key": "value"})

    assert config_loader.load_conf(filename) == {"key": "value"}


def test_load_conf_when_yaml_file_is_empty_returns_none(conf_dir):
    (conf_dir / "empty.yml").write_text("")

    assert config_loader.load_conf("empty.yml") is None

import pytest

pytest.importorskip("winreg")

from local_data_collection.utils import machine_uuid

VALID_GUID = "12345678-1234-5678-1234-567812345678"


@pytest.fixture
def mock_registry(mocker):
    handle = mocker.Mock()
    mocker.patch("winreg.OpenKey", return_value=handle)
    close_key = mocker.patch("winreg.CloseKey")
    return handle, close_key


def test_get_windows_uuid_when_registry_value_is_valid_returns_guid_string(mocker, mock_registry):
    handle, close_key = mock_registry
    mocker.patch("winreg.QueryValueEx", return_value=(VALID_GUID, None))

    assert machine_uuid.get_windows_uuid() == VALID_GUID


def test_get_windows_uuid_reads_machine_guid_from_cryptography_key(mocker, mock_registry):
    handle, _ = mock_registry
    query_value_ex = mocker.patch("winreg.QueryValueEx", return_value=(VALID_GUID, None))

    machine_uuid.get_windows_uuid()

    query_value_ex.assert_called_once_with(handle, "MachineGuid")


def test_get_windows_uuid_closes_registry_key_after_reading(mocker, mock_registry):
    handle, close_key = mock_registry
    mocker.patch("winreg.QueryValueEx", return_value=(VALID_GUID, None))

    machine_uuid.get_windows_uuid()

    close_key.assert_called_once_with(handle)


def test_get_windows_uuid_when_registry_value_is_not_a_uuid_raises_value_error(mocker, mock_registry):
    mocker.patch("winreg.QueryValueEx", return_value=("not-a-guid", None))

    with pytest.raises(ValueError):
        machine_uuid.get_windows_uuid()


def test_get_windows_uuid_when_guid_is_braced_returns_canonical_form(mocker, mock_registry):
    mocker.patch("winreg.QueryValueEx", return_value=(f"{{{VALID_GUID.upper()}}}", None))

    assert machine_uuid.get_windows_uuid() == VALID_GUID
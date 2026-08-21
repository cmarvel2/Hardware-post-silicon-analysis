from hardware_data_pipeline.ingestion.adls_payload import UploadMemory, adls_credentials, upload_blob
from hardware_data_pipeline.ingestion.models import HardwareDataStorage

def test_payload_buffer_add():
    memory = UploadMemory()
    sensor = HardwareDataStorage(
        timestamp="20260821_010200000",
        hardware_name="Intel Core i7",
        sensor_name="CPU Package",
        sensor_type="Temperature",
        sensor_value=55.5
    )

    memory.payload_buffer_add(
        r"C:\courses_and_personal_projects\hardware_data_pipeline\conf\occt_software.yml",
        [sensor],
        [sensor],
        [sensor]
    )

    assert len(memory.payload.snapshots) == 3

def test_adls_credentials():
    credentials, account_url = adls_credentials()

    assert account_url is not None

def test_upload_blob():
    memory = UploadMemory()
    sensor = HardwareDataStorage(
        timestamp="20260821_010200000",
        hardware_name="Intel Core i7",
        sensor_name="CPU Package",
        sensor_type="Temperature",
        sensor_value=55.5
    )

    memory.payload_buffer_add(
        r"C:\courses_and_personal_projects\hardware_data_pipeline\conf\occt_software.yml",
        [sensor],
        [],
        []
    )

    credentials, account_url = adls_credentials()
    buffer_complete = memory.check_buffer(1)

    uploaded = upload_blob(
        credentials,
        account_url,
        buffer_complete,
        memory.payload
    )

    assert uploaded == True
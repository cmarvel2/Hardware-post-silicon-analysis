from datetime import datetime, timezone
import logging
import os
import uuid
 
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient, ContentSettings
from dotenv import load_dotenv, find_dotenv

from local_data_collection.sensor_polling.models import HardwarePayload
from local_data_collection.utils import config_loader, logger, machine_uuid



logger.logging_setup()

class UploadMemory:
    def __init__(self) -> None:
        self.count = 0
        self.payload = HardwarePayload()

    def payload_buffer_add(self, filename: str, cpu_payload: list, gpu_payload: list, memory_payload: list) -> None:
        combined_tuple = (cpu_payload + gpu_payload + memory_payload)
        if not self.payload.metadata and not self.payload.snapshots:
            software_config = config_loader.load_conf(filename)
            windows_device_uuid = machine_uuid.get_windows_uuid()

            self.payload.metadata["underlying_system"] = "LibreHardwareMonitor"
            self.payload.metadata["testing_software"] = software_config
            self.payload.metadata["device_id"] = windows_device_uuid
            self.payload.metadata["test_id"] = uuid.uuid4()
            self.payload.metadata["test_date"] = datetime.now(timezone.utc).strftime(r"%Y%m%d_%H%M%S")
            logging.info("Payload metadata initialzied")
        else:
            logging.info("Sensor data snapshot appended")

        self.payload.snapshots.extend(combined_tuple)
        self.count += 1

    def check_buffer(self, buffer_size_limit: int) -> bool:
        if len(self.payload.snapshots) >= buffer_size_limit:
            logging.info(f"buffer size limit ({buffer_size_limit}) reached")
            return True
        else:
            return False

    def clear_buffer(self, buffer_uploaded) -> None:
        if buffer_uploaded == True:
            self.payload.snapshots.clear()
            self.count = 0
            logging.info("Payload snapshots list cleared")

def adls_credentials() -> tuple[ClientSecretCredential, str]:
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    
    client_id = os.getenv("AZURE_CLIENT_ID")
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")
    account_url = os.getenv("AZURE_STORAGE_URL")

    credentials = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)

    logging.info("Enviroment variables loaded for Azure blob conection")
    return credentials, account_url

def get_container(environment: str | None=None) -> str:
    try:
        dev_environment = (environment or os.getenv("CURRENT_ENVIRONMENT")).lower()
        container_mapping = {
            "dev": os.getenv("AZURE_HW_BLOB_NAME_DEV"),
            "test": os.getenv("AZURE_HW_BLOB_NAME_TEST"),
            "prod": os.getenv("AZURE_HW_BLOB_NAME_PROD")
        }
        container_name = container_mapping.get(dev_environment)
        logging.info(f"Current environment: {dev_environment} retrieved")
        return container_name
    except Exception as e:
        logging.error(f"Error during container name indexing: {e}")

def upload_blob(credentials: ClientSecretCredential, account_url: str, buffer_complete: bool, sensor_buffer: HardwarePayload, container_name: str):
    if buffer_complete == True:
        try:
            blob_service_client = BlobServiceClient(account_url=account_url, credential=credentials)
            container_client = blob_service_client.get_container_client(container=container_name)

            HardwarePayload.model_validate(sensor_buffer.model_dump())
            sensors_json = sensor_buffer.model_dump_json()

            timestamp = datetime.now(timezone.utc).strftime(r"%Y%m%d_%H%M%S")
            event_id = uuid.uuid4()

            blob_name = f"hardware_sensor_data_{timestamp}_{event_id}.json"
            blob_client = container_client.get_blob_client(blob=blob_name)
            blob_client.upload_blob(data=sensors_json, content_settings=ContentSettings(content_type="application/json"))
            logging.info(f"Sucessfully uploaded blob {blob_name}")
            return True
        except Exception as e:
            logging.error(f"Error {e} during blob upload")
            return False
    else:
        pass



    

    

    
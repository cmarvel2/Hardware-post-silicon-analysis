import time
import concurrent.futures

from local_data_collection.sensor_polling.hardware_sensor_collectors import init_computer, get_cpu_data, get_gpu_data, get_memory_data
from local_data_collection.sensor_polling.adls_payload import UploadMemory, adls_credentials, upload_blob, get_container
from local_data_collection.utils.config_loader import load_conf

def main():
    computer, hardwaretype = init_computer(cpu=True, gpu=True, motherboard=True, memory=True)
    testing_configs = load_conf(r"C:\courses_and_personal_projects\hardware_data_pipeline\src\local_data_collection\conf\occt_software.yml")
    end_time = time.time() + 60 * testing_configs["OCCT"]["stability_test"]["length_in_minutes"]
    mainmemory = UploadMemory()
    credential, account_url = adls_credentials()
    container = get_container()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while time.time() < end_time:
            f1 = executor.submit(get_memory_data, computer, hardwaretype)
            f2 = executor.submit(get_gpu_data, computer, hardwaretype)
            f3 = executor.submit(get_cpu_data, computer, hardwaretype)

            memory_data = f1.result()
            gpu_data = f2.result()
            cpu_data = f3.result()

            mainmemory.payload_buffer_add(filename=r"C:\courses_and_personal_projects\hardware_data_pipeline\src\local_data_collection\conf\occt_software.yml", cpu_payload=cpu_data, gpu_payload=gpu_data, memory_payload=memory_data)

            check_buffer_result = mainmemory.check_buffer(buffer_size_limit=200000)

            upload_blob_result = upload_blob(credentials=credential, account_url=account_url, buffer_complete=check_buffer_result, sensor_buffer=mainmemory.payload, container_name=container)

            mainmemory.clear_buffer(buffer_uploaded=upload_blob_result)

    if mainmemory.payload.snapshots:
        upload_blob(credentials=credential, account_url=account_url, buffer_complete=True, sensor_buffer=mainmemory.payload)

if __name__ == "__main__":
    main()
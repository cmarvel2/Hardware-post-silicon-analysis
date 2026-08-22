import winreg
import logging

from local_data_collection.utils import logger

logger.logging_setup()

def get_windows_uuid() -> str:
    try:
        key_handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Cryptography', 0, winreg.KEY_READ)
        uuid = winreg.QueryValueEx(key_handle, 'MachineGuid')
        winreg.CloseKey(key_handle)

        realuuid, _ = uuid

        if len(realuuid) == 36:
            logging.info("UUID retrieved")
            return realuuid 
    except Exception as e:
        logging.error(f"Error {e} caused UUID retrieval failure")
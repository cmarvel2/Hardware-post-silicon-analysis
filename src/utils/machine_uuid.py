import winreg

def get_machine_uuid():
    key_handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Cryptography', 0, access=winreg.KEY_READ)
    uuid = winreg.QueryValueEx(key_handle, 'MachineGuid')
    winreg.CloseKey(key_handle)

    realuuid, _ = uuid

    if realuuid == str and len(realuuid) == 36:
        return realuuid
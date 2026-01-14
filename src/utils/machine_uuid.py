import winreg

def get_machine_uuid():
    key_handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Cryptography', 0, winreg.KEY_READ)
    uuid = winreg.QueryValueEx(key_handle, 'MachineGuid')
    winreg.CloseKey(key_handle)

    realuuid, _ = uuid

    if len(realuuid) == 36:
        
        return realuuid 
# -*- coding:utf-8 -*-

import Exceptions
import settings_manager as SettingsManager

if __name__ == '__main__':
    sm = SettingsManager.SettingsManager()
    try:
        reports_path = sm.get_reports_path()
    except Exceptions.SettingsReadException:
        print (f"Can't read report's path section from config file")
        exit()

    active_devices = sm.get_active_devices()
    for device in active_devices:
        try:
            device.start()
        except:
            print(f"Device {device['name']} couldn't start")
            reader = None
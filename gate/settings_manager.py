# -*- coding:utf-8 -*-

from configparser import ConfigParser
import scanner
import Exceptions


class SettingsManager(object):
    NAME_SECTION_SETTINGS_FILE_NAME = "config.ini"
    NAME_SECTION_REPORT_PATH = "report_path"

    def __init__(self):
        self.setting_list = {}
        self.report_path = self._get_reports_path()
        self.setting_list['devicesList'] = self.getDevices()

    def get_section(self, section_name):
        parser = ConfigParser()
        parser.read(self.NAME_SECTION_SETTINGS_FILE_NAME)
        if parser.has_section(section_name):
            return parser.items(section_name)
        else:
            return None

    def getDevices(self,):
        devicesData = []
        prefix = "USB"
        for index in range (0, 7):
            section = prefix + str(index)
            device = self.get_section(section)
            if device is None:
                continue

            deviceData = {}
            for record in device:
                deviceData[record[0]] = record[1]
            devicesData.append(deviceData)
        return devicesData

    def get_active_devices(self):
        active_devices = []
        devices = self.getDevices()
        print(devices)

        for device in devices:
            if device['active'] == 'True':
                active_devices.append(scanner.Scanner(device, self.report_path))
        return active_devices

    def _get_reports_path(self ):
        try:
            report_path_section = self.get_section(self.NAME_SECTION_REPORT_PATH)
            if report_path_section is not None:
                for item in report_path_section:
                    # self.setting_list[item[0]] = item[1]
                    return item[1]
        except:
            raise Exceptions.SettingsReadException(
                self.NAME_SECTION_SETTINGS_FILE_NAME, self.self.report_path)

    def write_settings(self, section_name, values):
        parser = ConfigParser()
        parser['report_path'] = {'report_path' : section_name['report_path']}
        for record in values:
            parser[record[0]] = record[1]

        with open('config.ini', 'w') as configfile:
            parser.write(configfile)

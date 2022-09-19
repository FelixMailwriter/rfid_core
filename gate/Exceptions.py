# -*- coding:utf-8 -*-

class SettingsReadException(Exception):
    def __init__(self, filename, section):
        super().__init__()

        self.filename = filename
        self.section = section

    def __str__(self):
        return f"Error while reading section: {self.section} file {self.filename}"
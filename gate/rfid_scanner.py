# -*- coding:utf-8 -*-

import os
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QWidget, QCheckBox, QLineEdit
import settings_manager as SettingsManager
from errors import Errors


class Rfid_scanner(QWidget):
    UI_PATH = os.path.abspath('UI')

    def __init__(self):
        super().__init__()

        #print (self.UI_PATH)
        self.form = uic.loadUi(self.UI_PATH  + "/rfid.ui")
        self.SM = SettingsManager.SettingsManager()
        self._fill_in_form()

        # #Прописываем события
        self.form.pushButtonSave.clicked.connect(self._save)
        self.form.pushButton_Cancel.clicked.connect(QCoreApplication.instance().quit)
        self.form.pushButtonRefresh.clicked.connect(self._refresh)

        self.form.show()

    def _fill_in_form(self):
        self.form.lineEditReportPath.setText(self.SM.setting_list['report_path'])
        devices = self.SM.setting_list['devicesList']
        for device in devices:
            name = device['name']
            path = device['path']
            isActive = device['active'] == 'True'
            index = int(path[-1:]) + 1

            lineedit_widgetName = 'lineEditCN' + str(index)
            checkbox_widgetName = 'checkBoxActive' + str(index)
            ref_line_edit_widget= self.form.findChild(QLineEdit, lineedit_widgetName)
            ref_checkbox_widget = self.form.findChild(QCheckBox, checkbox_widgetName)
            ref_line_edit_widget.setText(name)
            ref_checkbox_widget.setChecked(isActive)

    def _save(self):
        ref_line_report_path = self.form.findChild(QLineEdit, 'lineEditReportPath')
        report_path = {'report_path' : ref_line_report_path.text()}
        data = []
        for index in range(0, 7):
            lineedit_widgetName = 'lineEditCN' + str(index)
            checkbox_widgetName = 'checkBoxActive' + str(index)
            ref_line_edit_widget= self.form.findChild(QLineEdit, lineedit_widgetName)
            ref_checkbox_widget = self.form.findChild(QCheckBox, checkbox_widgetName)
            if ref_line_edit_widget is None\
                    or ref_line_edit_widget.text() == '':
                continue
            section_name = 'USB' + str(index-1)
            data_record = []
            data_record.append(section_name)
            parameters = {
                'name' : ref_line_edit_widget.text(),
                'path' : '/dev/tty' + section_name,
                'active' : ref_checkbox_widget.isChecked()
            }
            data_record.append(parameters)
            data.append(data_record)
        self.SM.write_settings(report_path, data)

    def _refresh(self):
        self._fill_in_form()


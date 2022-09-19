# -*- coding:utf-8 -*-
import os
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.Qt import QObject


class Errors(QObject):

    def __init__(self, messageText):
        QObject.__init__(self)
        QObject.__init__(self)
        path = os.path.abspath("UI/UIForms/errorWindow.ui")
        self.window = uic.loadUi(path)
        self.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.window.setWindowModality(QtCore.Qt.ApplicationModal)
        self.window.btn_close.clicked.connect(self.window.close)
        self.window.label.setText(messageText)

    def setMessageText(self, messageText):
        self.window.label.setText(messageText)

    def setWindowTitle(self, title):
        self.window.setWindowTitle(title)
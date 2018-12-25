#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from PyQt5 import QtWidgets


class InfoDialog(QtWidgets.QMessageBox):
    def __init__(self, message):
        super(InfoDialog, self).__init__()
        self.setIcon(QtWidgets.QMessageBox.Information)
        self.setWindowTitle("Повідомлення")
        self.setInformativeText(message)
        self.setStandardButtons(QtWidgets.QMessageBox.Ok)

#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui
from gui.translate import fromUtf8


class InfoDialog(QtGui.QMessageBox):
    def __init__(self, message):
        super(InfoDialog, self).__init__()
        self.setIcon(QtGui.QMessageBox.Information)
        self.setWindowTitle(fromUtf8("Повідомлення"))
        self.setInformativeText(fromUtf8(message))
        self.setStandardButtons(QtGui.QMessageBox.Ok)

#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui
from database import Logger
from gui.translate import fromUtf8, shorten
logger = Logger()


class FileReadingDialog(QtGui.QMessageBox):
    def __init__(self, path):
        super(FileReadingDialog, self).__init__()
        self.setIcon(QtGui.QMessageBox.Information)
        with open(path, 'r') as out:
            text = out.readlines()

        info = ''.join(text)
        self.setInformativeText(fromUtf8(info))
        self.setWindowTitle(fromUtf8(shorten(text[0], 50)))

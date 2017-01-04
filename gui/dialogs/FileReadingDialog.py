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
        linfo = QtGui.QTextEdit()
        linfo.setPlainText(fromUtf8(info))
        linfo.setFixedHeight(600)
        linfo.setFixedWidth(450)
        linfo.setReadOnly(True)

        # self.layout().addWidget(linfo)
        self.layout().addWidget(linfo, 1, 1)
        self.setWindowTitle(fromUtf8(shorten(text[0], 50)))

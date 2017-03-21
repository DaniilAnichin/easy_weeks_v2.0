#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from database import Logger
logger = Logger()


class GeneralWarning(QtGui.QMessageBox):
    def __init__(self, message, *args):
        super(GeneralWarning, self).__init__(*args)
        self.setModal(True)
        self.setText(message)

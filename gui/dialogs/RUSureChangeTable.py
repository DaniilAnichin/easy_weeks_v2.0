#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from database import Logger
from gui.translate import fromUtf8
logger = Logger()


class RUSureChangeTable(QtGui.QMessageBox):
    def __init__(self):
        super(RUSureChangeTable, self).__init__()
        self.setIcon(QtGui.QMessageBox.Warning)
        info = u'Ви збираєтеся замінити розклад у програмому додатку'
        info += u'\nПопередня таблиця може містити зміни, що не було збережено'
        info += u'\nПродовжити?'
        self.setInformativeText(fromUtf8(info))
        self.setWindowTitle(fromUtf8('Зміна розкладу'))
        self.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        self.setDefaultButton(QtGui.QMessageBox.Yes)

    def translateUI(self):
        self.setButtonText(QtGui.QMessageBox.Yes, fromUtf8('Так'))
        self.setButtonText(QtGui.QMessageBox.No, fromUtf8('Ні'))
        self.setWindowTitle(fromUtf8('Попередження'))

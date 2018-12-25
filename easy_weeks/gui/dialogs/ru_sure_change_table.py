#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from easy_weeks.database import Logger
logger = Logger()


class RUSureChangeTable(QtWidgets.QMessageBox):
    def __init__(self):
        super(RUSureChangeTable, self).__init__()
        self.setIcon(QtWidgets.QMessageBox.Warning)
        info = u'Ви збираєтеся замінити розклад у програмому додатку'
        info += u'\nПопередня таблиця може містити зміни, що не було збережено'
        info += u'\nПродовжити?'
        self.setInformativeText(info)
        self.setWindowTitle('Зміна розкладу')
        self.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.setDefaultButton(QtWidgets.QMessageBox.Yes)

    def translateUI(self):
        self.button(QtWidgets.QMessageBox.Yes).setText('Так')
        self.button(QtWidgets.QMessageBox.No).setText('Ні')
        self.setWindowTitle('Попередження')

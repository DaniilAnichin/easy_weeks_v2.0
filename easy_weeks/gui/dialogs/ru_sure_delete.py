#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from easy_weeks.database import Logger
logger = Logger()


class RUSureDelete(QtWidgets.QMessageBox):
    def __init__(self, element):
        super(RUSureDelete, self).__init__()
        self.setIcon(QtWidgets.QMessageBox.Warning)
        info = u'Ви збираєтеся видилити елемент типу %s,' % element.translated
        info += u'\nа саме: %s' % str(element)
        self.setInformativeText(info)
        self.setWindowTitle('Видалення елемента')
        self.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.setDefaultButton(QtWidgets.QMessageBox.Yes)
        self.translateUI()

    def translateUI(self):
        self.button(QtWidgets.QMessageBox.Yes).setText('Так')
        self.button(QtWidgets.QMessageBox.No).setText('Ні')
        self.setWindowTitle('Попередження')

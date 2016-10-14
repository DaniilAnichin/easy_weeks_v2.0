#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from database import Logger
from gui.translate import fromUtf8
logger = Logger()


class RUSureDelete(QtGui.QMessageBox):
    def __init__(self, element):
        super(RUSureDelete, self).__init__()
        self.setIcon(QtGui.QMessageBox.Warning)
        info = u'Ви збираєтеся видилити елемент типу %s,' % element.translated
        info += u'\nа саме: %s' % unicode(element)
        self.setInformativeText(fromUtf8(info))
        self.setWindowTitle(fromUtf8('Видалення елемента'))
        self.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        self.setDefaultButton(QtGui.QMessageBox.Yes)
        self.translateUI()

    def translateUI(self):
        self.setButtonText(QtGui.QMessageBox.Yes, fromUtf8('Так'))
        self.setButtonText(QtGui.QMessageBox.No, fromUtf8('Ні'))
        self.setWindowTitle(fromUtf8('Попередження'))

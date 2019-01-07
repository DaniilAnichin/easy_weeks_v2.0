#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox
from easy_weeks.database import Logger
logger = Logger()


class RUSureDelete(QMessageBox):
    def __init__(self, element):
        super(RUSureDelete, self).__init__()
        self.setIcon(QMessageBox.Warning)
        info = f'Ви збираєтеся видилити елемент типу {element.translated},\nа саме: {element}'
        self.setInformativeText(info)
        self.setWindowTitle('Видалення елемента')
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.Yes)
        self.translateUI()

    def translateUI(self):
        self.button(QMessageBox.Yes).setText('Так')
        self.button(QMessageBox.No).setText('Ні')
        self.setWindowTitle('Попередження')

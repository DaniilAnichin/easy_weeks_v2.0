#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox
from easy_weeks.database import Logger
logger = Logger()


class RUSureChangeTable(QMessageBox):
    def __init__(self):
        super(RUSureChangeTable, self).__init__()
        self.setIcon(QMessageBox.Warning)
        info = (
            'Ви збираєтеся замінити розклад у програмому додатку'
            '\nПопередня таблиця може містити зміни, що не було збережено'
            '\nПродовжити?'
        )
        self.setInformativeText(info)
        self.setWindowTitle('Зміна розкладу')
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.Yes)

    def translateUI(self):
        self.button(QMessageBox.Yes).setText('Так')
        self.button(QMessageBox.No).setText('Ні')
        self.setWindowTitle('Попередження')

#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from PyQt5 import QtWidgets
from easy_weeks.database import Logger
from easy_weeks.database.structure import *
from easy_weeks.database.xls_tools import print_table, print_department_table
from easy_weeks.gui.translate import titles_for_many
from easy_weeks.gui.mixins.combo_mixin import ComboMixin
logger = Logger()


class PrintDialog(ComboMixin, QtWidgets.QDialog):
    def __init__(self, session, element, table_data, parent=None):
        super(PrintDialog, self).__init__(parent)

        self.element = element
        self.table_data = table_data

        self.layout = QtWidgets.QGridLayout(self)
        self.one_button = QtWidgets.QPushButton('Друк поточного розкладу', self)
        self.layout.addWidget(self.one_button, 0, 0)
        self.one_button.clicked.connect(self.print_cur)
        self.dep_button = QtWidgets.QPushButton('Друк розкладу кафедри')
        self.layout.addWidget(self.dep_button, 0, 1)
        self.dep_button.clicked.connect(self.print_dep)
        self.setWindowTitle('Друк')
        self.session = session
        self.dep_chooser = self.make_combo(
            Departments.read(self.session, True), None, 'Department', str)
        self.layout.addWidget(self.dep_chooser, 1, 1)

        self.teachersRadioButton = QtWidgets.QRadioButton('Вчикладачі', self)
        self.groupsRadioButton = QtWidgets.QRadioButton('Групи', self)
        self.roomsRadioButton = QtWidgets.QRadioButton('Аудиторії', self)

        self.teachersRadioButton.setChecked(True)

        self.layout.addWidget(self.teachersRadioButton, 0, 3)
        self.layout.addWidget(self.groupsRadioButton, 1, 3)
        self.layout.addWidget(self.groupsRadioButton, 2, 3)

        self.setLayout(self.layout)

    def print_cur(self):
        note = 'Збереження файлу для друку'
        if isinstance(self.element, (Teachers, Groups, Rooms)):
            name = 'Розклад_%s.xlsx' % str(self.element)
        else:
            return
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, note, directory=name, filter='ExcelFiles (*.xlsx)'
        )
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        print_table(self.session, filename, self.table_data, self.element)
        self.close()

    def print_dep(self):
        note = 'Збереження файлу для друку'
        if self.teachersRadioButton.isChecked():
            data_type = 'teachers'
        else:
            data_type = 'groups'

        name = titles_for_many[data_type](self.dep_chooser.currentText()).replace(' ', '_') + '.xlsx'
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, note, directory=name, filter='ExcelFiles (*.xlsx)'
        )
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        dep_id = Departments.read(self.session, short_name=str(self.dep_chooser.currentText()))[0].id

        print_department_table(self.session, filename, data_type, dep_id)
        self.close()

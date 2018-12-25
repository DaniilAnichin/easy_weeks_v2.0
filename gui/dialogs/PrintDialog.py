#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from PyQt5 import QtWidgets
from database import Logger
from database.structure import *
from database.xls_tools import print_table, print_department_table
from gui.elements.CompleterCombo import CompleterCombo
logger = Logger()


class PrintDialog(QtWidgets.QDialog):
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
            Departments.read(self.session, True), None, u'Department', str)
        self.layout.addWidget(self.dep_chooser, 1, 1)
        self.teacherChooser = QtWidgets.QRadioButton('Вчикладачі', self)
        self.teacherChooser.setChecked(True)
        self.groupChooser = QtWidgets.QRadioButton('Групи', self)
        self.layout.addWidget(self.teacherChooser, 0, 2)
        self.layout.addWidget(self.groupChooser, 1, 2)
        self.setLayout(self.layout)

    def make_combo(self, choice_list, selected, name, sort_key):
        combo = CompleterCombo()
        combo.items = choice_list[:]
        combo.items.sort(key=sort_key)
        combo.addItems([sort_key(item) for item in combo.items])
        setattr(self, name, combo)
        if selected:
            combo.setCurrentIndex(combo.items.index(selected))
        logger.info('Added combobox with name "%s"' % name)
        return combo

    def print_cur(self):
        note = u'Збереження файлу для друку'
        if isinstance(self.element, (Teachers, Groups, Rooms)):
            name = u'Розклад_%s.xlsx' % str(self.element)
        else:
            return
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, note, directory=name, filter=u'ExcelFiles (*.xlsx)'
        )
        filename = str(filename)
        if not filename.endswith(u'.xlsx'):
            filename += u'.xlsx'
        print_table(self.session, filename, self.table_data, self.element)
        self.close()

    def print_dep(self):
        note = u'Збереження файлу для друку'
        if self.teacherChooser.isChecked():
            name = u'Розклад_виклавачів_кафедри_%s.xlsx' % str(self.dep_chooser.currentText())
            data_type = u'teachers'
        else:
            name = u'Розклад_груп_кафедри_%s.xlsx' % str(self.dep_chooser.currentText())
            data_type = u'groups'
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, note, directory=name, filter=u'ExcelFiles (*.xlsx)'
        )
        filename = str(filename)
        if not filename.endswith(u'.xlsx'):
            filename += u'.xlsx'
        dep_id = Departments.read(self.session, short_name=str(self.dep_chooser.currentText()))[0].id

        print_department_table(self.session, filename, data_type, dep_id)
        self.close()

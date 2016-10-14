#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui
from gui.translate import fromUtf8
from database.structure.db_structure import *
from gui.elements.CompleterCombo import CompleterCombo
from database.select_table import get_table
from database.xls_tools import print_table
from database import Logger
logger = Logger()


class PrintDialog(QtGui.QDialog):
    def __init__(self, s, d, td, cdt, parent=None):
        super(PrintDialog, self).__init__(parent)

        self.cur_data = d
        self.table_data = td
        self.cur_data_type = cdt

        self.layout = QtGui.QGridLayout(self)
        self.one_button = QtGui.QPushButton(fromUtf8('Друк поточного розкладу'), self)
        self.layout.addWidget(self.one_button, 0, 0)
        self.one_button.clicked.connect(self.print_cur)
        self.dep_button = QtGui.QPushButton(fromUtf8('Друк розкладу кафедри\nкафедри'))
        self.layout.addWidget(self.dep_button, 0, 1)
        self.dep_button.clicked.connect(self.print_dep)
        self.setWindowTitle(fromUtf8('Друк'))
        self.session = s
        self.dep_choiseer = self.make_combo(Departments.read(self.session, True), None, u'Department',
                                            lambda a: unicode(a))
        self.layout.addWidget(self.dep_choiseer, 1, 1)
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
        if self.cur_data_type == u'teachers':
            teacher_name = Teachers.read(self.session, id=self.cur_data)[0].short_name.replace(u' ', u'_')[:-1]
            name = u'Розклад_%s.xlsx' % teacher_name
        elif self.cur_data_type == u'groups':
            group_name = Groups.read(self.session, id=self.cur_data)[0].name
            name = u'Розклад_%s.xlsx' % group_name
        else:
            return
        save_dest = QtGui.QFileDialog.getSaveFileName(
            None, note, directory=name, filter=u'ExcelFiles (*.xlsx)'
        )
        save_dest = unicode(save_dest)
        if not save_dest.endswith(u'.xlsx'):
            save_dest += u'.xlsx'
        print_table(self.session, save_dest, self.table_data, self.cur_data_type, self.cur_data)
        self.close()

    def print_dep(self):
        note = u'Збереження файлу для друку'
        save_dir = QtGui.QFileDialog.getExistingDirectory(
            None, note, options=QtGui.QFileDialog.ShowDirsOnly
        )
        save_dir = unicode(save_dir)
        dep_id = Departments.read(self.session, short_name=unicode(self.dep_choiseer.currentText()))[0].id
        for t in Teachers.read(self.session, id_department=dep_id):
            teacher_name = t.short_name.replace(u' ', u'_')[:-1]
            name = u'/Розклад_%s.xlsx' % teacher_name
            import os.path
            save_dest = os.path.join(save_dir, name)

            self.cur_data = t.id
            self.table_data = get_table(self.session, 'teachers', t.id)
            self.cur_data_type = 'teachers'

            print_table(self.session, save_dest, self.table_data, self.cur_data_type, self.cur_data)
        self.close()

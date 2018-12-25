#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from PyQt5 import QtCore, QtWidgets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Logger, TEACHERS
from database.start_db.import_db import teacher_update
from database.start_db.db_startup import create_database
from database.start_db.seeds import create_empty, create_common, update_departments
from database.select_table import get_table, same_tables, clear_temp, find_duplicates
from database.structure import *
from database.structure import Base
from gui.dialogs.ImportDiffDialog import ImportDiffDialog
from gui.elements.CompleterCombo import CompleterCombo
logger = Logger()


class ImportDialog(QtWidgets.QDialog):
    def __init__(self, window, parent=None):
        super(ImportDialog, self).__init__(parent)
        self.window = window
        self.session = self.window.session
        self.tmp_session = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Оновлення бази')
        self.layout = QtWidgets.QVBoxLayout(self)

        self.import_all_button = QtWidgets.QPushButton('Повне оновлення', self)
        self.layout.addWidget(self.import_all_button)
        self.import_all_button.clicked.connect(self.updatedb)
        self.import_dep_button = QtWidgets.QPushButton('Оновлення викладачів\nкафедри')
        self.layout.addWidget(self.import_dep_button)
        self.import_dep_button.clicked.connect(self.updateDepDb)

        self.dep_chooser = self.make_combo(
            Departments.read(self.session, True), None, u'Department', str
        )
        self.layout.addWidget(self.dep_chooser)

        self.pro_bar = QtWidgets.QProgressBar(self)
        self.pro_bar.setValue(0)
        self.layout.addWidget(self.pro_bar)

        self.break_button = QtWidgets.QPushButton('Перервати')
        self.break_button.clicked.connect(self.closeEvent)
        self.layout.addWidget(self.break_button)

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

    def updatedb(self):
        self.import_all_button.setDisabled(True)
        self.import_dep_button.setDisabled(True)
        self.pro_bar.show()
        self.session.close_all()
        session = create_database(delete_past=True)
        with open(TEACHERS, 'r') as out:
            lines = json.load(out)

        teacher_number = len(lines)
        for i in range(teacher_number):
            self.pro_bar.setValue(100 * i / teacher_number)
            self.pro_bar.update()
            teacher = lines[i]
            teacher_update(session, teacher)
            QtCore.QCoreApplication.processEvents()
        update_departments(session)
        self.import_all_button.setDisabled(False)
        self.import_dep_button.setDisabled(False)
        self.deleteLater()

    def updateDepDb(self):
        self.import_all_button.setDisabled(True)
        self.import_dep_button.setDisabled(True)
        self.pro_bar.show()
        pop_out = ImportDiffDialog(self.session)
        j = 0

        department_name = str(self.dep_chooser.currentText())
        department_id = Departments.read(self.session, short_name=department_name)[0].id
        teachers = Teachers.read(self.session, id_department=department_id)
        teachers_number = len(teachers)

        new_engine = create_engine('sqlite:///:memory:')
        # new_engine = create_engine('sqlite:///FICT_tmp.db')
        Base.metadata.create_all(new_engine)
        session_m = sessionmaker(bind=new_engine)
        self.tmp_session = session_m()
        self.tmp_session.commit()
        pop_out.setTmpSession(self.tmp_session)

        for i in range(teachers_number):
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

            self.pro_bar.setValue(100 * j / teachers_number)
            self.pro_bar.update()

            create_empty(self.tmp_session)
            create_common(self.tmp_session)
            teacher = teachers[i]
            teacher_name = u' '.join([
                Degrees.read(self.session, id=teacher.id_degree)[0].short_name,
                teacher.short_name
            ])
            pop_out.setCurTeacher(teacher)

            if teacher.id == 1:
                # meta = MetaData()
                self.clear_database()
                continue

            update_result = teacher_update(self.tmp_session, teacher_name, True)
            if update_result == -1:
                logger.debug('Update failed')
                self.clear_database()
                continue

            if same_tables(self.session, self.tmp_session, teacher):
                self.clear_database()
                continue
            else:
                clear_temp(self.tmp_session)
            temp_teacher = Teachers.read(self.tmp_session, all_=True)[-1]
            duplicates = find_duplicates(self.tmp_session, self.session, temp_teacher)
            data = get_table(self.tmp_session, temp_teacher)

            pop_out.week_tool_window.set_table(
                data, 'teachers', pass_check=False
            )
            pop_out.setWindowTitle(teacher_name)
            if duplicates:
                pop_out.ybutton.setDisabled(True)
            pop_out.show()
            QtCore.QCoreApplication.processEvents()
            pop_out.week_tool_window.draw_duplicates(duplicates)
            QtCore.QCoreApplication.processEvents()
            self.window.tabs.set_table(get_table(self.session, teacher), 'teachers')
            self.window.tabs.setCurrentIndex(1)
            QtWidgets.QApplication.restoreOverrideCursor()

            while not pop_out.is_done:
                QtCore.QCoreApplication.processEvents()
            pop_out.is_done = False

            self.clear_database()
            if pop_out.quit:
                break
        self.import_all_button.setDisabled(False)
        self.import_dep_button.setDisabled(False)

    def clear_database(self):
        for table in reversed(Base.metadata.sorted_tables):
            self.tmp_session.execute(table.delete())
            self.tmp_session.commit()

    def closeEvent(self, QCloseEvent):
        if hasattr(self, 'tmp_session'):
            if hasattr(self.tmp_session, 'close'):
                self.tmp_session.close()
        QtWidgets.QApplication.restoreOverrideCursor()
        self.deleteLater()

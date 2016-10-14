#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from PyQt4 import QtGui, QtCore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Logger, DATABASE_NAME, DATABASE_DIR
from database.import_schedule.GetCurTimetable import teacher_update
from database.select_table import get_table
from database.start_db.seeds import *
from database.start_db.New_db_startup import create_new_database
from database.structure.db_structure import *
from database.structure.db_structure import Base
from gui.elements.CompleterCombo import CompleterCombo
from gui.dialogs.ImportDiffDialog import ImportDiffDialog
from gui.translate import fromUtf8
logger = Logger()


class ImportDialog(QtGui.QDialog):
    def __init__(self, window, parent=None):
        super(ImportDialog, self).__init__(parent)
        self.window = window
        self.session = self.window.session
        self.initUI()

    def initUI(self):
        self.setWindowTitle(fromUtf8('Оновлення бази'))
        self.layout = QtGui.QVBoxLayout(self)

        self.import_all_button = QtGui.QPushButton(fromUtf8('Повне оновлення'), self)
        self.layout.addWidget(self.import_all_button)
        self.import_all_button.clicked.connect(self.updatedb)
        self.import_dep_button = QtGui.QPushButton(fromUtf8('Оновлення викладачів\nкафедри'))
        self.layout.addWidget(self.import_dep_button)
        self.import_dep_button.clicked.connect(self.updateDepDb)

        self.dep_chooser = self.make_combo(
            Departments.read(self.session, True), None, u'Department', lambda a: unicode(a)
        )
        self.layout.addWidget(self.dep_chooser)

        self.pro_bar = QtGui.QProgressBar(self)
        self.pro_bar.setValue(0)
        self.layout.addWidget(self.pro_bar)

        self.break_button = QtGui.QPushButton(fromUtf8('Перервати'))
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
        self.pro_bar.show()
        os.remove(os.path.join(DATABASE_DIR, DATABASE_NAME))
        session = create_new_database(os.path.join(DATABASE_DIR, DATABASE_NAME))
        session = create_empty(session)
        session = create_common(session)
        session = create_custom(session)
        with open(os.path.join(DATABASE_DIR, 'import_schedule', '_teachers.txt'), 'r') as f:
            lines = f.readlines()
            teacher_number = len(lines)
            for i in range(teacher_number):
                self.pro_bar.setValue(100 * i / teacher_number)
                self.pro_bar.update()
                teacher = lines[i][:-1]
                teacher_update(session, teacher)
                QtCore.QCoreApplication.processEvents()
        self.deleteLater()

    def updateDepDb(self):
        self.pro_bar.show()
        pop_out = ImportDiffDialog(self.session)
        j = 0

        department_name = unicode(self.dep_chooser.currentText())
        department_id = Departments.read(self.session, short_name=department_name)[0].id
        teachers = Teachers.read(self.session, id_department=department_id)
        teachers_number = len(teachers)

        new_engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(new_engine)
        session_m = sessionmaker(bind=new_engine)
        self.tmp_session = session_m()
        self.tmp_session.commit()
        pop_out.setTmpSession(self.tmp_session)

        for i in range(teachers_number):
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
                for table in reversed(Base.metadata.sorted_tables):
                    self.tmp_session.execute(table.delete())
                    self.tmp_session.commit()
                continue

            teacher_update(self.tmp_session, teacher_name, True)
            temp_teacher = Teachers.read(self.tmp_session, all_=True)[-1]

            pop_out.week_tool_window.set_table(
                get_table(self.tmp_session, 'teachers', temp_teacher.id), 'teachers', pass_check=False
            )
            pop_out.setWindowTitle(QtCore.QString(teacher_name))
            pop_out.show()
            self.window.tabs.set_table(get_table(self.session, 'teachers', teacher.id), 'teachers')
            self.window.tabs.setCurrentIndex(1)

            while not pop_out.is_done:
                QtCore.QCoreApplication.processEvents()
            pop_out.is_done = False

            self.pro_bar.setValue(100 * j / teachers_number)
            self.pro_bar.update()

            for table in reversed(Base.metadata.sorted_tables):
                self.tmp_session.execute(table.delete())
                self.tmp_session.commit()
            if pop_out.quit:
                break
        self.tmp_session.close()
        self.deleteLater()
        
    def closeEvent(self, QCloseEvent):
        if hasattr(self.tmp_session, 'close'):
            self.tmp_session.close()
        self.deleteLater()

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
        self.layout = QtGui.QGridLayout(self)
        self.import_all_button = QtGui.QPushButton(fromUtf8('Повне оновлення'), self)
        self.layout.addWidget(self.import_all_button, 0, 0)
        self.import_all_button.clicked.connect(self.updatedb)
        self.import_dep_button = QtGui.QPushButton(fromUtf8('Оновлення викладачів\nкафедри'))
        self.layout.addWidget(self.import_dep_button, 0, 1)
        self.import_dep_button.clicked.connect(self.updateDepDb)
        self.setWindowTitle(fromUtf8('Оновлення бази'))
        self.session = self.window.session
        self.dep_chooser = self.make_combo(Departments.read(self.session, True), None, u'Department',
                                           lambda a: unicode(a))
        self.layout.addWidget(self.dep_chooser, 1, 1)
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


        pro_bar = QtGui.QProgressBar(self)
        self.layout.addWidget(pro_bar, 1, 0)
        pro_bar.setValue(0)
        pro_bar.show()
        os.remove(os.path.join(DATABASE_DIR, DATABASE_NAME))
        s = create_new_database(os.path.join(DATABASE_DIR, DATABASE_NAME))
        s = create_empty(s)
        s = create_common(s)
        s = create_custom(s)
        with open(os.path.join(DATABASE_DIR, 'import_schedule', '_teachers.txt'), 'r') as f:
            i = 0
            max_t = len(f.readlines())
            f.seek(0)
            for teacher in f:
                i += 1
                pro_bar.setValue(int(100*i/max_t))
                pro_bar.update()
                teacher = teacher[:-1]
                teacher_update(s, teacher)
                QtCore.QCoreApplication.processEvents()
        self.deleteLater()

    def updateDepDb(self):
        from database.import_schedule.GetCurTimetable import teacher_update
        pro_bar = QtGui.QProgressBar(self)
        self.layout.addWidget(pro_bar, 1, 2)
        pro_bar.setValue(0)
        pro_bar.show()
        pop_out = ImportDiffDialog(self.session)
        j = 0
        dep_id = Departments.read(self.session, short_name=unicode(self.dep_chooser.currentText()))[0].id
        # dep_id = 1
        max_t = len(Teachers.read(self.session, id_department=dep_id))
        new_engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(new_engine)
        session_m = sessionmaker(bind=new_engine)
        tmps = session_m()
        tmps.commit()
        pop_out.setTmpSession(tmps)
        for t in Teachers.read(self.session, id_department=dep_id):
            create_empty(tmps)
            create_common(tmps)
            teacher = Degrees.read(self.session, id=t.id_degree)[0].short_name+u' '+t.short_name
            pop_out.setCurTeacher(t)

            if t.id == 1:
                # meta = MetaData()
                for table in reversed(Base.metadata.sorted_tables):
                    tmps.execute(table.delete())
                    tmps.commit()
                continue

            teacher_update(tmps, teacher, True)

            pop_out.week_tool_window.set_table(get_table(tmps, 'teachers', Teachers.read(tmps, True)[-1].id),
                                               'teachers', pass_check=True)
            pop_out.setWindowTitle(QtCore.QString(teacher))
            pop_out.show()
            self.window.tabs.set_table(*[get_table(self.session, 'teachers', t.id), 'teachers'])
            self.window.tabs.setCurrentIndex(1)

            while not pop_out.is_done:
                QtCore.QCoreApplication.processEvents()
            pop_out.is_done = False

            pro_bar.setValue(int(100 * j / max_t))
            pro_bar.update()
            j += 1
            for table in reversed(Base.metadata.sorted_tables):
                tmps.execute(table.delete())
                tmps.commit()
            if pop_out.quit:
                break
        tmps.close()
        self.deleteLater()

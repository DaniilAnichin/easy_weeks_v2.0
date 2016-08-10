#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
from PyQt4 import QtGui, QtCore
from translate import fromUtf8
from database import Logger
from database.structure import db_structure
from database.start_db.New_db_startup import connect_database
logger = Logger()


class ShowObject(QtGui.QDialog):
    def __init__(self, element, *args, **kwargs):
        super(ShowObject, self).__init__(*args, **kwargs)
        hbox = QtGui.QHBoxLayout(self)
        self.column_box = QtGui.QVBoxLayout()
        self.values_box = QtGui.QVBoxLayout()
        if type(element).__name__ not in db_structure.__all__:
            logger.debug('Wrong params')
        else:
            logger.debug('All right')
            for column in type(element).columns():
                column_value = getattr(element, column)
                logger.debug('Column {}, value {};'.format(column, column_value))
                column_label = QtGui.QLabel(column, self)
                value_label = QtGui.QLabel(fromUtf8(unicode(column_value)), self)
                self.column_box.addWidget(column_label, 1)
                self.values_box.addWidget(value_label, 1)
        hbox.addLayout(self.column_box, 1)
        hbox.addLayout(self.values_box, 1)

        hbox.addLayout(self.column_box, 1)
        hbox.addLayout(self.values_box, 1)


class ShowLesson(QtGui.QDialog):
    def __init__(self, element, *args, **kwargs):
        super(ShowLesson, self).__init__(*args, **kwargs)
        hbox = QtGui.QHBoxLayout(self)
        self.column_box = QtGui.QVBoxLayout()
        self.values_box = QtGui.QVBoxLayout()
        if not isinstance(element, db_structure.Lessons):
            logger.info('Wrong object passed: not a lesson')
            raise ValueError
        logger.info('Setting lesson data')
        self.lesson = element
        self.lp = self.lesson.lesson_plan

        self.group_label = QtGui.QLabel(
            type(self.lp.groups[0]).translated, self
        )
        self.group_value = QtGui.QLabel(
            ', '.join(unicode(group) for group in self.lp.groups), self
        )

        self.teacher_label = QtGui.QLabel(
            type(self.lp.teachers[0]).translated, self
        )
        self.teacher_value = QtGui.QLabel(
            ', '.join(unicode(teacher) for teacher in self.lp.teachers), self
        )

        self.subject_label = QtGui.QLabel(
            type(self.lp.subject).translated, self
        )
        self.subject_value = QtGui.QLabel(
            unicode(self.lp.subject), self
        )

        self.column_box.addWidget(self.group_label, 1)
        self.column_box.addWidget(self.teacher_label, 1)
        self.column_box.addWidget(self.subject_label, 1)

        self.values_box.addWidget(self.group_value, 1)
        self.values_box.addWidget(self.teacher_value, 1)
        self.values_box.addWidget(self.subject_value, 1)

        hbox.addLayout(self.column_box, 1)
        hbox.addLayout(self.values_box, 1)


def main():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    show_button = QtGui.QPushButton('Login', window)
    session = connect_database()
    obj = db_structure.Lessons.read(session, id=0)
    # dialog = ShowObject(obj[0])
    dialog = ShowLesson(obj[0])
    show_button.clicked.connect(dialog.show)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

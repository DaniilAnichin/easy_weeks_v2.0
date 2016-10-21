#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from database import Logger
from database.structure import *
from database.select_table import find_free, get_table
from gui.elements.CompleterCombo import CompleterCombo
from gui.translate import fromUtf8
logger = Logger()


class SearchTab(QtGui.QWidget):
    def __init__(self, parent, session):
        super(SearchTab, self).__init__(parent)
        self.session = session
        self.setObjectName('search_tab')
        self.initUI()

    def initUI(self):
        self.hbox = QtGui.QHBoxLayout(self)
        self.hbox.setObjectName('search_tab_hbox')
        self.form = QtGui.QFormLayout()
        self.form.setObjectName('search_tab_form')

        for text in ['object', 'department', 'week', 'day', 'time']:
            setattr(self, text + '_label', QtGui.QLabel())
            setattr(self, text + '_choice', CompleterCombo())
            self.form.addRow(getattr(self, text + '_label'), getattr(self, text + '_choice'))

        spacer = QtGui.QSpacerItem(
            QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum
        )
        self.submit_button = QtGui.QPushButton(self)
        self.submit_button.clicked.connect(self.search)
        self.form.setItem(5, QtGui.QFormLayout.LabelRole, spacer)
        self.form.setWidget(5, QtGui.QFormLayout.FieldRole, self.submit_button)

        self.hbox.addLayout(self.form)
        self.search_list = QtGui.QListWidget(self)
        self.search_list.itemDoubleClicked.connect(self.set_table_by_item)
        self.hbox.addWidget(self.search_list)
        self.translateUI()

    def translateUI(self):
        self.object_label.setText(fromUtf8('Що знайти: '))
        self.object_choice.items = [Teachers, Rooms]
        self.object_choice.addItems([item.translated for item in self.object_choice.items])

        self.department_label.setText(Departments.translated + u':')
        self.department_choice.items = Departments.read(self.session, all_=True)
        self.department_choice.addItems([unicode(time) for time in self.department_choice.items])

        self.week_label.setText(Weeks.translated + u':')
        self.week_choice.items = Weeks.read(self.session, all_=True)
        self.week_choice.addItems([unicode(week) for week in self.week_choice.items])

        self.day_label.setText(WeekDays.translated + u':')
        self.day_choice.items = WeekDays.read(self.session, all_=True)
        self.day_choice.addItems([unicode(day) for day in self.day_choice.items])

        self.time_label.setText(LessonTimes.translated + u':')
        self.time_choice.items = LessonTimes.read(self.session, all_=True)
        self.time_choice.addItems([unicode(time) for time in self.time_choice.items])

        self.submit_button.setText(fromUtf8('Знайти'))

    def get_time(self):
        return dict(
            lesson_time=self.time_choice.items[self.time_choice.currentIndex()],
            week_day=self.day_choice.items[self.day_choice.currentIndex()],
            week=self.week_choice.items[self.week_choice.currentIndex()],
        )

    def department(self):
        return dict(department=self.department_choice.items[self.department_choice.currentIndex()])

    def search(self):
        params = self.get_time()
        params.update(self.department())
        cls = self.object_choice.items[self.object_choice.currentIndex()]
        result = find_free(self.session, cls, **params)
        logger.debug('Number of free: "%d"' % len(result))
        self.show_results(result)

    def show_results(self, values):
        self.search_list.clear()
        self.search_list.view_items = values
        self.search_list.addItems([unicode(value) for value in values])
        if not self.search_list.view_items:
            self.search_list.addItem(fromUtf8('На жаль, усі(усе) зайнято'))

    def set_table_by_item(self, *args):
        logger.debug(', '.join([str(arg) for arg in args]))
        logger.debug('%s' % args[0].text())
        logger.debug('%s' % self.search_list.row(args[0]))
        item = self.search_list.view_items[self.search_list.row(args[0])]
        cls_name = type(item).__tablename__
        self.parent().parent().set_table(get_table(self.session, item), cls_name)

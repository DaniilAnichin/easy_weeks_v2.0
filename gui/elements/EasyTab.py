#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from database import Logger
from gui.elements import WeekTool
from gui.translate import fromUtf8
logger = Logger()


class EasyTab(QtGui.QTabWidget):
    def __init__(self, parent, session):
        super(EasyTab, self).__init__(parent)
        self.session = session
        self.parent_name = parent.objectName()
        self.initUI()

    def setTabEnabled(self, p_int, bool):
        super(EasyTab, self).setTabEnabled(p_int, bool)
        self.setStyleSheet(
            'QTabBar::tab::disabled{width: 0; height: 0; margin: 0; '
            'padding: 0; border: none;}'
        )

    def initUI(self):
        self.tab_user = QtGui.QWidget(self)
        self.tab_method = QtGui.QWidget(self)
        self.tab_admin = AdminTab(self, self.session)
        self.tab_search = SearchTab(self, self.session)

        self.user_table = WeekTool(self.tab_user, self.session)
        user_hbox = QtGui.QHBoxLayout(self.tab_user)
        user_hbox.addWidget(self.user_table)
        self.tab_user.setLayout(user_hbox)

        self.method_table = WeekTool(self.tab_method, self.session)
        method_hbox = QtGui.QHBoxLayout(self.tab_method)
        method_hbox.addWidget(self.method_table, 1)
        self.tab_method.setLayout(method_hbox)

        self.translateUI()

    def translateUI(self):
        self.addTab(self.tab_user, fromUtf8('Користувач'))
        self.addTab(self.tab_method, fromUtf8('Методист'))
        self.addTab(self.tab_admin, fromUtf8('Адміністратор'))
        self.addTab(self.tab_search, fromUtf8('Пошук'))

    def set_table(self, lesson_set, view_args):
        result = self.method_table.is_editing()
        if not result:
            return
        else:
            recover_empty(self.session)
            self.user_table.set_table(lesson_set, view_args)
            self.method_table.set_table(lesson_set, view_args, drag_enabled=True)

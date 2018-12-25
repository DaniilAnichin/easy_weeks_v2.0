#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from easy_weeks.database import Logger
from easy_weeks.gui.elements.AdminTab import AdminTab
from easy_weeks.gui.elements.SearchTab import SearchTab
from easy_weeks.gui.elements.WeekTool import WeekTool
logger = Logger()


class EasyTab(QtWidgets.QTabWidget):
    def __init__(self, parent, session):
        super(EasyTab, self).__init__(parent)
        self.session = session
        self.parent_name = parent.objectName()
        self.initUI()

    def setTabEnabled(self, p_int, enabled):
        super(EasyTab, self).setTabEnabled(p_int, enabled)
        self.setStyleSheet(
            'QTabBar::tab::disabled{width: 0; height: 0; margin: 0; '
            'padding: 0; border: none;}'
        )

    def initUI(self):
        self.tab_user = QtWidgets.QWidget(self)
        self.tab_method = QtWidgets.QWidget(self)
        self.tab_admin = AdminTab(self, self.session)
        self.tab_search = SearchTab(self, self.session)

        self.user_table = WeekTool(self.tab_user, self.session)
        user_hbox = QtWidgets.QHBoxLayout(self.tab_user)
        user_hbox.addWidget(self.user_table)
        self.tab_user.setLayout(user_hbox)

        self.method_table = WeekTool(self.tab_method, self.session)
        method_hbox = QtWidgets.QHBoxLayout(self.tab_method)
        method_hbox.addWidget(self.method_table, 1)
        self.tab_method.setLayout(method_hbox)

        self.translateUI()

    def translateUI(self):
        self.addTab(self.tab_user, 'Користувач')
        self.addTab(self.tab_method, 'Методист')
        self.addTab(self.tab_admin, 'Адміністратор')
        self.addTab(self.tab_search, 'Пошук')

    def set_table(self, lesson_set, view_args):
        result = self.method_table.is_editing()
        if not result:
            return
        else:
            self.user_table.set_table(lesson_set, view_args)
            self.method_table.set_table(lesson_set, view_args, drag_enabled=True)

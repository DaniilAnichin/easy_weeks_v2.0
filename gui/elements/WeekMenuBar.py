#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from database import Logger
from gui.translate import fromUtf8
logger = Logger()


class WeekMenuBar(QtGui.QMenuBar):
    def __init__(self, *args, **kwargs):
        self.menu_data = kwargs.pop('menu_data', [])
        super(WeekMenuBar, self).__init__(*args, **kwargs)

        for menu in self.menu_data:
            menu_element = QtGui.QMenu(self)
            menu_element.setTitle(fromUtf8(menu[0]))
            setattr(self, 'menu_%d' % self.menu_data.index(menu), menu_element)
            for action in menu[1:]:
                if not action:
                    menu_element.addSeparator()
                else:
                    action_element = QtGui.QAction(self.parent())
                    action_element.setText(fromUtf8(action[0]))
                    action_element.triggered.connect(action[1])
                    menu_element.addAction(action_element)
            self.addAction(menu_element.menuAction())

        self.parent().setMenuBar(self)

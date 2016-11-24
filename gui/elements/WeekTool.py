#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from database import Logger
from gui.elements.DragButton import DragButton
from gui.elements.ButtonGrid import ButtonGrid
from gui.dialogs.RUSureChangeTable import RUSureChangeTable
from gui.translate import fromUtf8
logger = Logger()


class WeekTool(QtGui.QToolBox):
    def __init__(self, parent, session, *args, **kwargs):
        super(WeekTool, self).__init__(parent, *args, **kwargs)
        self.session = session
        self.initUI()

    def initUI(self):
        self.first_panel = QtGui.QWidget(self)
        self.first_panel.acceptDrops()
        self.first_panel.session = self.session
        self.addItem(self.first_panel, '')
        self.first_table = ButtonGrid(self.first_panel, self)

        self.second_panel = QtGui.QWidget(self)
        self.second_panel.acceptDrops()
        self.second_panel.session = self.session
        self.addItem(self.second_panel, '')
        self.second_table = ButtonGrid(self.second_panel, self)

        self.set_edited(False)

        self.setMouseTracking(True)
        self.tabButtons = self.findChildren(QtGui.QAbstractButton)
        for button in self.tabButtons:
            button.setMouseTracking(True)

        self.translateUI()

    def set_table(self, lesson_set, view_args, drag_enabled=False, pass_check=True):
        if not pass_check:
            if not self.is_editing():
                return 1
        else:
            self.clear_table()
        self.set_edited(False)
        self.first_table.set_table(lesson_set[0], view_args, 0, drag_enabled)
        self.second_table.set_table(lesson_set[1], view_args, 1, drag_enabled)
        return 0

    def set_edited(self, boolean):
        self.first_panel.edited = boolean
        self.second_panel.edited = boolean

    def edited(self):
        return self.first_panel.edited or self.second_panel.edited

    def is_editing(self):
        if self.edited():
            logger.debug('Show dialog asking about table change')
            self.rusure = RUSureChangeTable()
            result = self.rusure.exec_() == RUSureChangeTable.Yes
        else:
            # logger.debug('Not edited')
            result = True
        return result

    def clear_table(self):
        self.set_edited(False)
        for child in self.first_panel.findChildren(DragButton):
            child.before_close()
            del child
        for child in self.second_panel.findChildren(DragButton):
            child.before_close()
            del child

    def draw_duplicates(self, duplicates):
        self.first_table.draw_duplicates([x for x in duplicates if x < 30])
        self.second_table.draw_duplicates([x - 30 for x in duplicates if x >= 30])

    def translateUI(self):
        self.setItemText(0, fromUtf8('Перший тиждень'))
        self.setItemText(1, fromUtf8('Другий тиждень'))

    def dragEnterEvent(self, e):
        e.accept()

#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui

from database import Logger
from database.structure import WeekDays, LessonTimes
from gui.elements.DragButton import DragButton

logger = Logger()


class ButtonGrid(QtGui.QGridLayout):
    def __init__(self, parent, weekToolRef):
        super(ButtonGrid, self).__init__(parent)
        self.weekToolRef = weekToolRef
        for i in range(6):
            l = QtGui.QLabel(WeekDays.read(self.weekToolRef.session, id=i+2)[0].short_name)
            l.setFixedHeight(13)
            self.addWidget(l, 0, i+1)
        for j in range(5):
            l = QtGui.QLabel(LessonTimes.read(self.weekToolRef.session, id=j+2)[0].short_name)
            l.setFixedWidth(7)
            self.addWidget(l, j+1, 0)

    def set_table(self, lesson_set, view_args, week, drag_enabled=False):
        for i in range(len(lesson_set)):
            for j in range(len(lesson_set[i])):
                time = [week, i, j]
                lesson_button = DragButton(self.weekToolRef, view_args, drag_enabled, time)
                self.addWidget(lesson_button, j+1, i+1, 1, 1)
                lesson_button.set_lesson(lesson_set[i][j])

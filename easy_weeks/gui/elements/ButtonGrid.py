#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from easy_weeks.database import Logger
from easy_weeks.database.structure import WeekDays, LessonTimes
from easy_weeks.gui.elements.DragButton import DragButton
logger = Logger()


class ButtonGrid(QtWidgets.QGridLayout):
    created = False

    def __init__(self, parent, weekToolRef):
        super(ButtonGrid, self).__init__(parent)
        self.weekToolRef = weekToolRef
        for i in range(6):
            l = QtWidgets.QLabel(WeekDays.read(self.weekToolRef.session, id=i+2)[0].short_name)
            l.setFixedHeight(13)
            self.addWidget(l, 0, i+1)
        for j in range(5):
            l = QtWidgets.QLabel(LessonTimes.read(self.weekToolRef.session, id=j+2)[0].short_name)
            l.setFixedWidth(7)
            self.addWidget(l, j+1, 0)

    def set_table(self, lesson_set, view_args, week, drag_enabled=False):
        for i, day in enumerate(lesson_set):
            for j, lesson in enumerate(day):
                if self.created:
                    lesson_button = self.itemAtPosition(j + 1, i + 1).widget()
                else:
                    time = [week, i, j]
                    lesson_button = DragButton(self.weekToolRef, view_args, drag_enabled, time)
                    self.addWidget(lesson_button, j + 1, i + 1, 1, 1)
                lesson_button.set_lesson(lesson)
        self.created = True

    def draw_duplicates(self, duplicates):
        for time in duplicates:
            button = self.itemAtPosition(
                time % 5 + 1, time / 5 + 1
            ).widget()
            button.set_error()
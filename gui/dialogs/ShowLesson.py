#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database import Logger
from database.structure import *
from gui.dialogs.WeeksDialog import WeeksDialog
logger = Logger()


class ShowLesson(WeeksDialog):
    def __init__(self, element, *args, **kwargs):
        super(ShowLesson, self).__init__(*args, **kwargs)

        if not isinstance(element, Lessons):
            logger.info('Wrong object passed: not a lesson')
            raise ValueError
        logger.info('Setting lesson data')
        self.lesson = element
        self.lp = self.lesson.lesson_plan

        self.set_pair(Groups.translated, self.lp.groups)
        self.set_pair(Teachers.translated, self.lp.teachers)
        self.set_pair(Subjects.translated, self.lp.subject)
        self.set_pair(LessonTypes.translated, self.lp.lesson_type)
        self.set_pair(Rooms.translated, self.lesson.room)
        self.set_pair(Weeks.translated, self.lesson.week)
        self.set_pair(WeekDays.translated, self.lesson.week_day)
        self.set_pair(LessonTimes.translated, self.lesson.lesson_time)
        self.setWindowTitle('Заняття')

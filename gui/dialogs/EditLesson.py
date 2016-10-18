#!/usr/bin/python
# -*- coding: utf-8 -*-
from database import Logger
from database.structure import Lessons, LessonPlans
from database.select_table import undefined_lp
from gui.dialogs.WeeksDialog import WeeksDialog
from gui.translate import fromUtf8
logger = Logger()


class EditLesson(WeeksDialog):
    def __init__(self, element, session, empty=False, time=False, *args, **kwargs):
        super(EditLesson, self).__init__(*args, **kwargs)

        self.session = session
        self.empty = empty

        if not isinstance(element, Lessons):
            logger.info('Wrong object passed: not a lesson')
            raise ValueError

        # logger.info('Setting lesson data')
        self.lesson = element
        self.lp = self.lesson.lesson_plan

        # for elem in ['groups', 'teachers']:
        #     self.default_list_pair(elem, lp=True)
        # self.default_combo_pair('subject', lp=True)
        # self.default_combo_pair('lesson_type', lp=True)
        self.lp_combo_pair()

        field_list = ['room'] + (['week', 'week_day', 'lesson_time'] if time else [])
        for elem in field_list:
            self.default_combo_pair(elem)

        self.vbox.addWidget(self.make_button(fromUtf8('Підтвердити'), self.accept))
        self.vbox.addWidget(self.make_button(fromUtf8('Видалити'), self.delete))
        self.setWindowTitle(fromUtf8('Редагування заняття'))

    def lp_combo_pair(self):
        cls = LessonPlans
        label = LessonPlans.translated
        values = undefined_lp(self.session)
        name = cls.__tablename__
        if not self.empty:
            value = self.lp
            values.append(value)
            self.set_combo_pair(label, values, name, selected=value)
        else:
            self.set_combo_pair(label, values, name)

    def default_combo_pair(self, param, lp=False):
        getter = self.lp if lp else self.lesson
        cls = type(getattr(Lessons.read(self.session, id=1)[0], param))
        label = cls.translated
        values = cls.read(self.session, all_=True)
        name = cls.__tablename__
        if not self.empty:
            value = getattr(getter, param)
            self.set_combo_pair(label, values, name, selected=value)
        else:
            self.set_combo_pair(label, values, name)

    def default_list_pair(self, param, lp=False):
        getter = self.lp if lp else self.lesson
        cls = type(getattr(Lessons.read(self.session, id=1)[0], param)[0])
        label = cls.translated
        selected_values = getattr(getter, param)
        values = cls.read(self.session, all_=True)
        name = cls.__tablename__
        self.set_list_pair(label, selected_values, values, name)

    def accept(self):
        logger.debug('Here is editor saving')
        lp = self.lesson_plans.items[self.lesson_plans.currentIndex()]
        room = self.rooms.items[self.rooms.currentIndex()]
        # self.lesson.lesson_plan = lp
        # self.lesson.room = room
        Lessons.update(self.session, main_id=self.lesson.id, id_lesson_plan=lp.id, id_room=room.id)
        super(EditLesson, self).accept()

    def delete(self):
        pass

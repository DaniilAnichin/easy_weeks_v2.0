#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui

from database import Logger
from database import db_codes_output
from database.structure import *
from gui.elements.WeekTool import WeekTool

logger = Logger()


class ImportDiffDialog(QtGui.QDialog):
    def __init__(self, session, parent=None):
        super(ImportDiffDialog, self).__init__(parent)
        self.resize(805, 600)
        vlayout = QtGui.QVBoxLayout()
        self.week_tool_window = WeekTool(self, session)
        self.session = session
        vlayout.addWidget(self.week_tool_window)
        bhlayoyt = QtGui.QHBoxLayout()
        self.ybutton = QtGui.QPushButton(u'Застосувати')
        self.nbutton = QtGui.QPushButton(u'Пропустити')
        self.qbutton = QtGui.QPushButton(u'Вийти')
        self.ybutton.clicked.connect(self.acceptTT)
        self.nbutton.clicked.connect(self.defuseTT)
        self.qbutton.clicked.connect(self.quitTT)
        self.qbutton.setFixedWidth(42)
        bhlayoyt.addWidget(self.ybutton)
        bhlayoyt.addWidget(self.nbutton)
        bhlayoyt.addWidget(self.qbutton)
        vlayout.addLayout(bhlayoyt)
        self.setLayout(vlayout)
        self.is_done = False
        self.quit = False
        self.teacher = None
        self.tmp_session = None

    def setTmpSession(self, s):
        self.tmp_session = s

    def setCurTeacher(self, t):
        self.teacher = t

    def quitTT(self):
        self.is_done = True
        self.quit = True
        self.deleteLater()

    def defuseTT(self):
        self.is_done = True

    def acceptTT(self):
        t_lessons = Lessons.read(self.session, id_lesson_plan=[
            old_lp.id for old_lp in LessonPlans.read(self.session, teachers=self.teacher.id)
        ])
        for lesson in t_lessons:
            Lessons.delete(self.session, main_id=lesson.id)
        for old_lp in LessonPlans.read(self.session, teachers=self.teacher.id):
            LessonPlans.delete(self.session, main_id=old_lp.id)
        self.is_done = True
        for lp in LessonPlans.read(self.tmp_session, all_=True):
            logger.debug(unicode(str(lp)) + lp.subject.full_name)
            new_lp = LessonPlans.create(
                self.session,
                amount=lp.amount,
                capacity=lp.capacity,
                needed_stuff=lp.needed_stuff,
                id_lesson_type=lp.id_lesson_type,
                id_subject=Subjects.read(self.session, full_name=lp.subject.full_name)[0].id,
                groups=Groups.read(self.session, name=[g.name for g in lp.groups]),
                teachers=Teachers.read(self.session, full_name=[t.full_name for t in lp.teachers])
            )
            if isinstance(new_lp, int):
                logger.debug(db_codes_output[new_lp])
            else:
                for lesson in Lessons.read(self.tmp_session, id_lesson_plan=lp.id):
                    new_lesson = Lessons.create(
                        self.session,
                        row_time=lesson.row_time,
                        id_room=Rooms.read(self.session, name=lesson.room.name)[0].id,
                        id_lesson_plan=new_lp.id
                    )
                    if isinstance(new_lesson, int):
                        logger.debug(db_codes_output[new_lesson])

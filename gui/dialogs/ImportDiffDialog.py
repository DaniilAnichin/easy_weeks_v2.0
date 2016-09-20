#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from database import Logger
from gui.elements import WeekTool
from database.structure.db_structure import *
from database.structure.new_tools import *
logger = Logger()


class ImportDiffDialog(QtGui.QDialog):
    def __init__(self, session, parent=None):
        super(ImportDiffDialog, self).__init__(parent)

        vlayout = QtGui.QVBoxLayout()
        self.week_tool_window = WeekTool(self, session)
        self.session = session
        vlayout.addWidget(self.week_tool_window)
        bhlayoyt = QtGui.QHBoxLayout()
        self.ybutton = QtGui.QPushButton(u'Застосувати')
        self.nbutton = QtGui.QPushButton(u'Пропустити')
        self.qbutton = QtGui.QPushButton(u'Вийти')
        self.qbutton.setFixedWidth(42)
        bhlayoyt.addWidget(self.ybutton)
        bhlayoyt.addWidget(self.nbutton)
        bhlayoyt.addWidget(self.qbutton)
        vlayout.addLayout(bhlayoyt)
        self.setLayout(vlayout)
        self.ybutton.clicked.connect(self.acceptTT)
        self.nbutton.clicked.connect(self.defuseTT)
        self.qbutton.clicked.connect(self.quitTT)
        self.is_done = False
        self.quit = False
        self.teacher = None
        self.tmps = None

    def setTmpSession(self, s):
        self.tmps = s

    def setCurTeacher(self, t):
        self.teacher = t

    def quitTT(self):
        self.is_done = True
        self.quit = True
        self.deleteLater()

    def acceptTT(self):
        t_lessons = Lessons.read(self.session, id_lesson_plan=[i.id for i in LessonPlans.read(self.session,
                                                                                              teachers=self.teacher.id)])
        for lesson in t_lessons:
            lesson.delete(self.session, lesson.id)
        for lp in LessonPlans.read(self.session, teachers=self.teacher.id):
            lp.delete(self.session, lp.id)
        for lp in self.tmps.query(LessonPlans).all()[1:]:
            new_lp = new_lesson_plan(self.session, times_for_2_week=lp.amount, capacity=lp.capacity,
                                     needed_stuff=lp.needed_stuff,
                                     id_les_type=lp.id_lesson_type,
                                     id_sub=Subjects.read(self.session, full_name=lp.subject.full_name)[0].id,
                                     id_grps=[g.id for g in Groups.read(self.session, name=[p.name for p in
                                                                                            lp.groups])],
                                     id_tes=[t.id for t in Teachers.read(self.session, full_name=[p.full_name
                                                                                                  for p in
                                                                                                  lp.teachers])])
            for l in Lessons.read(self.tmps, id_lesson_plan=lp.id):
                new_lesson(self.session, row_time=l.row_time, id_room=Rooms.read(self.session, name=l.room.name)[0].id,
                           id_lp=new_lp.id)
        self.is_done = True

    def defuseTT(self):
        self.is_done = True

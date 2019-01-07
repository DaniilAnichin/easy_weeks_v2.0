#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey
from easy_weeks.database import Logger
from easy_weeks.database.structure import Base
logger = Logger()


class TeacherPlans(Base):
    id_teacher = Column(Integer, ForeignKey('teachers.id'))
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plans.id'))
    translated = 'Заняття викладача'

    def __str__(self):
        return f'{self.id_teacher} to {self.id_lesson_plan}'

    _columns = ['id_teacher', 'id_lesson_plan']

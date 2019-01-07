#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey
from easy_weeks.database import Logger
from easy_weeks.database.structure import Base
logger = Logger()


class GroupPlans(Base):
    id_group = Column(Integer, ForeignKey('groups.id'))
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plans.id'))
    translated = 'Заняття групи'

    def __str__(self):
        return f'{self.id_group} to {self.id_lesson_plan}'

    _columns = ['id_group', 'id_lesson_plan']

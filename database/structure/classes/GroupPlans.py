#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey
from database import Logger
from database.structure import Base
logger = Logger()


class GroupPlans(Base):
    id_group = Column(Integer, ForeignKey('groups.id'))
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plans.id'))
    translated = u'Заняття групи'

    def __unicode__(self):
        return u'%d in %d' % (self.id_group, self.id_lesson_plan)

    _columns = ['id_group', 'id_lesson_plan']

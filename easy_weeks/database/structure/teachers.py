#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from easy_weeks.database import Logger
from easy_weeks.database.structure import Base
logger = Logger()


class Teachers(Base):
    full_name = Column(String)
    short_name = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_degree = Column(Integer, ForeignKey('degrees.id'))
    translated = u'Викладач'

    def __str__(self):
        return self.full_name

    _columns = ['id', 'full_name', 'short_name', 'id_department', 'id_degree']
    _links = ['department', 'degree']
    _associations = ['lesson_plans']

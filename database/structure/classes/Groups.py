#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Logger
from database.structure import Base
logger = Logger()


class Groups(Base):
    name = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))
    translated = u'Група'

    def __str__(self):
        return self.name

    _columns = ['id', 'name', 'id_department']
    _links = ['department']
    _associations = ['lesson_plans']

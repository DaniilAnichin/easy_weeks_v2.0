#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from easy_weeks.database import Logger
from easy_weeks.database.structure import Base
logger = Logger()


class Faculties(Base):
    full_name = Column(String)
    short_name = Column(String)
    id_university = Column(Integer, ForeignKey('universities.id'))
    translated = u'Факультет'

    def __str__(self):
        return self.short_name

    departments = relationship(
        'Departments', backref='faculty', cascade='all, delete-orphan'
    )

    _columns = ['id', 'full_name', 'short_name', 'id_university']
    _links = ['departments', 'university']

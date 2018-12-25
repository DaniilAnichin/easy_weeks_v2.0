#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from easy_weeks.database import Logger
from easy_weeks.database.structure import Base
logger = Logger()


class WeekDays(Base):
    full_name = Column(String)
    short_name = Column(String)
    translated = u'День'

    def __str__(self):
        return self.full_name

    lessons = relationship('Lessons', backref='week_day', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lessons']
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Logger
from database.structure import Base
logger = Logger()


class LessonTimes(Base):
    full_name = Column(String)
    short_name = Column(String)
    translated = u'Час'

    def __str__(self):
        return self.full_name

    lessons = relationship('Lessons', backref='lesson_time', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lessons']

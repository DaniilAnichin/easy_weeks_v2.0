#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from database import Logger
from database.structure import Base
logger = Logger()


class Subjects(Base):
    full_name = Column(String)
    short_name = Column(String)
    translated = u'Предмет'

    def __unicode__(self):
        return self.full_name

    lesson_plans = relationship('LessonPlans', backref='subject', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lesson_plans']

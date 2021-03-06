#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Logger
from database.structure import Base
logger = Logger()


class Departments(Base):
    full_name = Column(String)
    short_name = Column(String)
    id_faculty = Column(Integer, ForeignKey('faculties.id'))
    translated = u'Кафедра'

    def __unicode__(self):
        return self.short_name

    groups = relationship(
        'Groups', backref='department', cascade='all, delete-orphan'
    )
    teachers = relationship(
        'Teachers', backref='department', cascade='all, delete-orphan'
    )
    rooms = relationship(
        'Rooms', secondary='department_rooms', backref='departments'
    )

    _columns = ['id', 'full_name', 'short_name']
    _links = ['groups', 'teachers', 'faculty']
    _associations = ['rooms']

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey
from database import Logger
from database.structure import Base
logger = Logger()


class DepartmentRooms(Base):
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    translated = u'Кімнати кафедри'

    def __str__(self):
        return u'%d in %d' % (self.id_room, self.id_department)

    _columns = ['id_room', 'id_department']

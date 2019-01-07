#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey
from easy_weeks.database import Logger
from easy_weeks.database.structure import Base
logger = Logger()


class DepartmentRooms(Base):
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    translated = 'Кімнати кафедри'

    def __str__(self):
        return f'{self.id_room} in {self.id_department}'

    _columns = ['id_room', 'id_department']

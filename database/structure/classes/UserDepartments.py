#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey
from database import Logger
from database.structure import Base
logger = Logger()


class UserDepartments(Base):
    id_user = Column(Integer, ForeignKey('users.id'))
    id_department = Column(Integer, ForeignKey('departments.id'))
    translated = u'Користувач-Кафедра'

    def __str__(self):
        return u'%d in %d' % (self.id_user, self.id_department)

    _columns = ['id_user', 'id_department']

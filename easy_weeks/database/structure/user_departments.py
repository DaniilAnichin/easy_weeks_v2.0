#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey
from easy_weeks.database import Logger
from easy_weeks.database.structure import Base
logger = Logger()


class UserDepartments(Base):
    id_user = Column(Integer, ForeignKey('users.id'))
    id_department = Column(Integer, ForeignKey('departments.id'))
    translated = 'Користувач-Кафедра'

    def __str__(self):
        return f'{self.id_user} in {self.id_department}'

    _columns = ['id_user', 'id_department']

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import db_codes, Logger
from database.structure import Base
logger = Logger()


class Rooms(Base):
    name = Column(String)
    capacity = Column(Integer)
    additional_stuff = Column(String)
    translated = u'Аудиторія'

    def __str__(self):
        return self.name

    lessons = relationship('Lessons', backref='room', cascade='all, delete-orphan')

    _columns = ['id', 'name', 'capacity', 'additional_stuff']
    _links = ['lessons']
    _associations = ['departments']

    @classmethod
    def read(cls, session, all_=False, **kwargs):
        from database.structure import Departments, Lessons
        if isinstance(session, int):
            return db_codes['session']

        result = session.query(cls)

        if all_:
            return result.all()[1:]

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']

            if key in ['departments', 'lessons']:
                if not isinstance(kwargs[key], list):
                    kwargs[key] = [kwargs[key]]

                kwargs[key] = [item.id if not isinstance(item, int) else item
                               for item in kwargs[key]]
                if key == 'lessons':
                    result = result.filter(Rooms.lessons.any(
                        Lessons.id.in_(kwargs[key])
                    ))
                elif key == 'departments':
                    result = result.filter(Rooms.departments.any(
                        Departments.id.in_(kwargs[key])
                    ))
            else:
                if isinstance(kwargs[key], list):
                    result = result.filter(getattr(cls, key).in_(kwargs[key]))
                else:
                    result = result.filter(getattr(cls, key) == (kwargs[key]))

        return result.all()

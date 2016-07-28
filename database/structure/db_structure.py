#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Create_new_db.py
#
#  Copyright 2016 AntonBogovis <antonbogovis@lenovo-bogovis>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from database import db_codes

__all__ = [
    'Degrees', 'Department_rooms', 'Departments', 'Faculties', 'Groups',
    'Group_plans', 'Lesson_plans', 'Teacher_plans', 'Lesson_times',
    'Lesson_types', 'Lessons', 'Rooms', 'Subjects', 'Teachers', 'Tmp_lessons',
    'Universities', 'Week_days', 'Weeks'
]


_Base = declarative_base()


@as_declarative()
class Base(object):
    def __init__(self, **kwargs):
        super(Base, self).__init__(**kwargs)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)

    @classmethod
    def fields(cls):
        return cls._fields[:]

    @classmethod
    def columns(cls):
        return cls._columns[:]

    @classmethod
    def create(cls, session, **kwargs):
        if isinstance(session, int):
            return db_codes['session']

        result = session.query(cls)

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']
            elif isinstance(kwargs[key], list):
                result.filter(getattr(cls, key) in kwargs[key])
            else:
                result.filter(getattr(cls, key) == kwargs[key])

        if result.all():
            return db_codes['exists']

        return db_codes['success']

    @classmethod
    def read(cls, session, **kwargs):
        if isinstance(session, int):
            return db_codes['session']

        result = session.query(cls)

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']
            elif isinstance(kwargs[key], list):
                result.filter(getattr(cls, key) in kwargs[key])
            else:
                result.filter(getattr(cls, key) == kwargs[key])

        return result.all()

    @classmethod
    def update(cls, session, main_id, **kwargs):
        if isinstance(session, int):
            return db_codes['session']

        result = session.query(cls)

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']
            elif isinstance(kwargs[key], list):
                result.filter(getattr(cls, key) in kwargs[key])
            else:
                result.filter(getattr(cls, key) == kwargs[key])

        return db_codes['success']

    @classmethod
    def delete(cls, session, main_id):
        if isinstance(session, int):
            return db_codes['session']

        # No deleting first data
        if main_id == 1:
            return db_codes['reserved']

        result = session.query(cls).get(main_id)

        # Check for existance
        if not result:
            return db_codes['absent']

        # Reset links:
        for reference in cls.fields():
            if reference not in cls.columns():
                referenced = getattr(result, reference)
                if isinstance(referenced, list):
                    for element in referenced:
                        setattr(element, 'id_' + cls.__tablename__, 1)
                else:
                    setattr(referenced, 'id_' + cls.__tablename__, 1)

        session.delete(result)
        session.commit()
        return db_codes['success']


class Universities(Base):
    full_name = Column(String)
    short_name = Column(String)

    faculties = relationship('Faculties', backref='universities', cascade="all, delete-orphan")

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['faculties']


class Faculties(Base):
    full_name = Column(String)
    short_name = Column(String)
    id_university = Column(Integer, ForeignKey('universities.id'))

    departments = relationship('Departments', backref='faculties', cascade="all, delete-orphan")

    _columns = ['id', 'full_name', 'short_name', 'id_university']
    _fields = _columns + ['departments']


class Department_rooms(Base):
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))

    _columns = ['id_room', 'id_department']
    _fields = _columns


class Departments(Base):
    full_name = Column(String)
    short_name = Column(String)
    id_faculty = Column(Integer, ForeignKey('faculties.id'))

    groups = relationship('Groups', backref='departments', cascade="all, delete-orphan")
    teachers = relationship('Teachers', backref='departments', cascade="all, delete-orphan")
    rooms = relationship('Rooms', secondary='department_rooms', backref='departments')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['groups', 'teachers', 'rooms']


class Group_plans(Base):
    id_group = Column(Integer, ForeignKey('groups.id'))
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plan.id'))

    _columns = ['id_group', 'id_lesson_plan']
    _fields = _columns


class Teacher_plans(Base):
    id_teacher = Column(Integer, ForeignKey('teachers.id'))
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plan.id'))

    _columns = ['id_teacher', 'id_lesson_plan']
    _fields = _columns


class Groups(Base):
    name = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))

    _columns = ['id', 'name', 'id_department']
    _fields = _columns + ['lesson_plans']


class Degrees(Base):
    full_name = Column(String)
    short_name = Column(String)

    teachers = relationship('Teachers', backref='degrees', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['teachers']


class Teachers(Base):
    full_name = Column(String)
    short_name = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_degree = Column(Integer, ForeignKey('degrees.id'))

    _columns = ['id', 'full_name', 'short_name', 'id_department', 'id_degree']
    _fields = _columns + ['faculties', 'lesson_plans']


class Subjects(Base):
    full_name = Column(String)
    short_name = Column(String)

    lesson_plan = relationship('Lesson_plans', backref='subjects', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['lesson_plan']


class Rooms(Base):
    name = Column(String)
    capacity = Column(Integer)
    additional_stuff = Column(String)

    lessons = relationship('Lessons', backref='rooms', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='rooms', cascade='all, delete-orphan')

    _columns = ['id', 'name', 'capacity', 'additional_stuff']
    _fields = _columns + ['lessons', 'tmp_lessons', 'departments']


class Lesson_types(Base):
    full_name = Column(String)
    short_name = Column(String)

    lesson_plan = relationship('Lesson_plans', backref='lesson_types', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['lesson_plan']


class Weeks(Base):
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='weeks', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='weeks', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['lessons', 'tmp_lessons']


class Week_days(Base):
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='week_days', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='week_days', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['lessons', 'tmp_lessons']


class Lesson_times(Base):
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='lesson_times', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='lesson_times', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['lessons', 'tmp_lessons']


class Lesson_plans(Base):
    id_subject = Column(Integer, ForeignKey('subjects.id'))
    id_lesson_type = Column(Integer, ForeignKey('lesson_types.id'))

    amount = Column(Integer)
    needed_stuff = Column(String)
    capacity = Column(Integer)
    split_groups = Column(Integer)

    param_checker = Column(String)

    lessons = relationship('Lessons', backref='lesson_plan', cascade='all, delete-orphan')
    groups = relationship('Groups', secondary='group_plans', backref='lesson_plans')
    teachers = relationship('Teachers', secondary='teacher_plans', backref='lesson_plans')

    _columns = ['id', 'id_subject', 'id_lesson_type', 'amount',
                'needed_stuff', 'capacity', 'split_groups', 'param_checker']
    _fields = _columns + ['lessons', 'groups', 'teachers']


class Lessons(Base):
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plan.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    id_lesson_time = Column(Integer, ForeignKey('lesson_times.id'))
    id_week_day = Column(Integer, ForeignKey('week_days.id'))
    id_week = Column(Integer, ForeignKey('weeks.id'))

    row_time = Column(Integer)

    _columns = ['id', 'id_lesson_plan', 'id_room', 'id_lesson_time',
                'id_week_day', 'id_week', 'row_time']
    _fields = _columns


class Tmp_lessons(Base):
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plan.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    id_lesson_time = Column(Integer, ForeignKey('lesson_times.id'))
    id_week_day = Column(Integer, ForeignKey('week_days.id'))
    id_week = Column(Integer, ForeignKey('weeks.id'))

    row_time = Column(Integer)

    _columns = ['id', 'id_lesson_plan', 'id_room', 'id_lesson_time',
                'id_week_day', 'id_week', 'row_time']
    _fields = _columns

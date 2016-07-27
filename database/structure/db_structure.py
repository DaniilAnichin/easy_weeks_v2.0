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

from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import as_declarative, declared_attr
__all__ = [
    'Degrees', 'Department_rooms', 'Departments', 'Faculties', 'Groups',
    'Lesson_groups', 'Lesson_plan', 'Lesson_teachers', 'Lesson_times',
    'Lesson_types', 'Lessons', 'Rooms', 'Subjects', 'Teachers', 'Tmp_lessons',
    'Universities', 'Week_days', 'Weeks'
]


_Base = declarative_base()


@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


class Universities(Base):
    full_name = Column(String)
    short_name = Column(String)

    faculties = relationship('Faculties', backref='universities', cascade="all, delete-orphan")

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['faculties']


class Faculties(Base):
    __tablename__ = 'faculties'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)
    id_university = Column(Integer, ForeignKey('universities.id'))

    departments = relationship('Departments', backref='faculties', cascade="all, delete-orphan")

    _columns = ['id', 'full_name', 'short_name', 'id_university']
    _fields = _columns + ['departments']

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns

#
# Department_rooms = Table('department_rooms', Base.metadata,
#                          Column('id_department', Integer, ForeignKey('departments.id')),
#                          Column('id_room', Integer, ForeignKey('rooms.id')))


class Department_rooms(Base):
    # id = None
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))

    _columns = ['id_room', 'id_department']
    _fields = _columns
    #
    # @property
    # def foreign_keys(self):
    #     return [getattr(type(self), column) for column in self._columns]


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)
    id_faculty = Column(Integer, ForeignKey('faculties.id'))

    groups = relationship('Groups', backref='departments', cascade="all, delete-orphan")

    teachers = relationship('Teachers', backref='departments', cascade="all, delete-orphan")

    rooms = relationship('Rooms', secondary='department_rooms', backref='departments')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['groups', 'teachers', 'rooms']

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


Lesson_groups = Table('lesson_groups', Base.metadata,
                      Column('id_lesson_plan', Integer, ForeignKey('lesson_plan.id')),
                      Column('id_group', Integer, ForeignKey('groups.id')))

Lesson_teachers = Table('lesson_teachers', Base.metadata,
                        Column('id_lesson_plan', Integer, ForeignKey('lesson_plan.id')),
                        Column('id_teacher', Integer, ForeignKey('teachers.id')))


class Groups(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))

    _columns = ['id', 'name', 'id_department']
    _fields = _columns + []

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


class Degrees(Base):
    __tablename__ = 'degrees'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    teachers = relationship('Teachers', backref='degrees', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['teachers']

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


class Teachers(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_degree = Column(Integer, ForeignKey('degrees.id'))

    _columns = ['id', 'full_name', 'short_name', 'id_department', 'id_degree']
    _fields = _columns + ['faculties']

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


class Subjects(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    lesson_plan = relationship('Lesson_plan', backref='subjects', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['lesson_plan']

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    capacity = Column(Integer)
    additional_stuff = Column(String)
    # id_department = Column(Integer, ForeignKey('departments.id'))

    lessons = relationship('Lessons', backref='rooms', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='rooms', cascade='all, delete-orphan')

    _columns = ['id', 'name', 'capacity', 'additional_stuff']
    _fields = _columns + ['lessons', 'tmp_lessons', 'departments']

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


class Lesson_types(Base):
    __tablename__ = 'lesson_types'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    lesson_plan = relationship('Lesson_plan', backref='lesson_types', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['lesson_plan']

    @property
    def fields(self):
        return type(self)._fields


class Weeks(Base):
    __tablename__ = 'weeks'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='weeks', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='weeks', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['lessons', 'tmp_lessons']

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


class Week_days(Base):
    __tablename__ = 'week_days'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='week_days', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='week_days', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['lessons', 'tmp_lessons']

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


class Lesson_times(Base):
    __tablename__ = 'lesson_times'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='lesson_times', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='lesson_times', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _fields = _columns + ['lessons', 'tmp_lessons']

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


class Lesson_plan(Base):
    __tablename__ = 'lesson_plan'

    id = Column(Integer, primary_key=True)
    id_subject = Column(Integer, ForeignKey('subjects.id'))
    id_lesson_type = Column(Integer, ForeignKey('lesson_types.id'))

    times_for_2_week = Column(Integer)
    needed_stuff = Column(String)
    capacity = Column(Integer)
    split_groups = Column(Integer)

    param_checker = Column(String)

    lessons = relationship('Lessons', backref='lesson_plan', cascade='all, delete-orphan')
    groups = relationship('Groups', secondary=Lesson_groups, backref='lesson_plan')
    teachers = relationship('Teachers', secondary=Lesson_teachers, backref='lesson_plan')

    _columns = ['id', 'id_subject', 'id_lesson_type', 'times_for_2_week',
                'needed_stuff', 'capacity', 'split_groups', 'param_checker']
    _fields = _columns + ['lessons', 'groups', 'teachers']

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


class Lessons(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plan.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    id_lesson_time = Column(Integer, ForeignKey('lesson_times.id'))
    id_week_day = Column(Integer, ForeignKey('week_days.id'))
    id_week = Column(Integer, ForeignKey('weeks.id'))

    row_time = Column(Integer)

    _columns = ['id', 'id_lesson_plan', 'id_room', 'id_lesson_time',
                'id_week_day', 'id_week', 'row_time']
    _fields = _columns + []

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns


class Tmp_lessons(Base):
    __tablename__ = 'tmp_lessons'

    id = Column(Integer, primary_key=True)
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plan.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    id_lesson_time = Column(Integer, ForeignKey('lesson_times.id'))
    id_week_day = Column(Integer, ForeignKey('week_days.id'))
    id_week = Column(Integer, ForeignKey('weeks.id'))

    row_time = Column(Integer)

    _columns = ['id', 'id_lesson_plan', 'id_room', 'id_lesson_time',
                'id_week_day', 'id_week', 'row_time']
    _fields = _columns + []

    @property
    def fields(self):
        return type(self)._fields

    @property
    def columns(self):
        return type(self)._columns

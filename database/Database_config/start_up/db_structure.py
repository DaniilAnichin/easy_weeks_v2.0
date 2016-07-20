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

Base = declarative_base()


class Universities(Base):
    __tablename__ = 'universities'
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    faculties = relationship('Faculties', backref='universities', cascade="all, delete-orphan")

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Universities.id
        elif column_name == 'full_name':
            return Universities.full_name
        elif column_name == 'short_name':
            return Universities.short_name
        else:
            return 0


class Faculties(Base):
    __tablename__ = 'faculties'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)
    id_university = Column(Integer, ForeignKey('universities.id'))

    departments = relationship('Departments', backref='faculties', cascade="all, delete-orphan")

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Faculties.id
        elif column_name == 'full_name':
            return Faculties.full_name
        elif column_name == 'short_name':
            return Faculties.short_name
        elif column_name == 'id_university':
            return Faculties.id_university
        else:
            return 0


Department_rooms = Table('department_rooms', Base.metadata,
                         Column('id_department', Integer, ForeignKey('departments.id')),
                         Column('id_room', Integer, ForeignKey('rooms.id')))


class Departments(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)
    id_faculty = Column(Integer, ForeignKey('faculties.id'))

    groups = relationship('Groups', backref='departments', cascade="all, delete-orphan")

    teachers = relationship('Teachers', backref='departments', cascade="all, delete-orphan")

    rooms = relationship('Rooms', secondary=Department_rooms, backref='departments')

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Departments.id
        elif column_name == 'full_name':
            return Departments.full_name
        elif column_name == 'short_name':
            return Departments.short_name
        elif column_name == 'rooms':
            return Departments.rooms
        else:
            return 0


# class Streams(Base):
#     __tablename__ = 'streams'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     id_department = Column(Integer, ForeignKey('departments.id'))
#
#     groups = relationship('Groups', backref='streams', cascade="all, delete-orphan")
#
#     lesson_plan = relationship('Lesson_plan', backref='streams', cascade='all, delete-orphan')
#
#     # def __init__(self, name='', id_de=1):
#     #     if name == '':
#     #         print "Name must be"
#     #         del self
#     #     else:
#     #         self.name = name
#     #         self.id_department = id_de


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

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Groups.id
        elif column_name == 'name':
            return Groups.name
        elif column_name == 'id_department':
            return Groups.id_department
        elif column_name == 'lesson_plan':
            return Groups.lesson_plan.id
        else:
            return 0


class Degrees(Base):
    __tablename__ = 'degrees'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    teachers = relationship('Teachers', backref='degrees', cascade='all, delete-orphan')

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Degrees.id
        elif column_name == 'full_name':
            return Degrees.full_name
        elif column_name == 'short_name':
            return Degrees.short_name
        else:
            return 0


class Teachers(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_degree = Column(Integer, ForeignKey('degrees.id'))

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Teachers.id
        elif column_name == 'full_name':
            return Teachers.full_name
        elif column_name == 'short_name':
            return Teachers.short_name
        elif column_name == 'id_department':
            return Teachers.id_department
        elif column_name == 'id_degree':
            return Teachers.id_degree
        elif column_name == 'lesson_plan':
            return Teachers.lesson_plan.id
        else:
            return 0


class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    capacity = Column(Integer)
    additional_stuff = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))

    lessons = relationship('Lessons', backref='rooms', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='rooms', cascade='all, delete-orphan')

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Rooms.id
        elif column_name == 'name':
            return Rooms.name
        elif column_name == 'capacity':
            return Rooms.capacity
        elif column_name == 'additional_stuff':
            return Rooms.additional_stuff
        elif column_name == 'departments':
            return Rooms.departments
        else:
            return 0


class Subjects(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    lesson_plan = relationship('Lesson_plan', backref='subjects', cascade='all, delete-orphan')

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Subjects.id
        elif column_name == 'full_name':
            return Subjects.full_name
        elif column_name == 'short_name':
            return Subjects.short_name
        else:
            return 0


class Lesson_types(Base):
    __tablename__ = 'lesson_types'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    lesson_plan = relationship('Lesson_plan', backref='lesson_types', cascade='all, delete-orphan')

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Lesson_types.id
        elif column_name == 'full_name':
            return Lesson_types.full_name
        elif column_name == 'short_name':
            return Lesson_types.short_name
        else:
            return 0


class Weeks(Base):
    __tablename__ = 'weeks'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='weeks', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='weeks', cascade='all, delete-orphan')

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Weeks.id
        elif column_name == 'full_name':
            return Weeks.full_name
        elif column_name == 'short_name':
            return Weeks.short_name
        else:
            return 0


class Week_days(Base):
    __tablename__ = 'week_days'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='week_days', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='week_days', cascade='all, delete-orphan')

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Week_days.id
        elif column_name == 'full_name':
            return Week_days.full_name
        elif column_name == 'short_name':
            return Week_days.short_name
        else:
            return 0


class Lesson_times(Base):
    __tablename__ = 'lesson_times'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='lesson_times', cascade='all, delete-orphan')
    tmp_lessons = relationship('Tmp_lessons', backref='lesson_times', cascade='all, delete-orphan')

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Lesson_times.id
        elif column_name == 'full_name':
            return Lesson_times.full_name
        elif column_name == 'short_name':
            return Lesson_times.short_name
        else:
            return 0


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

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Lesson_plan.id
        elif column_name == 'id_subject':
            return Lesson_plan.id_subject
        elif column_name == 'id_lesson_type':
            return Lesson_plan.id_lesson_type
        elif column_name == 'times_for_2_week':
            return Lesson_plan.times_for_2_week
        elif column_name == 'needed_stuff':
            return Lesson_plan.needed_stuff
        elif column_name == 'capacity':
            return Lesson_plan.capacity
        elif column_name == 'split_groups':
            return Lesson_plan.split_groups
        elif column_name == 'param_checker':
            return Lesson_plan.param_checker
        elif column_name == 'groups':
            return Groups.id
        elif column_name == '_groups':
            return Lesson_plan.groups
        elif column_name == 'teachers':
            return Teachers.id
        elif column_name == '_teachers':
            return Lesson_plan.teachers
        else:
            return 0


class Lessons(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True)
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plan.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    id_lesson_time = Column(Integer, ForeignKey('lesson_times.id'))
    id_week_day = Column(Integer, ForeignKey('week_days.id'))
    id_week = Column(Integer, ForeignKey('weeks.id'))

    row_time = Column(Integer)

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Lessons.id
        elif column_name == 'id_lesson_plan':
            return Lessons.id_lesson_plan
        elif column_name == 'id_room':
            return Lessons.id_room
        elif column_name == 'id_lesson_time':
            return Lessons.id_lesson_time
        elif column_name == 'id_week_day':
            return Lessons.id_week_day
        elif column_name == 'id_week':
            return Lessons.id_week
        elif column_name == 'row_time':
            return Lessons.row_time
        else:
            return 0


class Tmp_lessons(Base):
    __tablename__ = 'tmp_lessons'

    id = Column(Integer, primary_key=True)
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plan.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    id_lesson_time = Column(Integer, ForeignKey('lesson_times.id'))
    id_week_day = Column(Integer, ForeignKey('week_days.id'))
    id_week = Column(Integer, ForeignKey('weeks.id'))

    row_time = Column(Integer)

    @staticmethod
    def get_column(column_name=''):
        if column_name == 'id':
            return Tmp_lessons.id
        elif column_name == 'id_lesson_plan':
            return Tmp_lessons.id_lesson_plan
        elif column_name == 'id_room':
            return Tmp_lessons.id_room
        elif column_name == 'id_lesson_time':
            return Tmp_lessons.id_lesson_time
        elif column_name == 'id_week_day':
            return Tmp_lessons.id_week_day
        elif column_name == 'id_week':
            return Tmp_lessons.id_week
        elif column_name == 'row_time':
            return Tmp_lessons.row_time
        else:
            return 0

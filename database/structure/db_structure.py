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
import re
from sqlalchemy import Column, Integer, String, ForeignKey, or_
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from database import db_codes

__all__ = [
    'Degrees', 'DepartmentRooms', 'Departments', 'Faculties', 'Groups',
    'GroupPlans', 'LessonPlans', 'TeacherPlans', 'LessonTimes',
    'LessonTypes', 'Lessons', 'Rooms', 'Subjects', 'Teachers', 'TmpLessons',
    'Universities', 'WeekDays', 'Weeks', 'Users', 'UserDepartments'
]
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


@as_declarative()
class Base(object):
    _columns = ['id']
    _links = []
    _associations = []

    def __init__(self, **kwargs):
        super(Base, self).__init__(**kwargs)

    @declared_attr
    def __tablename__(cls):
        s1 = first_cap_re.sub(r'\1_\2', cls.__name__)
        return all_cap_re.sub(r'\1_\2', s1).lower()

    @classmethod
    def single(cls):
        if cls.__name__ in ['Faculties', 'Universities']:
            return cls.__name__[:-2] + 'y'
        else:
            return cls.__name__[:-1]

    id = Column(Integer, primary_key=True)

    @classmethod
    def links(cls):
        # To return list of fields, which provide one-to-many relations
        return cls._links[:]

    @classmethod
    def associations(cls):
        # To return list of fields, which provide many-to-many relations
        return cls._associations[:]

    @classmethod
    def columns(cls):
        # To return list of fields, which are sql columns
        return cls._columns[:]

    @classmethod
    def fields(cls):
        # To return full list of class fields
        return cls.columns() + cls.associations() + cls.links()

    @classmethod
    def create(cls, session, **kwargs):
        # looks like it's working
        if isinstance(session, int):
            return db_codes['session']

        result = session.query(cls)

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.columns():
                return db_codes['wrong']
            else:
                result.filter(getattr(cls, key) == kwargs[key])

        if result.all():
            return db_codes['exists']
        else:
            session.add(cls(**kwargs))

        return db_codes['success']

    @classmethod
    def read(cls, session, all_=False, **kwargs):
        if isinstance(session, int):
            return db_codes['session']

        result = session.query(cls)

        if all_:
            return result.all()

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']
            elif isinstance(kwargs[key], list):
                # More lists
                elements = getattr(result.all()[0], key)
                if isinstance(elements, list):
                    result.filter(or_(
                        element.in_(kwargs[key]) for element in getattr(cls, key)
                    ))
                else:
                    result.filter(cls.id.in_(kwargs[key]))
            else:
                result.filter(getattr(cls, key) == kwargs[key])

        return result.all()

    @classmethod
    def update(cls, session, main_id, **kwargs):
        if isinstance(session, int):
            return db_codes['session']

        # No deleting first data
        if main_id == 1:
            return db_codes['reserved']

        result = cls.read(session, id=main_id)[0]

        # Check for existance
        if not result:
            return db_codes['absent']

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.columns():
                return db_codes['wrong']
            else:
                setattr(result, key, kwargs[key])

        if cls.read(session, **kwargs):
            return db_codes['exists']
        session.commit()

        return db_codes['success']

    @classmethod
    def delete(cls, session, main_id):
        # looks like it's working
        if isinstance(session, int):
            return db_codes['session']

        # No deleting first data
        if main_id == 1:
            return db_codes['reserved']

        result = cls.read(session, id=main_id)

        # Check for existence
        if not result:
            return db_codes['absent']

        # Reset links:
        for link in cls.links():
            linked = getattr(result, link)
            if isinstance(linked, list):
                for element in linked:
                    setattr(element, 'id_' + cls.single(), 1)
            else:
                setattr(linked, 'id_' + cls.single(), 1)

        for association in cls.associations():
            linked = getattr(result, association)
            for element in linked:
                getattr(element, cls.__tablename__).remove(result)

        session.delete(result)
        session.commit()
        return db_codes['success']


class Users(Base):
    nickname = Column(String)
    hashed_password = Column(String)
    status = Column(String)   # Expected values are 'admin' and 'method'

    # To give methodist user separated rights we need to create merging table
    # between User and Department, but if we don't - user can edit any table.
    departments = relationship(
        'Departments', secondary='user_departments', backref='users'
    )

    _columns = ['id', 'nickname', 'hashed_password']
    _associations = ['departments']
    error = db_codes['user']


class UserDepartments(Base):
    id_user = Column(Integer, ForeignKey('users.id'))
    id_department = Column(Integer, ForeignKey('departments.id'))

    _columns = ['id_user', 'id_department']
    error = db_codes['user']


class Universities(Base):
    full_name = Column(String)
    short_name = Column(String)

    faculties = relationship('Faculties', backref='university', cascade="all, delete-orphan")

    _columns = ['id', 'full_name', 'short_name']
    _links = ['faculties']
    error = db_codes['user']


class Faculties(Base):
    full_name = Column(String)
    short_name = Column(String)
    id_university = Column(Integer, ForeignKey('universities.id'))

    departments = relationship('Departments', backref='faculty', cascade="all, delete-orphan")

    _columns = ['id', 'full_name', 'short_name', 'id_university']
    _links = ['departments', 'university']
    error = db_codes['user']


class DepartmentRooms(Base):
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))

    _columns = ['id_room', 'id_department']
    error = db_codes['user']


class Departments(Base):
    full_name = Column(String)
    short_name = Column(String)
    id_faculty = Column(Integer, ForeignKey('faculties.id'))

    groups = relationship('Groups', backref='department', cascade="all, delete-orphan")
    teachers = relationship('Teachers', backref='department', cascade="all, delete-orphan")
    rooms = relationship('Rooms', secondary='department_rooms', backref='departments')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['groups', 'teachers', 'faculty']
    _associations = ['rooms']
    error = db_codes['user']


class GroupPlans(Base):
    id_group = Column(Integer, ForeignKey('groups.id'))
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plans.id'))

    _columns = ['id_group', 'id_lesson_plan']
    error = db_codes['user']


class TeacherPlans(Base):
    id_teacher = Column(Integer, ForeignKey('teachers.id'))
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plans.id'))

    _columns = ['id_teacher', 'id_lesson_plan']
    error = db_codes['user']


class Groups(Base):
    name = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))

    _columns = ['id', 'name', 'id_department']
    _links = ['department']
    _associations = ['lesson_plans']
    error = db_codes['user']


class Degrees(Base):
    full_name = Column(String)
    short_name = Column(String)

    teachers = relationship('Teachers', backref='degree', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['teachers']
    error = db_codes['user']


class Teachers(Base):
    full_name = Column(String)
    short_name = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_degree = Column(Integer, ForeignKey('degrees.id'))

    _columns = ['id', 'full_name', 'short_name', 'id_department', 'id_degree']
    _links = ['department', 'degree']
    _associations = ['lesson_plans']
    error = db_codes['user']


class Subjects(Base):
    full_name = Column(String)
    short_name = Column(String)

    lesson_plans = relationship('LessonPlans', backref='subject', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lesson_plans']
    error = db_codes['user']


class Rooms(Base):
    name = Column(String)
    capacity = Column(Integer)
    additional_stuff = Column(String)

    lessons = relationship('Lessons', backref='room', cascade='all, delete-orphan')
    tmp_lessons = relationship('TmpLessons', backref='room', cascade='all, delete-orphan')

    _columns = ['id', 'name', 'capacity', 'additional_stuff']
    _links = ['lessons', 'tmp_lessons']
    _associations = ['departments']
    error = db_codes['user']


class LessonTypes(Base):
    full_name = Column(String)
    short_name = Column(String)

    lesson_plans = relationship('LessonPlans', backref='lesson_type', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lesson_plans']
    error = db_codes['user']


class Weeks(Base):
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='week', cascade='all, delete-orphan')
    tmp_lessons = relationship('TmpLessons', backref='week', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lessons', 'tmp_lessons']
    error = db_codes['user']


class WeekDays(Base):
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='week_day', cascade='all, delete-orphan')
    tmp_lessons = relationship('TmpLessons', backref='week_day', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lessons', 'tmp_lessons']
    error = db_codes['user']


class LessonTimes(Base):
    full_name = Column(String)
    short_name = Column(String)

    lessons = relationship('Lessons', backref='lesson_time', cascade='all, delete-orphan')
    tmp_lessons = relationship('TmpLessons', backref='lesson_time', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lessons', 'tmp_lessons']
    error = db_codes['lesson_time']


class LessonPlans(Base):
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
    _links = ['subject', 'lesson_type', 'lessons']
    _associations = ['groups', 'teachers']
    error = db_codes['lesson_plan']


class Lessons(Base):
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plans.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    id_lesson_time = Column(Integer, ForeignKey('lesson_times.id'))
    id_week_day = Column(Integer, ForeignKey('week_days.id'))
    id_week = Column(Integer, ForeignKey('weeks.id'))

    row_time = Column(Integer)

    _columns = ['id', 'id_lesson_plan', 'id_room', 'id_lesson_time',
                'id_week_day', 'id_week', 'row_time']
    _links = ['lesson_plan', 'room', 'lesson_time', 'week_day', 'week']
    error = db_codes['temp_lesson']

    @classmethod
    def update(cls, session, main_id, **kwargs):
        pass

    @classmethod
    def create(cls, session, **kwargs):
        pass


class TmpLessons(Base):
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plans.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    id_lesson_time = Column(Integer, ForeignKey('lesson_times.id'))
    id_week_day = Column(Integer, ForeignKey('week_days.id'))
    id_week = Column(Integer, ForeignKey('weeks.id'))

    row_time = Column(Integer)

    _columns = ['id', 'id_lesson_plan', 'id_room', 'id_lesson_time',
                'id_week_day', 'id_week', 'row_time']
    _links = ['lesson_plan', 'room', 'lesson_time', 'week_day', 'week']
    error = db_codes['lesson']

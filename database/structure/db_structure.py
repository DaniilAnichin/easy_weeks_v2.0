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
import bcrypt
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, or_
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from database import db_codes, Logger
from gui.translate import shorten
logger = Logger()
__all__ = [
    'Degrees', 'DepartmentRooms', 'Departments', 'Faculties', 'Groups',
    'GroupPlans', 'LessonPlans', 'TeacherPlans', 'LessonTimes',
    'LessonTypes', 'Lessons', 'Rooms', 'Subjects', 'Teachers', 'Universities',
    'WeekDays', 'Weeks', 'Users', 'UserDepartments'
]
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


@as_declarative()
class Base(object):
    _columns = ['id']
    _links = []
    _associations = []
    id = Column(Integer, primary_key=True)

    def __init__(self, *args, **kwargs):
        logger.info('DB model init call invokes')   # Never called..
        super(Base, self).__init__(*args, **kwargs)

    @declared_attr
    def __tablename__(self):
        s1 = first_cap_re.sub(r'\1_\2', self.__name__)
        return all_cap_re.sub(r'\1_\2', s1).lower()

    @classmethod
    def single(cls):
        if cls.__tablename__ in ['faculties', 'universities']:
            return cls.__tablename__[:-2] + 'y'
        else:
            return cls.__tablename__[:-1]

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
        # Add fields and associations?
        if not set(kwargs.keys()) < set(cls.fields()):
            return db_codes['wrong']

        result = cls.read(session, **kwargs)

        if isinstance(result, int):
            return result
        elif result:
            return db_codes['exists']
        else:
            elem = cls(**kwargs)
            session.add(elem)

        return elem

    @classmethod
    def read(cls, session, all_=False, **kwargs):
        if isinstance(session, int):
            return db_codes['session']

        result = session.query(cls)

        if all_:
            # return result.all()
            return result.all()[1:]

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']
            elif isinstance(kwargs[key], list):
                example = cls.read(session, id=1)[0]
                if isinstance(getattr(example, key), list):
                    for item in kwargs[key]:
                        result = result.filter(getattr(cls, key).contains(item))
                else:
                    result = result.filter(getattr(cls, key).in_(kwargs[key]))
                # OK as parent select for lesson_plan and other will be modified
                # work proper for all 'easy' classes
            else:
                result = result.filter(getattr(cls, key) == kwargs[key])

        return result.all()

    @classmethod
    def update(cls, session, main_id, **kwargs):
        # looks like it's working
        # No deleting first data:
        if main_id == 1:
            return db_codes['reserved']

        result = cls.read(session, id=main_id)

        # Check for existence:
        if not result:
            return db_codes['absent']
        if isinstance(result, int):
            return result
        result = result[0]

        data = {}
        for field in cls.fields():
            data.update({field: getattr(result, field)})
        for key in kwargs.keys():
            data.update({key: kwargs[key]})
        if cls.read(session, **data):
            return db_codes['exists']


        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']
        for key in kwargs.keys():
            setattr(result, key, kwargs[key])

        session.commit()

        return db_codes['success']

    @classmethod
    def delete(cls, session, main_id):
        # looks like it's working
        # No deleting first data:
        if main_id == 1:
            return db_codes['reserved']

        result = cls.read(session, id=main_id)

        # Check for existence:
        if not result:
            return db_codes['absent']
        if isinstance(result, int):
            return result

        result = result[0]

        # Reset links:
        for link in cls.links():
            default_id = 1
            linked = getattr(result, link)
            if isinstance(linked, list):
                try:
                    if isinstance(linked[0], Departments):
                        default_id = 2
                except:
                    pass
                for element in linked:
                    setattr(element, 'id_' + cls.single(), 1)
            # else:
            #     setattr(linked, 'id_' + cls.single(), 1)
        for association in cls.associations():
            linked = getattr(result, association)
            for element in linked:
                getattr(element, cls.__tablename__).remove(result)

        # Delete:
        session.delete(result)
        session.commit()
        return db_codes['success']


class Users(Base):
    nickname = Column(String, unique=True)
    hashed_password = Column(String)
    status = Column(String)   # Expected values are 'admin' and 'method'
    message = Column(String)   # Message when giving an methodist request
    translated = u'Користувач'

    # def __init__(self, *args, **kwargs):
    #     password = kwargs.pop('password', '')
    #
    #     if not password:
    #         logger.error('No password passed')
    #         raise ValueError('No password passed')
    #     hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    #
    #     kwargs.update(hashed_password=hashed)
    #     super(Users, self).__init__(*args, **kwargs)
    #     logger.info('Hashed user %s password' % self.nickname)

    @classmethod
    def create(cls, session, **kwargs):
        password = kwargs.pop('password', '')
        if not password:
            logger.error('No password passed')
            raise ValueError('No password passed')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())

        kwargs.update(hashed_password=hashed)
        return super(Users, cls).create(session, **kwargs)

    def __unicode__(self):
        return self.nickname

    def authenticate(self, password):
        logger.info('User %s auth passing' % self.nickname)
        encoded = password.encode('cp1251')
        result = bcrypt.hashpw(encoded, self.hashed_password.encode('cp1251'))
        return self.hashed_password.encode('cp1251') == result

    # To give methodist user separated rights we need to create merging table
    # between User and Department, but if we don't - user can edit any table.
    departments = relationship(
        'Departments', secondary='user_departments', backref='users'
    )

    _columns = ['id', 'nickname', 'hashed_password', 'message', 'status']
    _associations = ['departments']
    # error = db_codes['user']


class UserDepartments(Base):
    id_user = Column(Integer, ForeignKey('users.id'))
    id_department = Column(Integer, ForeignKey('departments.id'))
    translated = u'Користувач-Кафедра'

    def __unicode__(self):
        return u'%d in %d' % (self.id_user, self.id_department)

    _columns = ['id_user', 'id_department']
    # error = db_codes['user_department']


class Universities(Base):
    full_name = Column(String)
    short_name = Column(String)
    translated = u'Університет'

    def __unicode__(self):
        return self.short_name

    faculties = relationship(
        'Faculties', backref='university', cascade='all, delete-orphan'
    )

    _columns = ['id', 'full_name', 'short_name']
    _links = ['faculties']
    # error = db_codes['university']


class Faculties(Base):
    full_name = Column(String)
    short_name = Column(String)
    id_university = Column(Integer, ForeignKey('universities.id'))
    translated = u'Факультет'

    def __unicode__(self):
        return self.short_name

    departments = relationship(
        'Departments', backref='faculty', cascade='all, delete-orphan'
    )

    _columns = ['id', 'full_name', 'short_name', 'id_university']
    _links = ['departments', 'university']
    # error = db_codes['faculty']


class DepartmentRooms(Base):
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    translated = u'Кімнати кафедри'

    def __unicode__(self):
        return u'%d in %d' % (self.id_room, self.id_department)

    _columns = ['id_room', 'id_department']
    # error = db_codes['user']


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
    # error = db_codes['department']


class GroupPlans(Base):
    id_group = Column(Integer, ForeignKey('groups.id'))
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plans.id'))
    translated = u'Заняття групи'

    def __unicode__(self):
        return u'%d in %d' % (self.id_group, self.id_lesson_plan)

    _columns = ['id_group', 'id_lesson_plan']
    # error = db_codes['user']


class TeacherPlans(Base):
    id_teacher = Column(Integer, ForeignKey('teachers.id'))
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plans.id'))
    translated = u'Заняття викладача'

    def __unicode__(self):
        return u'%d in %d' % (self.id_teacher, self.id_lesson_plan)

    _columns = ['id_teacher', 'id_lesson_plan']
    # error = db_codes['user']

# lesson_groups = Table('lesson_groups', Base.metadata,
#                       Column('id_lesson_plan', Integer, ForeignKey('lesson_plans.id')),
#                       Column('id_group', Integer, ForeignKey('groups.id')))
#
#
# lesson_teachers = Table('lesson_teachers', Base.metadata,
#                         Column('id_lesson_plan', Integer, ForeignKey('lesson_plans.id')),
#                         Column('id_teacher', Integer, ForeignKey('teachers.id')))


class Groups(Base):
    name = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))
    translated = u'Група'

    def __unicode__(self):
        return self.name

    _columns = ['id', 'name', 'id_department']
    _links = ['department']
    _associations = ['lesson_plans']
    # error = db_codes['group']


class Degrees(Base):
    full_name = Column(String)
    short_name = Column(String)
    translated = u'Ступінь'

    def __unicode__(self):
        return self.full_name

    teachers = relationship('Teachers', backref='degree', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['teachers']
    # error = db_codes['degree']


class Teachers(Base):
    full_name = Column(String)
    short_name = Column(String)
    id_department = Column(Integer, ForeignKey('departments.id'))
    id_degree = Column(Integer, ForeignKey('degrees.id'))
    translated = u'Викладач'

    def __unicode__(self):
        return self.full_name

    _columns = ['id', 'full_name', 'short_name', 'id_department', 'id_degree']
    _links = ['department', 'degree']
    _associations = ['lesson_plans']
    # error = db_codes['teacher']


class Subjects(Base):
    full_name = Column(String)
    short_name = Column(String)
    translated = u'Предмет'

    def __unicode__(self):
        return self.full_name

    lesson_plans = relationship('LessonPlans', backref='subject', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lesson_plans']
    # error = db_codes['subject']


class Rooms(Base):
    name = Column(String)
    capacity = Column(Integer)
    additional_stuff = Column(String)
    translated = u'Аудиторія'

    def __unicode__(self):
        return self.name

    lessons = relationship('Lessons', backref='room', cascade='all, delete-orphan')

    _columns = ['id', 'name', 'capacity', 'additional_stuff']
    _links = ['lessons']
    _associations = ['departments']
    # error = db_codes['room']

    @classmethod
    def read(cls, session, all_=False, **kwargs):
        if isinstance(session, int):
            return db_codes['session']

        result = session.query(cls)

        if all_:
            # return result.all()
            return result.all()[1:]

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']
            elif isinstance(kwargs[key], list):
                if key == 'lessons':
                    try:
                        if not isinstance(kwargs[key][0], int):
                            kwargs[key] = [lesson.id for lesson in kwargs[key]]
                    except IndexError:
                        pass
                    result = result.filter(LessonPlans.lessons.any(
                        Lessons.id.in_(kwargs[key])
                    ))
                else:
                    result = result.filter(getattr(cls, key).in_(kwargs[key]))
            else:
                if key == 'lessons':
                    if not isinstance(kwargs[key], int):
                        kwargs[key] = [lesson.id for lesson in kwargs[key]]
                    result = result.filter(LessonPlans.lessons.any(
                        Lessons.id.in_(kwargs[key])
                    ))
                else:
                    result = result.filter(getattr(cls, key) == kwargs[key])

        return result.all()


class LessonTypes(Base):
    full_name = Column(String)
    short_name = Column(String)
    translated = u'Тип'

    def __unicode__(self):
        return self.full_name

    lesson_plans = relationship('LessonPlans', backref='lesson_type', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lesson_plans']
    # error = db_codes['user']


class Weeks(Base):
    full_name = Column(String)
    short_name = Column(String)
    translated = u'Тиждень'

    def __unicode__(self):
        return self.full_name

    lessons = relationship('Lessons', backref='week', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lessons']
    # error = db_codes['']


class WeekDays(Base):
    full_name = Column(String)
    short_name = Column(String)
    translated = u'День'

    def __unicode__(self):
        return self.full_name

    lessons = relationship('Lessons', backref='week_day', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lessons']
    # error = db_codes['user']


class LessonTimes(Base):
    full_name = Column(String)
    short_name = Column(String)
    translated = u'Час'

    def __unicode__(self):
        return self.full_name

    lessons = relationship('Lessons', backref='lesson_time', cascade='all, delete-orphan')

    _columns = ['id', 'full_name', 'short_name']
    _links = ['lessons']
    # error = db_codes['lesson_time']


class LessonPlans(Base):
    id_subject = Column(Integer, ForeignKey('subjects.id'))
    id_lesson_type = Column(Integer, ForeignKey('lesson_types.id'))
    translated = u'Навчальній план'

    def __unicode__(self):
        return u'{0},\n{1}\nз {2}\nз {3}'.format(
            unicode(self.lesson_type),
            unicode(self.subject),
            u', '.join([unicode(group) for group in self.groups]),
            u', '.join([unicode(teacher) for teacher in self.teachers])
        )

    amount = Column(Integer, default=2)
    needed_stuff = Column(String, default='')
    capacity = Column(Integer, default=32)
    split_groups = Column(Integer)

    param_checker = Column(String)

    lessons = relationship('Lessons', backref='lesson_plan', cascade='all, delete-orphan')
    groups = relationship('Groups', secondary='group_plans', backref='lesson_plans')
    teachers = relationship('Teachers', secondary='teacher_plans', backref='lesson_plans')
    # groups = relationship('Groups', secondary='lesson_groups', backref='lesson_plans')
    # teachers = relationship('Teachers', secondary='lesson_teachers', backref='lesson_plans')

    _columns = ['id', 'id_subject', 'id_lesson_type', 'amount',
                'needed_stuff', 'capacity', 'split_groups', 'param_checker']
    _links = ['subject', 'lesson_type', 'lessons']
    _associations = ['groups', 'teachers']
    # error = db_codes['lesson_plan']

    @classmethod
    def create(cls, session, **kwargs):
        # looks like it's working
        # Add fields and associations?
        if not set(kwargs.keys()) < set(cls.fields()):
            return db_codes['wrong']

        result = cls.read(session, **kwargs)

        if isinstance(result, int):
            return result
        elif result:
            return db_codes['exists']
        else:
            elem = cls(**kwargs)
            # t_checker = u''
            # g_checker = u''
            # for t in kwargs['teachers']:
            #     t_checker += unicode(t)+u','
            # for g in kwargs['groups']:
            #     g_checker += unicode(g) + u','
            t_checker = u','.join(kwargs.get('teachers', []))
            g_checker = u','.join(kwargs.get('groups', []))
            elem.param_checker = u'%d,%d,%s,%s,%d,%d,%d' % (kwargs['id_subject'], kwargs['id_lesson_type'],
                                                            g_checker, t_checker, kwargs['amount'],
                                                            kwargs['split_groups'], kwargs['capacity'])
            session.add(elem)

        return elem

    @classmethod
    def read(cls, session, all_=False, **kwargs):
        if isinstance(session, int):
            return db_codes['session']

        result = session.query(cls)

        if all_:
            # return result.all()
            return result.all()[1:]

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']
            elif isinstance(kwargs[key], list):
                if key == 'groups':
                    try:
                        if not isinstance(kwargs[key][0], int):
                            kwargs[key] = [lesson.id for lesson in kwargs[key]]
                    except IndexError:
                        pass
                    result = result.filter(LessonPlans.groups.any(
                             Groups.id.in_(kwargs[key])))
                elif key == 'teachers':
                    try:
                        if not isinstance(kwargs[key][0], int):
                            kwargs[key] = [lesson.id for lesson in kwargs[key]]
                    except IndexError:
                        pass
                    result = result.filter(LessonPlans.teachers.any(
                             Teachers.id.in_(kwargs[key])))
                elif key == 'lessons':
                    try:
                        if not isinstance(kwargs[key][0], int):
                            kwargs[key] = [lesson.id for lesson in kwargs[key]]
                    except IndexError:
                        pass
                    result = result.filter(LessonPlans.lessons.any(
                        Lessons.id.in_(kwargs[key])
                    ))
                else:
                    result = result.filter(getattr(cls, key).in_(kwargs[key]))
            else:
                if key == 'groups':
                    if not isinstance(kwargs[key], int):
                        kwargs[key] = [lesson.id for lesson in kwargs[key]]
                    result = result.filter(getattr(LessonPlans, key).any(
                             Groups.id == kwargs[key]))
                elif key == 'teachers':
                    if not isinstance(kwargs[key], int):
                        kwargs[key] = [lesson.id for lesson in kwargs[key]]
                    result = result.filter(getattr(LessonPlans, key).any(
                             Teachers.id == kwargs[key]))
                elif key == 'lessons':
                    if not isinstance(kwargs[key], int):
                        kwargs[key] = [lesson.id for lesson in kwargs[key]]
                    result = result.filter(LessonPlans.lessons.any(
                        Lessons.id.in_(kwargs[key])
                    ))
                else:
                    result = result.filter(getattr(cls, key) == kwargs[key])

        return result.all()


class Lessons(Base):
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plans.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    id_lesson_time = Column(Integer, ForeignKey('lesson_times.id'))
    id_week_day = Column(Integer, ForeignKey('week_days.id'))
    id_week = Column(Integer, ForeignKey('weeks.id'))
    is_temp = Column(Boolean, default=False)
    is_empty = Column(Boolean, default=False)
    row_time = Column(Integer)
    translated = u'Заняття'
    week_ids = range(2, 4)
    day_ids = range(2, 8)
    time_ids = range(2, 7)
    table_size = len(week_ids) * len(day_ids) * len(time_ids)

    def __init__(self, *args, **kwargs):
        row_time = kwargs.get('row_time', '')

        if row_time != '':
            kwargs.update(self.from_row(row_time))

        super(Lessons, self).__init__(*args, **kwargs)
        self.row_time = self.to_row(self.time())
        # logger.info('Passed lesson init')

    def __unicode__(self):
        return u'%s у час %s' % (unicode(self.lesson_plan), unicode(self.row_time))

    def __eq__(self, other):
        fields = self.fields()
        fields.pop(fields.index('id'))
        fields.pop(fields.index('is_temp'))
        result = True
        for field in fields:
            result = result and (getattr(self, field) == getattr(other, field))
        return result

    def time(self):
        return dict(
            id_week=self.id_week,
            id_week_day=self.id_week_day,
            id_lesson_time=self.id_lesson_time
        )

    def set_time(self, time):
        for key in time.keys():
            setattr(self, key, time[key])
        self.row_time = self.to_row(time)

    @classmethod
    def from_row(cls, row_time):
        number = row_time % len(cls.time_ids)
        row_time /= len(cls.time_ids)
        day = row_time % len(cls.day_ids)
        row_time /= len(cls.day_ids)
        week = row_time % len(cls.week_ids)
        return dict(
            id_week=cls.week_ids[week],
            id_week_day=cls.day_ids[day],
            id_lesson_time=cls.time_ids[number]
        )

    @classmethod
    def to_row(cls, time):
        try:
            row_time = cls.time_ids.index(time['id_lesson_time'])
            row_time += cls.day_ids.index(time['id_week_day']) * len(cls.time_ids)
            row_time += cls.week_ids.index(time['id_week']) * len(cls.day_ids) * len(cls.time_ids)
        except KeyError:
            row_time = cls.time_ids.index(time['lesson_time'].id)
            row_time += cls.day_ids.index(time['week_day'].id) * len(cls.time_ids)
            row_time += cls.week_ids.index(time['week'].id) * len(cls.day_ids) * len(cls.time_ids)
        return row_time

    @classmethod
    def bad_time(cls):
        return dict(id_week=1, id_week_day=1, id_lesson_time=1)

    @classmethod
    def get_empty(cls, **kwargs):
        defaults = dict(
            id_week=cls.week_ids[0],
            id_week_day=cls.day_ids[0],
            id_lesson_type=cls.time_ids[0]
        )
        if 'rooms' in kwargs.keys():
            defaults.pop('rooms')
            defaults.update({'rooms': kwargs['rooms']})

        if set(kwargs.keys()) < set(cls.fields()):
            return Lessons(is_temp=True, is_empty=True)
        else:
            return Lessons(is_temp=True, id_empty=True, **kwargs)

    def make_temp(self, session, time=None):
        if not time:
            time = self.time()
        temp_lesson = Lessons.create(session, id_lesson_plan=self.id_lesson_plan,
                                     is_temp=True, id_room=self.id_room, **time)
        if isinstance(temp_lesson, int) and temp_lesson == db_codes['exists']:
            logger.debug('RLY?')
            return Lessons.read(session, id_lesson_plan=self.id_lesson_plan,
                                is_temp=True, id_room=self.id_room, **time)[0]
        elif isinstance(temp_lesson, int):
            return temp_lesson

        return temp_lesson

    @classmethod
    def get_plan(cls, session, **data):
        needed_keys = list(set(data.keys()) & set(LessonPlans.fields()))
        exists = LessonPlans.read(session, **{key: data[key] for key in needed_keys})
        if isinstance(exists, list):
            return exists[0]

        lesson_plan = LessonPlans.create(session, **{key: data[key] for key in needed_keys})
        if isinstance(lesson_plan, int):
            return lesson_plan

        return lesson_plan

    def to_table(self, *args):
        # Make lesson to string to view it on the table
        if self.is_empty:
            return u''
        result = shorten(unicode(self.lesson_plan.subject), 15)
        if 'teachers' not in args:
            teachers = u', '.join(
                unicode(teacher) for teacher in self.lesson_plan.teachers
            )
            result += u'\n' + shorten(teachers, 15)
        if 'rooms' not in args:
            result += u'\n' + shorten(unicode(self.room), 15)
        if 'groups' not in args:
            groups = u', '.join(unicode(group) for group in self.lesson_plan.groups)
            result += u'\n' + shorten(groups, 15)
        return result

    _columns = ['id', 'id_lesson_plan', 'id_room', 'id_lesson_time',
                'id_week_day', 'id_week', 'row_time', 'is_temp', 'is_empty']
    _links = ['lesson_plan', 'room', 'lesson_time', 'week_day', 'week']
    # error = db_codes['lessons']

    @classmethod
    def read(cls, session, all_=False, **kwargs):
        if not set(kwargs.keys()).intersection({'is_temp', 'id', 'all_'}):
            kwargs.update(dict(is_temp=False))
        return super(Lessons, cls).read(session, all_=all_, **kwargs)

    @classmethod
    def create(cls, session, **kwargs):
        if not set(kwargs.keys()) < set(cls.fields()):
            return db_codes['wrong']
        if 'row_time' not in kwargs.keys():
            kwargs.update(row_time=cls.to_row(kwargs))
            # logger.debug('No row_time passed')

        result = cls.read(session, **kwargs)

        if isinstance(result, int):
            return result
        elif result and not kwargs.get('is_temp', True):
            return db_codes['exists']

        if not kwargs.get('is_temp', True):
            try:
                cur_lp = kwargs['lesson_plan']
                lesson_num = Lessons.read(session, lesson_plan=kwargs['lesson_plan'])
            except KeyError:
                cur_lp = LessonPlans.read(session, id=kwargs['id_lesson_plan'])[0]
                lesson_num = Lessons.read(session, id_lesson_plan=kwargs['id_lesson_plan'])

            if kwargs['row_time'] < 0 or kwargs['row_time'] > cls.table_size:
                return db_codes['time']
            if cur_lp.amount <= lesson_num:
                return db_codes['wrong']

            exists = cls.exists(session, **kwargs)
            if exists:
                return exists

        lesson = Lessons(**kwargs)
        session.add(lesson)
        session.commit()

        return lesson

    @classmethod
    def update(cls, session, main_id, **kwargs):
        # No deleting first data:
        if main_id == 1:
            return db_codes['reserved']

        result = cls.read(session, id=main_id)

        # Check for existence:
        if not result:
            return db_codes['absent']
        if isinstance(result, int):
            return result

        if not kwargs.get('is_temp', True):
            if cls.read(session, **kwargs):
                return db_codes['exists']
            exists = cls.exists(session, **kwargs)
            if exists:
                return exists

        result = result[0]

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.columns():
                return db_codes['wrong']
            else:
                setattr(result, key, kwargs[key])

        result.row_time = cls.to_row(result.time())
        session.commit()

        return db_codes['success']

    @classmethod
    def exists(cls, session, **kwargs):
        cur_lp = LessonPlans.read(session, id=kwargs['id_lesson_plan'])[0]

        for lesson in Lessons.read(session, lesson_plan=LessonPlans.read(
                session, groups=cur_lp.groups
        )):
            if lesson.row_time == kwargs['row_time']:
                return db_codes['group']

        for lesson in Lessons.read(session, lesson_plan=LessonPlans.read(
                session, teachers=cur_lp.teachers
        )):
            if lesson['row_time'] == kwargs['row_time']:
                return db_codes['teacher']

        if kwargs['id_room'] != 1:
            for lesson in Lessons.read(session, row_time=kwargs['row_time']):
                if lesson.id_room == kwargs['id_room']:
                    return db_codes['room']

        return None

    @classmethod
    def move_temp(cls, session):
        pass
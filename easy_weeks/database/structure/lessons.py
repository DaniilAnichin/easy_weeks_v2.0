#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from easy_weeks.database import db_codes, Logger
from easy_weeks.database.structure import Base
from easy_weeks.gui.translate import shorten
logger = Logger()


class Lessons(Base):
    id_lesson_plan = Column(Integer, ForeignKey('lesson_plans.id'))
    id_room = Column(Integer, ForeignKey('rooms.id'))
    id_lesson_time = Column(Integer, ForeignKey('lesson_times.id'))
    id_week_day = Column(Integer, ForeignKey('week_days.id'))
    id_week = Column(Integer, ForeignKey('weeks.id'))
    is_temp = Column(Boolean, default=False)
    is_empty = Column(Boolean, default=False)
    row_time = Column(Integer)
    translated = 'Заняття'
    week_ids = range(2, 4)
    day_ids = range(2, 8)
    time_ids = range(2, 7)
    table_size = len(week_ids) * len(day_ids) * len(time_ids)

    def __init__(self, *args, row_time: int=None, **kwargs):
        if row_time is not None:
            kwargs.update(self.from_row(row_time))

        super(Lessons, self).__init__(*args, **kwargs)
        self.row_time = self.to_row(self.time())

    def __str__(self) -> str:
        return f'{self.lesson_plan} у час {self.row_time}'

    def __eq__(self, other) -> bool:
        if self.row_time != other.row_time:
            return False
        if self.room.name != other.room.name:
            return False
        if self.lesson_plan.subject.short_name != other.lesson_plan.subject.short_name:
            return False

        self_teacher_set = {teacher.short_name for teacher in self.lesson_plan.teachers}
        other_teacher_set = {teacher.short_name for teacher in other.lesson_plan.teachers}
        if self_teacher_set != other_teacher_set:
            return False

        self_group_set = {group.name for group in self.lesson_plan.groups}
        other_group_set = {group.name for group in other.lesson_plan.groups}
        return self_group_set == other_group_set

    def time(self) -> dict:
        return {
            'id_week': self.id_week,
            'id_week_day': self.id_week_day,
            'id_lesson_time': self.id_lesson_time,
        }

    def set_time(self, time: dict) -> None:
        for key in time.keys():
            setattr(self, key, time[key])
        self.row_time = self.to_row(time)

    @classmethod
    def from_row(cls, row_time: int) -> dict:
        times, days, weeks = len(cls.time_ids), len(cls.day_ids), len(cls.week_ids)
        number = row_time % times
        row_time //= times
        day = row_time % days
        row_time //= days
        week = row_time % weeks
        return {
            'id_week': cls.week_ids[week],
            'id_week_day': cls.day_ids[day],
            'id_lesson_time': cls.time_ids[number]
        }

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
    def bad_time(cls) -> dict:
        return {'id_week': 1, 'id_week_day': 1, 'id_lesson_time': 1}

    @classmethod
    def get_empty(cls, **kwargs):
        defaults = {
            'id_week': cls.week_ids[0],
            'id_week_day': cls.day_ids[0],
            'id_lesson_type': cls.time_ids[0],
        }
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
        return temp_lesson

    def to_table(self) -> str:
        # Convert lesson to string to view it on the table
        if self.is_empty:
            return ''

        teachers = ', '.join(str(teacher) for teacher in self.lesson_plan.teachers)
        groups = ', '.join(str(group) for group in self.lesson_plan.groups)

        result = '\n'.join((
            shorten(self.lesson_plan.subject),
            shorten(teachers),
            shorten(self.room),
            shorten(groups)
        ))
        return result

    _columns = ['id', 'id_lesson_plan', 'id_room', 'id_lesson_time',
                'id_week_day', 'id_week', 'row_time', 'is_temp', 'is_empty']
    _links = ['lesson_plan', 'room', 'lesson_time', 'week_day', 'week']
    # error = db_codes['lessons']

    @classmethod
    def read(cls, session, all_=False, **kwargs):
        if not set(kwargs.keys()).intersection({'is_temp', 'id', 'all_'}):
            kwargs.update({'is_temp': False})
        return super(Lessons, cls).read(session, all_=all_, **kwargs)

    @classmethod
    def create(cls, session, **kwargs):
        from easy_weeks.database.structure import LessonPlans
        if not set(kwargs.keys()) < set(cls.fields()):
            return db_codes['wrong']
        if 'row_time' not in kwargs.keys():
            kwargs.update(row_time=cls.to_row(kwargs))

        if 'is_temp' not in kwargs.keys():
            kwargs.update(is_temp=False)

        result = cls.read(session, **kwargs)

        if isinstance(result, int):
            return result
        elif result and not kwargs.get('is_temp', True):
            return db_codes['exists']

        if not kwargs.get('is_temp', True):
            try:
                cur_lp = kwargs['lesson_plan']
            except KeyError:
                cur_lp = LessonPlans.read(session, id=kwargs['id_lesson_plan'])[0]
            lessons = Lessons.read(session, id_lesson_plan=cur_lp.id)
            lesson_num = len(lessons)

            if kwargs['row_time'] < 0 or kwargs['row_time'] > cls.table_size:
                return db_codes['time']
            if cur_lp.amount <= lesson_num:
                return db_codes['amount']

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

        result = result[0]
        data = {}
        for field in cls.columns():
            data.update({field: getattr(result, field)})
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']
            data.update({key: kwargs[key]})

        if not data['is_temp']:
            doubles = cls.read(session, **data)
            if doubles and doubles[0].id != main_id:
                return db_codes['exists']
            exists = cls.exists(session, main_id, **data)
            if exists:
                return exists

        # Global filter loop:
        for key in kwargs.keys():
            setattr(result, key, kwargs[key])

        result.row_time = cls.to_row(result.time())
        session.commit()

        return db_codes['success']

    @classmethod
    def exists(cls, session, main_id=None, **kwargs):
        from easy_weeks.database.structure import LessonPlans

        cur_lp = LessonPlans.read(session, id=kwargs['id_lesson_plan'])[0]
        params = {'is_temp': False}
        if not kwargs.get('is_empty', False):
            params.update({'is_empty': False})

        for lesson in Lessons.read(session, id_lesson_plan=[
            lp.id for lp in LessonPlans.read(session, groups=cur_lp.groups)
        ], **params):
            if lesson.row_time == kwargs['row_time']:
                if lesson.id != main_id:
                    return db_codes['group']

        for lesson in Lessons.read(session, id_lesson_plan=[
            lp.id for lp in LessonPlans.read(session, teachers=cur_lp.teachers)
        ], **params):
            if lesson.row_time == kwargs['row_time']:
                if lesson.id != main_id:
                    return db_codes['teacher']

        if kwargs['id_room'] != 1:
            for lesson in Lessons.read(session, row_time=kwargs['row_time'], **params):
                if lesson.id_room == kwargs['id_room']:
                    if lesson.id != main_id:
                        return db_codes['room']

        return False

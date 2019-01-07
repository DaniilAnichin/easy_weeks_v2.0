#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from easy_weeks.database import db_codes, Logger
from easy_weeks.database.structure import Base
logger = Logger()


class LessonPlans(Base):
    id_subject = Column(Integer, ForeignKey('subjects.id'))
    id_lesson_type = Column(Integer, ForeignKey('lesson_types.id'))
    amount = Column(Integer, default=2)
    needed_stuff = Column(String, default='')
    capacity = Column(Integer, default=32)
    split_groups = Column(Integer)

    param_checker = Column(String)

    lessons = relationship('Lessons', backref='lesson_plan', cascade='all, delete-orphan')
    groups = relationship('Groups', secondary='group_plans', backref='lesson_plans')
    teachers = relationship('Teachers', secondary='teacher_plans', backref='lesson_plans')

    translated = 'Навчальній план'

    def __str__(self):
        groups = ', '.join([str(group) for group in self.groups])
        teachers = ', '.join([str(teacher) for teacher in self.teachers])
        return f'{self.lesson_type},\n{self.subject}\nз {groups}\nз {teachers}'

    _columns = ['id', 'id_subject', 'id_lesson_type', 'amount',
                'needed_stuff', 'capacity', 'split_groups', 'param_checker']
    _links = ['subject', 'lesson_type', 'lessons']
    _associations = ['groups', 'teachers']

    @classmethod
    def create(cls, session, **kwargs):
        if not set(kwargs.keys()) < set(cls.fields()):
            return db_codes['wrong']

        kwargs.setdefault('split_groups', 0)
        checker = LessonPlans.make_params(**kwargs)
        if not checker:
            return db_codes['params']

        result = cls.read(session, param_checker=checker)
        if isinstance(result, int):
            return result

        if result:
            return db_codes['exists']

        kwargs['param_checker'] = checker
        elem = cls(**kwargs)
        session.add(elem)
        session.commit()
        return elem

    @staticmethod
    def make_params(**kwargs):
        for key in ['subject', 'lesson_type']:
            if key in kwargs.keys():
                kwargs.update({f'id_{key}': kwargs[key].id})
        try:
            t_checker = ','.join([str(teach.id) for teach in kwargs['teachers']])
            g_checker = ','.join([str(group.id) for group in kwargs['groups']])
            # Add two letters to avoid groups & teacher rearranging
            checker = f"{kwargs['id_subject']},{kwargs['id_lesson_type']},g{g_checker},t{t_checker}," \
                      f"{kwargs['amount']},{kwargs['split_groups']},{kwargs['capacity']}"
        except KeyError:
            checker = ''
        return checker

    @classmethod
    def update(cls, session, main_id, **kwargs):
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
            if key not in cls.fields():
                return db_codes['wrong']
            data.update({key: kwargs[key]})

        checker = LessonPlans.make_params(**data)
        if not checker:
            return db_codes['params']
        doubles = cls.read(session, param_checker=checker)
        if doubles and doubles[0].id != main_id:
            return db_codes['exists']

        # Global filter loop:
        for key in kwargs.keys():
            setattr(result, key, kwargs[key])
        result.param_checker = checker

        session.commit()
        return db_codes['success']

    @classmethod
    def read(cls, session, all_=False, **kwargs):
        from easy_weeks.database.structure import Groups, Teachers, Lessons

        if isinstance(session, int):
            return db_codes['session']

        result = session.query(cls)

        if all_:
            return result.all()[1:]

        if 'param_checker' in kwargs.keys():
            return result.filter(LessonPlans.param_checker == kwargs['param_checker']).all()

        # Global filter loop:
        for key in kwargs.keys():
            if key not in cls.fields():
                return db_codes['wrong']

            if key in ['groups', 'teachers', 'rooms']:
                if not isinstance(kwargs[key], list):
                    kwargs[key] = [kwargs[key]]

                kwargs[key] = [item.id if not isinstance(item, int) else item
                               for item in kwargs[key]]
                if key == 'groups':
                    result = result.filter(LessonPlans.groups.any(Groups.id.in_(kwargs[key])))
                elif key == 'teachers':
                    result = result.filter(LessonPlans.teachers.any(Teachers.id.in_(kwargs[key])))
                elif key == 'lessons':
                    result = result.filter(LessonPlans.lessons.any(Lessons.id.in_(kwargs[key])))
            else:
                if isinstance(kwargs[key], list):
                    result = result.filter(getattr(cls, key).in_(kwargs[key]))
                else:
                    result = result.filter(getattr(cls, key) == (kwargs[key]))

        return result.all()

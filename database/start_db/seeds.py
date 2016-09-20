#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database import Logger, db_codes_output
from database.structure import db_structure
from database.structure.db_structure import *
__all__ = ['create_common', 'create_custom', 'create_empty']
logger = Logger()


def create_empty(session):
    # All DB models():
    session.add_all([
        Universities(short_name=u'Unknown', full_name=u'Unknown'),
        Faculties(short_name=u'Unknown', full_name=u'Unknown', id_university=1),
        Departments(short_name=u'Unknown', full_name=u'Unknown', id_faculty=1),
        Degrees(short_name=u'Unknown', full_name=u'Unknown'),
        Teachers(short_name=u'Unknown', full_name=u'Unknown', id_department=1, id_degree=1),
        Subjects(short_name=u'Unknown', full_name=u'Unknown'),
        LessonTypes(short_name=u'Unknown', full_name=u'Unknown'),
        Weeks(short_name=u'Unknown', full_name=u'Unknown'),
        WeekDays(short_name=u'Unknown', full_name=u'Unknown'),
        LessonTimes(short_name=u'Unknown', full_name=u'Unknown'),
        Rooms(name=u'Unknown', capacity=320, additional_stuff=''),
        Groups(name=u'Unknown', id_department=1),
        LessonPlans(
            id_subject=1, id_lesson_type=1, amount=4, needed_stuff='',
            capacity=32, split_groups=0
        ),
        Lessons(id_lesson_plan=1, id_room=1, is_empty=True,
                id_lesson_time=2, id_week_day=2, id_week=2),
    ])
    Users.create(session, nickname=u'Test', status=u'method', password='password')

    # Association tables:
    session.add_all([
        DepartmentRooms(id_department=1, id_room=1),
        TeacherPlans(id_lesson_plan=1, id_teacher=1),
        GroupPlans(id_lesson_plan=1, id_group=1),
        UserDepartments(id_user=1, id_department=1)
    ])

    session.commit()
    return session


def create_common(session):
    # Adding week days, degrees, times, etc
    session.add_all([
        Universities(short_name=u'Невизначено', full_name=u'Невизначено'),
        Faculties(short_name=u'Невизначено', full_name=u'Невизначено', id_university=2),
        Departments(short_name=u'Невизначено', full_name=u'Невизначено', id_faculty=2),
        Rooms(name=u'Невизначено', capacity=320, additional_stuff=''),

        Degrees(short_name=u'ас.', full_name=u'асистент'),
        Degrees(short_name=u'вик.', full_name=u'викладач'),
        Degrees(short_name=u'доц.', full_name=u'доцент'),
        Degrees(short_name=u'дек.', full_name=u'декан'),
        Degrees(short_name=u'зав.каф.', full_name=u'завідувач кафедри'),
        Degrees(short_name=u'проф.', full_name=u'професор'),
        Degrees(short_name=u'ст.вик.', full_name=u'старший викладач'),

        LessonTypes(short_name=u'Лек', full_name=u'Лекція'),
        LessonTypes(short_name=u'Прак', full_name=u'Практика'),
        LessonTypes(short_name=u'Лаб', full_name=u'Лабораторна'),

        Weeks(short_name=u'І', full_name=u'Перший тиждень'),
        Weeks(short_name=u'ІІ', full_name=u'Другий тиждень'),

        WeekDays(short_name=u'Пн', full_name=u'Понеділок'),
        WeekDays(short_name=u'Вт', full_name=u'Вівторок'),
        WeekDays(short_name=u'Ср', full_name=u'Середа'),
        WeekDays(short_name=u'Чт', full_name=u'Четвер'),
        WeekDays(short_name=u'Пт', full_name=u'П\'ятниця'),
        WeekDays(short_name=u'Сб', full_name=u'Субота'),
        WeekDays(short_name=u'Нд', full_name=u'Неділя'),

        LessonTimes(short_name=u'1', full_name=u'8:30-10:05'),
        LessonTimes(short_name=u'2', full_name=u'10:25-12:00'),
        LessonTimes(short_name=u'3', full_name=u'12:20-13:55'),
        LessonTimes(short_name=u'4', full_name=u'14:15-15:50'),
        LessonTimes(short_name=u'5', full_name=u'16:10-17:45'),
        LessonTimes(short_name=u'6', full_name=u'18:05-19:40'),
    ])

    Users.create(session, nickname=u'Admin', status=u'admin', password='easy_weeks_admin'),
    Users.create(session, nickname=u'Method', status=u'method', password='easy_weeks_method')

    session.commit()
    return session


def create_custom(session):
    # Complete this staff
    session.add_all([
        Universities(short_name=u'НТУУ «КПІ»',
                     full_name=u'Національний технічний університет України '
                               u'«Київський політехнічний інститут»'),

        Faculties(id_university=3, short_name=u'ФІОТ',
                  full_name=u'Інформатики та обчислюваної техніки'),

        Departments(id_faculty=3, short_name=u'ТК',
                    full_name=u'Технiчної кiбернетики'),
        Departments(id_faculty=3, short_name=u'ОТ',
                    full_name=u'Обчислювальної технiки'),
        Departments(id_faculty=3, short_name=u'АУТС',
                    full_name=u'Автоматики i управлiння в технiчних системах'),
        Departments(id_faculty=3, short_name=u'АСОІУ',
                    full_name=u'Автоматизованих систем обробки iнформацiї та управлiння'),
    ])
    session.commit()

    group_prefixes = [
        'ia', 'ik', 'io', 'ip', 'is', 'it'
    ]

    return session


def update_departments(session, cls_name, **data):
    for dept_name in data.keys():
        department = Departments.read(session, short_name=dept_name)[0]
        cls = getattr(db_structure, cls_name)
        for element_name in data[dept_name]:
            param = 'full_name' if cls_name == 'Teachers' else 'name'
            element = cls.read(session, **{param: element_name})[0]
            logger.debug('Element: %s' % unicode(element))
            logger.debug('Department: %s' % unicode(department))
            try:
                element.departments
                logger.debug('Association')
                logger.debug(db_codes_output[cls.update(session, main_id=element.id, departments=[department])])
            except AttributeError:
                logger.debug(db_codes_output[cls.update(session, main_id=element.id, department=department)])
                logger.debug('Link')


def drop_departments(session, cls_name, department_id=2):
    department = Departments.read(session, id=department_id)[0]
    cls = getattr(db_structure, cls_name)
    elements = cls.read(session, all_=True)
    for element in elements:
        param = 'full_name' if cls_name == 'Teachers' else 'name'
        logger.debug('Element: %s' % unicode(element))
        logger.debug('Department: %s' % unicode(department))
        try:
            element.departments
            logger.debug('Association')
            logger.debug(db_codes_output[cls.update(session, main_id=element.id, departments=[department])])
        except AttributeError:
            logger.debug(db_codes_output[cls.update(session, main_id=element.id, department=department)])
            logger.debug('Link')


if __name__ == "__main__":
    pass

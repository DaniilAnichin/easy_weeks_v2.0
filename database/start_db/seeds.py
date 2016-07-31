#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bcrypt
from database.structure.db_structure import *


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
        Lessons(id_lesson_plan=1, id_room=1, id_lesson_time=1, id_week_day=1, id_week=1),
        TmpLessons(id_lesson_plan=1, id_room=1, id_lesson_time=1, id_week_day=1, id_week=1),
        Users(nickname='Test', status='method', hashed_password=bcrypt.hashpw('password', bcrypt.gensalt()))
    ])

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

        LessonTimes(short_name=u'1', full_name=u'8:30-10:05'),
        LessonTimes(short_name=u'2', full_name=u'10:25-12:00'),
        LessonTimes(short_name=u'3', full_name=u'12:20-13:55'),
        LessonTimes(short_name=u'4', full_name=u'14:15-15:50'),
        LessonTimes(short_name=u'5', full_name=u'16:10-17:45'),
        LessonTimes(short_name=u'6', full_name=u'18:05-19:40'),

        Users(nickname='Admin', status='admin', hashed_password=bcrypt.hashpw('easy_weeks_admin', bcrypt.gensalt())),
        Users(nickname='Method', status='method', hashed_password=bcrypt.hashpw('easy_weeks_method', bcrypt.gensalt()))
    ])

    session.commit()
    return session


def create_custom(session):
    # Complete this staff
    session.add_all([
        Departments(short_name=u'ТК', full_name=u'Техн')
    ])
    session.commit()
    return session

#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        Lesson_types(short_name=u'Unknown', full_name=u'Unknown'),
        Weeks(short_name=u'Unknown', full_name=u'Unknown'),
        Week_days(short_name=u'Unknown', full_name=u'Unknown'),
        Lesson_times(short_name=u'Unknown', full_name=u'Unknown'),
        Rooms(name=u'Unknown', capacity=320, additional_stuff=''),
        Groups(name=u'Unknown', id_department=1),
        Lesson_plans(
            id_subject=1, id_lesson_type=1, amount=4, needed_stuff='',
            capacity=32, split_groups=0
        ),
        Lessons(id_lesson_plan=1, id_room=1, id_lesson_time=1, id_week_day=1, id_week=1),
        Tmp_lessons(id_lesson_plan=1, id_room=1, id_lesson_time=1, id_week_day=1, id_week=1)
    ])

    # Association tables:
    session.add_all([
        Department_rooms(id_department=1, id_room=1),
        Teacher_plans(id_lesson_plan=1, id_teacher=1),
        Group_plans(id_lesson_plan=1, id_group=1)
    ])

    session.commit()
    return session


def create_common(session):
    session.add_all([
        Degrees(short_name=u'ас.', full_name=u'асистент'),
        Degrees(short_name=u'вик.', full_name=u'викладач'),
        Degrees(short_name=u'доц.', full_name=u'доцент'),
        Degrees(short_name=u'дек.', full_name=u'декан'),
        Degrees(short_name=u'зав.каф.', full_name=u'завідувач кафедри'),
        Degrees(short_name=u'проф.', full_name=u'професор'),
        Degrees(short_name=u'ст.вик.', full_name=u'старший викладач'),

        Lesson_types(short_name=u'Лек', full_name=u'Лекція'),
        Lesson_types(short_name=u'Прак', full_name=u'Практика'),
        Lesson_types(short_name=u'Лаб', full_name=u'Лабораторна'),

        Weeks(short_name=u'І', full_name=u'Перший тиждень'),
        Weeks(short_name=u'ІІ', full_name=u'Другий тиждень'),

        Week_days(short_name=u'Пн', full_name=u'Понеділок'),
        Week_days(short_name=u'Вт', full_name=u'Вівторок'),
        Week_days(short_name=u'Ср', full_name=u'Середа'),
        Week_days(short_name=u'Чт', full_name=u'Четвер'),
        Week_days(short_name=u'Пт', full_name=u'П\'ятниця'),
        Week_days(short_name=u'Сб', full_name=u'Субота'),

        Lesson_times(short_name=u'1', full_name=u'8:30-10:05'),
        Lesson_times(short_name=u'2', full_name=u'10:25-12:00'),
        Lesson_times(short_name=u'3', full_name=u'12:20-13:55'),
        Lesson_times(short_name=u'4', full_name=u'14:15-15:50'),
        Lesson_times(short_name=u'5', full_name=u'16:10-17:45'),
        Lesson_times(short_name=u'6', full_name=u'18:05-19:40')
    ])

    session.commit()
    return session

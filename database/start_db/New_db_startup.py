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
import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import DATABASE_DIR, DATABASE_NAME
from database.structure import *
from database.structure.db_structure import Base


def create_new_database(path=DATABASE_NAME):
    full_path = os.path.join(DATABASE_DIR, path)
    if os.path.isfile(full_path):
        print "Data base with same name already exits"
        return -1
    en = create_engine('sqlite:///%s' % full_path)
    Base.metadata.create_all(en)
    session_m = sessionmaker(bind=en)
    s = session_m()
    s.add_all([
        Universities(short_name=unicode("Unknown", 'utf-8'), full_name=unicode("Unknown", 'utf-8')),
        Faculties(short_name=unicode("Unknown", 'utf-8'), full_name=unicode("Unknown", 'utf-8'),
                  id_university=1),
        Departments(short_name=unicode("Unknown", 'utf-8'), full_name=unicode("Unknown", 'utf-8'),
                    id_faculty=1),
        Degrees(short_name=unicode("Unknown", 'utf-8'), full_name=unicode("Unknown", 'utf-8')),
        Degrees(short_name=unicode("ас.", 'utf-8'), full_name=unicode("асистент", 'utf-8')),
        Degrees(short_name=unicode("вик.", 'utf-8'), full_name=unicode("викладач", 'utf-8')),
        Degrees(short_name=unicode("доц.", 'utf-8'), full_name=unicode("доцент", 'utf-8')),
        Degrees(short_name=unicode("дек.", 'utf-8'), full_name=unicode("декан", 'utf-8')),
        Degrees(short_name=unicode("зав.каф.", 'utf-8'), full_name=unicode("завідувач кафедри", 'utf-8')),
        Degrees(short_name=unicode("проф.", 'utf-8'), full_name=unicode("професор", 'utf-8')),
        Degrees(short_name=unicode("ст.вик.", 'utf-8'), full_name=unicode("старший викладач", 'utf-8')),
        Teachers(short_name=unicode("Unknown", 'utf-8'), full_name=unicode("Unknown", 'utf-8'),
                 id_department=1, id_degree=1),
        Lesson_types(short_name=unicode("Unknown", 'utf-8'), full_name=unicode("Unknown", 'utf-8')),
        Lesson_types(short_name=unicode("Лек", 'utf-8'), full_name=unicode("Лекція", 'utf-8')),
        Lesson_types(short_name=unicode("Прак", 'utf-8'), full_name=unicode("Практика", 'utf-8')),
        Lesson_types(short_name=unicode("Лаб", 'utf-8'), full_name=unicode("Лабораторна", 'utf-8')),
        Weeks(short_name=unicode("1", 'utf-8'), full_name=unicode("І Тиждень", 'utf-8')),
        Weeks(short_name=unicode("2", 'utf-8'), full_name=unicode("ІІ Тиждень", 'utf-8')),
        Week_days(short_name=unicode("Пн", 'utf-8'), full_name=unicode("Понеділок", 'utf-8')),
        Week_days(short_name=unicode("Вт", 'utf-8'), full_name=unicode("Вівторок", 'utf-8')),
        Week_days(short_name=unicode("Ср", 'utf-8'), full_name=unicode("Середа", 'utf-8')),
        Week_days(short_name=unicode("Чт", 'utf-8'), full_name=unicode("Четвер", 'utf-8')),
        Week_days(short_name=unicode("Пт", 'utf-8'), full_name=unicode("П'ятниця", 'utf-8')),
        Week_days(short_name=unicode("Сб", 'utf-8'), full_name=unicode("Субота", 'utf-8')),
        Lesson_times(short_name=unicode("1", 'utf-8'), full_name=unicode("8:30-10:05", 'utf-8')),
        Lesson_times(short_name=unicode("2", 'utf-8'), full_name=unicode("10:25-12:00", 'utf-8')),
        Lesson_times(short_name=unicode("3", 'utf-8'), full_name=unicode("12:20-13:55", 'utf-8')),
        Lesson_times(short_name=unicode("4", 'utf-8'), full_name=unicode("14:15-15:50", 'utf-8')),
        Lesson_times(short_name=unicode("5", 'utf-8'), full_name=unicode("16:10-17:45", 'utf-8')),
        Rooms(name=unicode("Unknown", 'utf-8'), capacity=320, additional_stuff='')
    ])

    s.commit()
    return s


def connect_database(path=DATABASE_NAME):
    full_path = os.path.join(DATABASE_DIR, path)
    if not os.path.isfile(full_path):
        print "Data base does not exits"
        return -1
    en = create_engine('sqlite:///%s' % full_path)
    Base.metadata.create_all(en)
    session_m = sessionmaker(bind=en)
    s = session_m()
    return s


def main():
    s = create_new_database('Test.db')
    # s = connect_database('Test.db')
    new_university(s,
                    unicode("Національний технічний університет України 'Київський політехнічний інститут'", 'utf-8'),
                   unicode("НТУУ'КПІ'", 'utf-8'))
    new_faculty(s, unicode("Факультет інформатики та очислювальної техніки", 'utf-8'),
                unicode("ФІОТ", 'utf-8'), 2)
    new_department(s,
                   unicode("Кафедра технічної кібернетики", 'utf-8'),
                   unicode("ТК", 'utf-8'), 2)
    new_group(s, unicode("ік-51", 'utf-8'), 2)
    new_group(s, unicode("ік-52", 'utf-8'), 2)
    new_teacher(s, '', unicode("Орловський І. В.", 'utf-8'), 2, 4)
    new_room(s, unicode("438", 'utf-8'), 64, '', [2])
    new_subject(s, unicode("Вища математика -2", 'utf-8'), unicode("ВМ-2", 'utf-8'))
    new_lesson_plan(s, 1, 2, [1, 2], [2], 3, 0, 64, '')
    new_lesson_plan(s, 1, 3, [1], [2], 2, 0, 32, '')
    new_lesson(s, 1, 2, 0)
    new_lesson(s, 2, 2, 1)
    new_tmp_lesson(s, 1, 2, 32)
    # print select_universities(s, short_name=unicode("НТУУ'КПІ'", 'utf-8'))
    # print select_groups(s, id_department=2)
    # print select_lesson_plans(s, [1])
    # print select_lesson_plans(s, groups=[1])
    # print select_lessons(s, [1])
    # print select_lessons(s, id_lesson_plan=[1, 2, 3])
    # delete_university(s, 2)
    # delete_group(s, 1)
    print select_lesson_plans(s, groups=[1, 2])
    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())

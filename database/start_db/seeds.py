#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from database import Logger, db_codes, db_codes_output, structure, \
    DEPARTMENTS, SEEDS
from database.structure import *
__all__ = ['create_common', 'create_custom', 'create_empty',
           'update_departments', 'drop_departments']
logger = Logger()


def create_empty(session):
    # All DB models():
    # !!Cannot move this to json, cause this data should not be changed!!
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
    with open(SEEDS) as out:
        seed_data = json.load(out)['common']

    session_data = []
    for class_name in seed_data.keys():
        cls = getattr(structure, class_name)
        for values in seed_data[class_name]:
            session_data.append(cls(**values))

    # Adding week days, degrees, times, etc
    session.add_all(session_data)

    Users.create(session, nickname=u'Admin', status=u'admin', password='easy_weeks_admin'),
    Users.create(session, nickname=u'Method', status=u'method', password='easy_weeks_method')

    session.commit()
    return session


def create_custom(session):
    with open(SEEDS) as out:
        seed_data = json.load(out)['custom']

    session_data = []
    for class_name in seed_data.keys():
        cls = getattr(structure, class_name)
        for values in seed_data[class_name]:
            session_data.append(cls(**values))

    session.add_all(session_data)
    session.commit()
    return session


def part_departments(session, cls_name, **data):
    for dept_name in data.keys():
        department = Departments.read(session, short_name=dept_name)[0]
        cls = getattr(structure, cls_name)
        for element_name in data[dept_name]:
            param = 'full_name' if cls_name == 'Teachers' else 'name'
            try:
                element = cls.read(session, **{param: element_name})[0]
            except IndexError:
                logger.error('No such element: %s' % element_name)
                continue

            if hasattr(element, 'departments'):
                result = cls.update(session, main_id=element.id, departments=[department])
            else:
                result = cls.update(session, main_id=element.id, department=department)
            if result not in [db_codes['exists'], db_codes['success']]:
                logger.debug(db_codes_output[result])


def get_departments(session, cls_name, **data):
    for dept_name in data.keys():
        department = Departments.read(session, short_name=dept_name)[0]
        cls = getattr(structure, cls_name)
        for element_name in data[dept_name]:
            param = 'full_name' if cls_name == 'Teachers' else 'name'
            try:
                element = cls.read(session, **{param: element_name})[0]
            except IndexError:
                logger.error('No such element: %s' % element_name)
                continue

            if hasattr(element, 'departments'):
                result = cls.update(session, main_id=element.id, departments=[department])
            else:
                result = cls.update(session, main_id=element.id, department=department)
            if result not in [db_codes['exists'], db_codes['success']]:
                logger.debug(db_codes_output[result])


def drop_departments(session, cls_name, department_id=2):
    department = Departments.read(session, id=department_id)[0]
    cls = getattr(structure, cls_name)
    elements = cls.read(session, all_=True)
    for element in elements:
        if hasattr(element, 'departments'):
            result = cls.update(session, main_id=element.id, departments=[department])
        else:
            result = cls.update(session, main_id=element.id, department=department)
        if result not in [db_codes['exists'], db_codes['success']]:
            logger.debug(db_codes_output[result])


def update_departments(session):
    with open(DEPARTMENTS) as out:
        department_data = json.load(out)

    part_departments(session, cls_name='Teachers', **department_data['Teachers'])
    part_departments(session, cls_name='Groups', **department_data['Groups'])
    part_departments(session, cls_name='Rooms', **department_data['Rooms'])


def save_departments(session):
    teachers_data = {}
    groups_data = {}
    rooms_data = {}
    departments = Departments.read(session, all_=True)
    for dept in departments:
        teacher_names = map(lambda x: x.full_name, dept.teachers)
        teachers_data.update({dept.short_name: teacher_names})

        group_names = map(lambda x: x.name, dept.groups)
        groups_data.update({dept.short_name: group_names})

        room_names = map(lambda x: x.name, dept.rooms)
        rooms_data.update({dept.short_name: room_names})
    data = {
        'Teachers': teachers_data,
        'Groups': groups_data,
        'Rooms': rooms_data
    }
    import codecs
    with codecs.open(DEPARTMENTS, 'w', encoding='utf-8') as out:
        json.dump(data, out, indent=4, ensure_ascii=False)

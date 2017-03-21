#!/usr/bin/python
# -*- coding: utf-8 -*-#
import json
import urllib
from database import Logger, db_codes, db_codes_output, GROUPS, TEACHERS
from database.structure import *
from database.select_table import is_free
logger = Logger()

lessons_url = "http://api.rozklad.org.ua/v2/teachers/%d/lessons"
gr_lessons_url = "http://api.rozklad.org.ua/v2/groups/%d/lessons"
teachers_url = "http://api.rozklad.org.ua/v2/teachers/?search={'query': '%s'}"
groups_url = "http://api.rozklad.org.ua/v2/groups/?search={'query': '%s'}"


def get_teacher_id(session, teacher_short_name, add_teacher=True):
    # Already checking in outer function
    # if isinstance(teacher_short_name, unicode):
    #     teacher_short_name = teacher_short_name.encode('utf-8')
    teacher_surname = teacher_short_name.split(' ')[1]
    if '\'' in teacher_surname:
        teacher_surname = teacher_surname.split('\'')[0]
    unicode_name = unicode(teacher_short_name, 'utf-8')
    teacher_url = teachers_url % teacher_surname

    info = json.load(urllib.urlopen(teacher_url))

    if info['statusCode'] != 200:
        logger.debug('Bad response: ' + info['statusCode'] + ' ' + teacher_url.decode('utf-8'))
        return -1

    for row in info['data']:
        if row['teacher_short_name'] == unicode_name:
            cur_teacher_id = int(row['teacher_id'])
            if add_teacher:
                create_teacher(session, row, teacher_short_name)
            return cur_teacher_id
    for row in info['data']:
        # For bad only:
        if row['teacher_short_name'] == u'' and \
                        unicode(teacher_surname, 'utf-8') in row['teacher_name']:
            row.update(dict(
                teacher_short_name=unicode_name,
            ))
        if row['teacher_short_name'] == unicode_name:
            cur_teacher_id = int(row['teacher_id'])
            if add_teacher:
                create_teacher(session, row, teacher_short_name)
            return cur_teacher_id

    logger.info('Empty response: ' + teacher_url.decode('utf-8'))
    return -1


def get_group_id(session, group_name, add_group=True):
    # Already checking in outer function
    # if isinstance(teacher_short_name, unicode):
    #     teacher_short_name = teacher_short_name.encode('utf-8')
    group_url = groups_url % group_name
    info = json.load(urllib.urlopen(group_url))

    if info['statusCode'] != 200:
        logger.debug('Bad response: ' + info['statusCode'] + ' ' + group_url.decode('utf-8'))
        return -1

    for row in info['data']:
        if row['group_full_name'] == group_name:
            group_id = int(row['teacher_id'])
            if add_group:
                Groups.create(session, name=group_name)
            return group_id

    logger.info('Empty response: ' + group_url.decode('utf-8'))
    return -1


def create_groups(session, groups_path=GROUPS):
    if isinstance(session, int):
        return db_codes['session']

    with open(groups_path, 'r') as out:
        group_names = json.load(out)

    ids = []

    for name in group_names:
        if isinstance(name, list):
            ids.append(name[1])
            continue

        group_name = unicode(name, 'utf-8')

        created = False
        info = json.load(urllib.urlopen(groups_url % name))
        if info['statusCode'] != 200:
            logger.debug('Bad response: ' + group_name.decode('utf-8'))
            return -1

        for row in info['data']:
            if row['group_full_name'] == group_name:
                created = True
                res = Groups.create(session, name=group_name)
                if isinstance(res, int):
                    logger.debug('Creating groups: ' + db_codes_output[res])
                ids.append(int(row['group_id']))

        if not created:
            logger.info('Empty response: ' + group_name.decode('utf-8'))

    return ids


def create_teachers(session, teachers_path=TEACHERS):
    if isinstance(session, int):
        return db_codes['session']

    with open(teachers_path, 'r') as out:
        teacher_names = json.load(out)

    ids = []

    for name in teacher_names:
        if isinstance(name, list):
            ids.append(name[1])
        else:
            ids.append(get_teacher_id(session, name))

    return ids


def create_teacher(session, row, teacher_short_name):
    full_name = row['teacher_name']
    short_name = unicode(' '.join(teacher_short_name.split(' ')[1:]), 'utf-8')
    default_department_id = 2
    degree_name = unicode(teacher_short_name.split(' ')[0], 'utf-8')
    degree = Degrees.read(session, short_name=degree_name)
    if isinstance(degree, int):
        logger.debug('Looking for degree: ' + db_codes_output[degree])
        degree_id = 2
    elif len(degree) > 0:
        degree_id = degree[0].id
    else:
        logger.debug('No degree found: ' + degree_name)
        degree_id = 2

    teacher = Teachers.create(
        session,
        full_name=full_name,
        short_name=short_name,
        id_department=default_department_id,
        id_degree=degree_id
    )

    if isinstance(teacher, int):
        logger.debug(db_codes_output[teacher])


def teacher_update(session, teacher_name, add_teacher=True):

    if isinstance(teacher_name, list):
        teacher_id = teacher_name[1]
        teacher_name = teacher_name[0]
        if isinstance(teacher_name, unicode):
            teacher_name = teacher_name.encode('utf-8')
        get_teacher_id(session, teacher_name, add_teacher)
    else:
        if isinstance(teacher_name, unicode):
            teacher_name = teacher_name.encode('utf-8')
        teacher_id = get_teacher_id(session, teacher_name, add_teacher)

    teacher_name = unicode(' '.join(teacher_name.split(' ')[1:]), 'utf-8')
    if teacher_id == -1:
        # logger.debug('Teacher not found')
        return -1
    teacher = Teachers.read(
        session,
        short_name=teacher_name
    )
    if isinstance(teacher, list):
        teacher = teacher[0]
    else:
        logger.debug('Teacher model not found')
        return -1

    cur_url = lessons_url % teacher_id
    info = json.load(urllib.urlopen(cur_url))
    if info['statusCode'] != 200:
        logger.debug('Bad response: ' + str(info['statusCode']) + ' ' + cur_url.decode('utf-8'))
        return -1

    department_id = 2
    for lesson in info['data']:
        row_time = int(lesson['lesson_number']) - 1 + \
            5 * (int(lesson['day_number']) - 1) + \
            30 * (int(lesson['lesson_week']) - 1)
        # Creating Rooms, Groups and Subjects
        groups = []
        for group in lesson['groups']:
            db_group = Groups.read(session, name=group['group_full_name'])
            if not db_group:
                db_group = Groups.create(
                    session, name=group['group_full_name'], id_department=department_id
                )
            elif isinstance(db_group, list):
                db_group = db_group[0]
            if isinstance(db_group, int):
                logger.debug('Creating/Reading group: ' + db_codes_output[db_group])
            else:
                groups.append(db_group)

        # Calculating capacity
        groups_number = len(groups)
        if groups_number < 3:
            cap = 70
        else:
            cap = 35 * groups_number
        if len(lesson['lesson_room']) < 5:
            cap = 256

        # Room:
        if lesson['lesson_room'] in ['', '-18']:
            lesson['lesson_room'] = teacher_name + lesson['lesson_id']
        db_room = Rooms.read(session, name=lesson['lesson_room'])
        if not db_room:
            db_room = Rooms.create(
                session, name=lesson['lesson_room'], capacity=cap, additional_stuff=''
            )
        elif isinstance(db_room, list):
            db_room = db_room[0]
        if isinstance(db_room, int):
            logger.debug('Creating/Reading room: ' + db_codes_output[db_room])
            continue

        # Subject:
        db_subject = Subjects.read(session, full_name=lesson['lesson_full_name'])
        if not db_subject:
            db_subject = Subjects.create(
                session, full_name=lesson['lesson_full_name'], short_name=lesson['lesson_name']
            )
        elif isinstance(db_subject, list):
            db_subject = db_subject[0]
        if isinstance(db_subject, int):
            logger.debug('Creating/Reading subject: ' + db_codes_output[db_subject])
            continue

        # Collecting LessonPlans data
        lesson_type = LessonTypes.read(session, short_name=lesson['lesson_type'])
        if isinstance(lesson_type, int) or not lesson_type:
            lesson_type = LessonTypes.read(session, short_name=u'Лек')
        if isinstance(lesson_type, int):
            logger.debug('Creating/Reading subject: ' + db_codes_output[lesson_type])
            continue
        else:
            lesson_type = lesson_type[0]

        lesson_plan_info = {
            'id_subject': db_subject.id,  # Subject
            'id_lesson_type': lesson_type.id,     # Lesson Type
            'groups': groups,  # Groups
        }
        lesson_plan = LessonPlans.read(session, teachers=[teacher], **lesson_plan_info)
        if isinstance(lesson_plan, list) and len(lesson_plan) > 0:
            lesson_plan = lesson_plan[0]
            LessonPlans.update(session, main_id=lesson_plan.id, amount=lesson_plan.amount + 1)
        else:
            lesson_plan = LessonPlans.read(session, **lesson_plan_info)
            if isinstance(lesson_plan, list) and len(lesson_plan) > 0:
                lesson_plan = lesson_plan[0]
                LessonPlans.update(
                    session, main_id=lesson_plan.id,
                    teachers=(lesson_plan.teachers + [teacher])
                )

            else:
                lesson_plan = LessonPlans.create(
                    session,
                    amount=1,
                    split_groups=0,
                    capacity=32 * groups_number,
                    param_checker=u'',
                    teachers=[teacher],
                    **lesson_plan_info
                )
                if isinstance(lesson_plan, int):
                    logger.debug('Creating LP: ' + db_codes_output[lesson_plan])

        if not isinstance(lesson_plan, LessonPlans):
            logger.debug('Ploblem while loading LP model')
            continue

        # Going to create lesson
        new_lesson = Lessons.create(
            session,
            id_lesson_plan=lesson_plan.id,
            id_room=db_room.id,
            row_time=row_time
        )
        if isinstance(new_lesson, int):
            logger.debug('Error while creating Lesson: ' + db_codes_output[new_lesson])
            logger.debug('At ' + str(row_time))
            # logger.debug('LP amount: ' + str(lesson_plan.amount))
            # logger.debug('id: %d, Subject: %s' % (lesson_plan.id, db_subject.full_name))

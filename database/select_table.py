#!/usr/bin/python
# -*- coding: utf-8 -*- #
from database import Logger, db_codes, db_codes_output, structure
from database.structure import *
__all__ = ['get_table', 'check_table', 'save_table', 'recover_empty',
           'clear_empty', 'clear_temp', 'find_free', 'undefined_lp',
           'get_element', 'get_name']
logger = Logger()


def get_table(session, element):
    if isinstance(session, int):
        return db_codes['session']
    # check data_type and data
    data_type = element.__tablename__
    logger.debug('Data: %s' % get_name(element))
    if data_type == 'rooms':
        params = dict(id_room=element.id)
    else:
        lesson_plan_ids = [lp.id for lp in LessonPlans.read(
            session, **{data_type: element.id}
        )]
        params = dict(id_lesson_plan=lesson_plan_ids)

    rettable = [[[None
                  for i in range(len(Lessons.time_ids))]
                 for j in range(len(Lessons.day_ids))]
                for k in range(len(Lessons.week_ids))]

    for week_id in Lessons.week_ids:
        for day_id in Lessons.day_ids:
            for time_id in Lessons.time_ids:
                week = Lessons.week_ids.index(week_id)
                day = Lessons.day_ids.index(day_id)
                time = Lessons.time_ids.index(time_id)

                lessons = Lessons.read(
                    session, id_week=week_id, id_week_day=day_id,
                    id_lesson_time=time_id, **params
                )
                if isinstance(lessons, list) and lessons:
                    # logger.debug('On %d we have %d lessons for %s' %
                    #              (lesson1.row_time, len(lessons), get_name(element)))
                    rettable[week][day][time] = lessons[0].make_temp(session)
                    res = Lessons.update(session, lessons[0].id, is_empty=True)
                    # logger.debug('Lesson empted?: {}'.format(db_codes_output[res]))
                else:
                    rettable[week][day][time] = Lessons.read(session, id=1)[0]
    return rettable


def undefined_lp(session, element=None):
    if isinstance(session, int):
        return db_codes['session']

    result = []
    # check data_type and data
    if not element:
        lesson_plans = LessonPlans.read(session, all_=True)
    else:
        data_type = element.__tablename__
        lesson_plans = LessonPlans.read(session, **{data_type: element.id})
    for plan in lesson_plans:
        unsorted = plan.amount - len(Lessons.read(session, id_lesson_plan=plan.id))
        if unsorted > 0:
            result.append(plan)
    return result


def check_part(session, element):
    data = {
        'Groups': lambda group: dict(id_lesson_plan=[lp.id for lp in group.lesson_plans]),
        'Teachers': lambda teach: dict(id_lesson_plan=[lp.id for lp in teach.lesson_plans]),
        'Rooms': lambda room: dict(id_room=room.id)
    }

    part_data = data[element.__class__.__name__](element)
    lessons = Lessons.read(session, is_temp=[False, True], is_empty=False, **part_data)
    time_list = [lesson.row_time for lesson in lessons]
    duplicates = [time for time in set(time_list) if time_list.count(time) > 1]

    for time in duplicates:
        if hasattr(element, 'short_name'):
            logger.info('Problem with %s at %s' % (element.short_name, time))
        else:
            logger.info('Problem with %s at %s' % (element.name, time))
        return duplicates

    return db_codes['success']


def check_table(session, only_temp=False):
    if isinstance(session, int):
        return db_codes['session']

    # Can optimize by reading not the all groups/teachers/rooms
    if only_temp:
        lessons = Lessons.read(session, is_temp=True)
        groups = []
        teachers = []
        rooms = []
        for l in lessons:
            for g in l.lesson_plan.groups:
                if not groups.count(g):
                    groups.append(g)
            for t in l.lesson_plan.teachers:
                if not teachers.count(t):
                    teachers.append(t)
            if not rooms.count(l.room):
                rooms.append(l.room)
    else:
        groups = Groups.read(session, all_=True)
        teachers = Teachers.read(session, all_=True)
        rooms = Rooms.read(session, all_=True)

    elements = {
        'Group': groups,
        'Teacher': teachers,
        'Room': rooms,
    }

    # This is awful for now
    overlaying = []
    for key in elements.keys():
        for element in elements[key]:
            if hasattr(element, 'capacity') and element.capacity >= 256:
                continue
            res = check_part(session, element)
            if res != db_codes['success']:
                for time in res:
                    if not overlaying.count(time):
                        overlaying.append(time)
    if overlaying:
        return overlaying

    logger.info('Database is correct')
    return db_codes['success']


def find_duplicates(session, old_session, main_teacher):
    new_lessons = Lessons.read(
        session,
        id_lesson_plan=[lp.id for lp in LessonPlans.read(session, teachers=[main_teacher.id])]
    )
    duplicates = []
    for lesson in new_lessons:
        params = {
            'row_time': lesson.row_time,
            'id_lesson_plan': [
                lp.id for lp in LessonPlans.read(
                    old_session,
                    groups=[
                        group.id for group in Groups.read(
                            old_session, name=[
                                gro.name for gro in lesson.lesson_plan.groups
                                ]
                        )
                        ]
                )
                ]
        }
        grouper = Lessons.read(old_session, **params)
        if grouper and not isinstance(grouper, int):
            if not lesson.lesson_plan.teachers[0].short_name == \
                    grouper[0].lesson_plan.teachers[0].short_name:
                duplicates.append(lesson.row_time)
                continue
        params = {
            'row_time': lesson.row_time,
            'room': Rooms.read(old_session, name=lesson.room.name)[0]
        }
        roomer = Lessons.read(old_session, **params)
        if roomer:
            if not lesson.lesson_plan.teachers[0].short_name == \
                    roomer[0].lesson_plan.teachers[0].short_name:
                duplicates.append(lesson.row_time)
    return duplicates


def save_table(session):
    if isinstance(session, int):
        return db_codes['session']

    result = check_table(session)
    if result == db_codes['success']:
        clear_empty(session)
        for lesson in Lessons.read(session, is_temp=True):
            ret = lesson.update(session, lesson.id, is_temp=False)
            # logger.degub('Edited?: {}'.format(db_codes_output[ret]))
    return result


def clear_empty(session):
    if isinstance(session, int):
        return db_codes['session']

    lessons = Lessons.read(session, is_empty=True)
    # Skips the first empty lesson:
    for lesson in lessons[1:]:
        ret = Lessons.delete(session, main_id=lesson.id)
        # logger.degub('Deleted?: {}'.format(db_codes_output[ret]))
    return db_codes['success']


def clear_temp(session):
    if isinstance(session, int):
        return db_codes['session']

    lessons = Lessons.read(session, is_temp=True)
    for lesson in lessons:
        ret = Lessons.delete(session, main_id=lesson.id)
        # logger.degub('Deleted?: {}'.format(db_codes_output[ret]))


def recover_empty(session):
    if isinstance(session, int):
        return db_codes['session']

    lessons = Lessons.read(session, is_empty=True)
    for lesson in lessons[1:]:
        ret = Lessons.update(session, main_id=lesson.id, is_empty=False)
        # logger.degub('Restored?: {}'.format(db_codes_output[ret]))
    return db_codes['success']


def is_free(session, cls, main_id, **kwargs):
    if cls == Rooms:
        lessons = Lessons.read(session, id_room=main_id, **kwargs)
        if lessons:
            return False
        return True
    else:
        lesson_plans = LessonPlans.read(session, **{cls.__tablename__: main_id})

        for lesson_plan in lesson_plans:
            lessons = Lessons.read(session, lesson_plan=lesson_plan, **kwargs)
            if lessons:
                return False
        return True


def find_free(session, cls, **kwargs):
    classmates = cls.read(session, all_=True)
    result = []
    department = kwargs.pop('department', None)

    for classmate in classmates:
        if hasattr(classmate, 'departments'):
            departments = classmate.departments
        else:
            departments = [classmate.department]

        if department in departments and is_free(session, cls, classmate.id, **kwargs):
            result.append(classmate)

    return result


def get_element(session, data_type, data_id):
    if isinstance(session, int):
        return db_codes['session']

    result = getattr(structure, data_type.capitalize()).read(session, id=data_id)

    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    return result


def get_name(element):
    if hasattr(element, 'name'):
        result = element.name
    elif hasattr(element, 'full_name'):
        result = element.full_name
    else:
        result = str(element)
    return result


def same_tables(first_session, second_session, teacher):
    first_table = get_table(first_session, teacher)
    second_table = get_table(second_session, Teachers.read(
        second_session, short_name=teacher.short_name
    )[0])
    for i in range(len(first_table)):
        for j in range(len(first_table[i])):
            for k in range(len(first_table[i][j])):
                lesson = first_table[i][j][k]
                second = second_table[i][j][k]
                if lesson.is_empty and second.is_empty:
                    continue
                if lesson.is_empty or second.is_empty:
                    return False
                if not lesson == second:
                    return False
    return True

if __name__ == '__main__':
    from database.start_db.db_startup import connect_database

    first_db = connect_database()
    second_db = connect_database('FICT_timetable2.db')

    teacher = Teachers.read(first_db, id=20)[0]
    logger.debug(same_tables(first_db, second_db, teacher))

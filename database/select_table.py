#!/usr/bin/python
# -*- coding: utf-8 -*- #
from database import Logger, db_codes, structure
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


def check_part(session, name, element):
    data = {
        'group': lambda group: dict(id_lesson_plan=[lp.id for lp in group.lesson_plans]),
        'teacher': lambda teach: dict(id_lesson_plan=[lp.id for lp in teach.lesson_plans]),
        'room': lambda room: dict(id_room=room.id)
    }

    part_data = data[name](element)
    lessons = Lessons.read(session, is_temp=[False, True], is_empty=False, **part_data)
    time_list = [lesson.row_time for lesson in lessons]
    duplicates = [time for time in set(time_list) if time_list.count(time) > 1]

    for time in duplicates:
        if hasattr(element, 'short_name'):
            logger.info('Problem with %s at %s' % (element.short_name, time))
        else:
            logger.info('Problem with %s at %s' % (element.name, time))

        # return db_codes[name]
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
        'group': groups,
        'teacher': teachers,
        'room': rooms,
    }

    # This is awful for now
    overlaying = []
    for key in elements.keys():
        for element in elements[key]:
            if hasattr(element, 'capacity') and element.capacity >= 256:
                continue
            res = check_part(session, key, element)
            if res != db_codes['success']:
                for time in res:
                    if not overlaying.count(time):
                        overlaying.append(time)
    if overlaying:
        return overlaying

    logger.info('Database is correct')
    return db_codes['success']


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


def check_table_after_swap(session, lesson1, lesson2):

    if isinstance(session, int):
        return db_codes['session']

    bad_lessons = []
    if not isinstance(lesson2, dict):
        lpidg2 = [lp.id for lp in LessonPlans.read(session, groups=[g.id for g in lesson2.lesson_plan.groups])]
        lpidt2 = [lp.id for lp in LessonPlans.read(session, teachers=[g.id for g in lesson2.lesson_plan.teachers])]
        lpidg2.remove(lesson2.lesson_plan.id) if lpidg2.count(lesson2.lesson_plan.id) else None
        lpidt2.remove(lesson2.lesson_plan.id) if lpidt2.count(lesson2.lesson_plan.id) else None
        if not isinstance(lesson1, dict):
            lpidt2.remove(lesson1.lesson_plan.id) if lpidt2.count(lesson1.lesson_plan.id) else None
            lpidg2.remove(lesson1.lesson_plan.id) if lpidg2.count(lesson1.lesson_plan.id) else None
        rl = Lessons.read(session, row_time=lesson2.row_time, is_temp=False, id_room=lesson2.id_room)
        for l in rl:
            if l.lesson_plan.id == lesson2.lesson_plan.id:
                rl.remove(l)
                break
            if not isinstance(lesson1, dict):
                if l.lesson_plan.id == lesson1.lesson_plan.id:
                    rl.remove(l)
                    break
        bad_lessons.append(rl)
        bad_lessons.append(Lessons.read(session, row_time=lesson2.row_time, is_temp=False,
                                        id_lesson_plan=lpidg2))
        bad_lessons.append(Lessons.read(session, row_time=lesson2.row_time, is_temp=False,
                                        id_lesson_plan=lpidt2))
    else:
        bad_lessons.append([])
        bad_lessons.append([])
        bad_lessons.append([])
    if not isinstance(lesson1, dict):
        lpidg1 = [lp.id for lp in LessonPlans.read(session, groups=[g.id for g in lesson1.lesson_plan.groups])]
        lpidt1 = [lp.id for lp in LessonPlans.read(session, teachers=[g.id for g in lesson1.lesson_plan.teachers])]
        lpidg1.remove(lesson1.lesson_plan.id) if lpidg1.count(lesson1.lesson_plan.id) else None
        lpidt1.remove(lesson1.lesson_plan.id) if lpidt1.count(lesson1.lesson_plan.id) else None
        if not isinstance(lesson2, dict):
            lpidt1.remove(lesson2.lesson_plan.id) if lpidt1.count(lesson2.lesson_plan.id) else None
            lpidg1.remove(lesson2.lesson_plan.id) if lpidg1.count(lesson2.lesson_plan.id) else None
        rl = Lessons.read(session, row_time=lesson1.row_time, is_temp=False, id_room=lesson1.id_room)
        for l in rl:
            if l.lesson_plan.id == lesson1.lesson_plan.id:
                rl.remove(l)
                break
            if not isinstance(lesson2, dict):
                if l.lesson_plan.id == lesson2.lesson_plan.id:
                    rl.remove(l)
                    break
        bad_lessons.append(rl)
        bad_lessons.append(Lessons.read(session, row_time=lesson1.row_time, is_temp=False,
                                        id_lesson_plan=lpidg1))
        bad_lessons.append(Lessons.read(session, row_time=lesson1.row_time, is_temp=False,
                                        id_lesson_plan=lpidt1))
    else:
        bad_lessons.append([])
        bad_lessons.append([])
        bad_lessons.append([])
    return bad_lessons


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

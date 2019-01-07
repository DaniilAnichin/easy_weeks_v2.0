#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from easy_weeks.database import Logger, db_codes, structure
from easy_weeks.database.structure import *
__all__ = ['get_table', 'check_table', 'save_table', 'recover_empty',
           'clear_empty', 'clear_temp', 'find_free', 'undefined_lp',
           'get_element', 'same_tables', 'find_duplicates']
logger = Logger()


def get_table(session, element):
    if isinstance(session, int):
        return db_codes['session']
    data_type = element.__tablename__
    logger.debug(f'Data: {element}')
    if data_type == 'rooms':
        params = {'id_room': element.id}
    else:
        lesson_plan_ids = [lp.id for lp in LessonPlans.read(session, **{data_type: element.id})]
        params = {'id_lesson_plan': lesson_plan_ids}

    empty = Lessons.read(session, id=1)[0]
    full = Lessons.read(session, **params)
    lessons_by_row_time = {lesson.row_time: lesson for lesson in full}
    rettable = [[[empty
                  for i in range(len(Lessons.time_ids))]
                 for j in range(len(Lessons.day_ids))]
                for k in range(len(Lessons.week_ids))]

    for i, week in enumerate(rettable):
        for j, day in enumerate(week):
            for k in range(len(day)):
                time = {
                    'id_lesson_time': k + 2,
                    'id_week_day': j + 2,
                    'id_week': i + 2,
                }
                row_time = Lessons.to_row(time)
                lesson = lessons_by_row_time.get(row_time, None)
                if lesson:
                    day[k] = lesson.make_temp(session)
                    Lessons.update(session, lesson.id, is_empty=True)
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


def check_part(session, element) -> tuple:
    data = {
        'Groups': lambda group: dict(id_lesson_plan=[lp.id for lp in group.lesson_plans]),
        'Teachers': lambda teach: dict(id_lesson_plan=[lp.id for lp in teach.lesson_plans]),
        'Rooms': lambda room: dict(id_room=room.id)
    }

    part_data = data[element.__class__.__name__](element)
    lessons = Lessons.read(session, is_temp=[False, True], is_empty=False, **part_data)
    time_list = [lesson.row_time for lesson in lessons]
    duplicates = [time for time in set(time_list) if time_list.count(time) > 1]

    if duplicates:
        if hasattr(element, 'short_name'):
            return duplicates, element.short_name
        else:
            return duplicates, element.name

    return db_codes['success'], db_codes['success']


def check_table(session, only_temp=False):
    if isinstance(session, int):
        return db_codes['session']

    # Can optimize by reading not the all groups/teachers/rooms
    if only_temp:
        lessons = Lessons.read(session, is_temp=True)
        groups = set(sum([lesson.lesson_plan.groups for lesson in lessons], []))
        teachers = set(sum([lesson.lesson_plan.groups for lesson in lessons], []))
        rooms = {lesson.room for lesson in lessons}
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
    overlaying = {}
    for key in elements.keys():
        for element in elements[key]:
            if hasattr(element, 'capacity') and element.capacity >= 256:
                continue
            res, elem = check_part(session, element)
            if res != db_codes['success']:
                if elem not in overlaying.keys():
                    overlaying[elem] = res
                else:
                    overlaying[elem] += res
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
                            old_session, name=[gro.name for gro in lesson.lesson_plan.groups]
                        )
                    ]
                )
            ]
        }
        by_groups = Lessons.read(old_session, **params)
        if by_groups and not isinstance(by_groups, int):
            if not lesson.lesson_plan.teachers[0].short_name == by_groups[0].lesson_plan.teachers[0].short_name:
                duplicates.append(lesson.row_time)
                continue
        params = {
            'row_time': lesson.row_time,
            'room': Rooms.read(old_session, name=lesson.room.name)[0]
        }
        by_rooms = Lessons.read(old_session, **params)
        if by_rooms:
            if not lesson.lesson_plan.teachers[0].short_name == by_rooms[0].lesson_plan.teachers[0].short_name:
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
            # logger.debug(f'Edited?: {db_codes_output[ret]}')
    return result


def clear_empty(session):
    if isinstance(session, int):
        return db_codes['session']

    lessons = Lessons.read(session, is_empty=True)
    # Skips the first empty lesson:
    for lesson in lessons[1:]:
        ret = Lessons.delete(session, main_id=lesson.id)
        # logger.debug(f'Deleted?: {db_codes_output[ret]}')
    return db_codes['success']


def clear_temp(session):
    if isinstance(session, int):
        return db_codes['session']

    lessons = Lessons.read(session, is_temp=True)
    for lesson in lessons:
        ret = Lessons.delete(session, main_id=lesson.id)
        # logger.debug(f'Deleted?: {db_codes_output[ret]}')


def recover_empty(session):
    if isinstance(session, int):
        return db_codes['session']

    lessons = Lessons.read(session, is_empty=True)
    for lesson in lessons[1:]:
        ret = Lessons.update(session, main_id=lesson.id, is_empty=False)
        # logger.debug(f'Restored?: {db_codes_output[ret]}')
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
    department = kwargs.pop('department', None)
    result = []
    if hasattr(cls, 'department'):
        classmates = cls.read(session, department=department)
    elif hasattr(cls, 'departments'):
        classmates = cls.read(session, departments=[department])
    else:
        return result

    for classmate in classmates:
        if is_free(session, cls, classmate.id, **kwargs):
            result.append(classmate)

    return result


def get_element(session, data_type, data_id):
    if isinstance(session, int):
        return db_codes['session']

    result = getattr(structure, data_type.capitalize()).read(session, id=data_id)

    if isinstance(result, list) and len(result) > 0:
        result = result[0]
    return result


def same_tables(first_session, second_session, teacher):
    first_table = Lessons.read(
        first_session,
        id_lesson_plan=[
            lp.id for lp in LessonPlans.read(
                first_session, teachers=[teacher.id]
            )
        ]
    )
    second_table = Lessons.read(
        second_session,
        id_lesson_plan=[
            lp.id for lp in LessonPlans.read(
                second_session, teachers=[Teachers.read(second_session, short_name=teacher.short_name)[0].id]
            )
        ]
    )
    first_table.sort(key=lambda a: a.row_time)
    second_table.sort(key=lambda a: a.row_time)
    for first, second in zip(first_table, second_table):
        empty = (first.is_empty, second.is_empty)
        if all(empty):
            continue
        if any(empty):
            return False
        if not first == second:
            return False
    return True


if __name__ == '__main__':
    from easy_weeks.database.start_db.db_startup import connect_database

    first_db = connect_database()
    second_db = connect_database('FICT_timetable2.db')

    logger.debug(same_tables(first_db, second_db, Teachers.read(first_db, id=20)[0]))

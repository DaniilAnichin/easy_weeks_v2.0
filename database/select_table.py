from database.structure.db_structure import *
from database import Logger, db_codes
logger = Logger()


def get_table(session, data_type, data):
    if isinstance(session, int):
        return db_codes['session']
    # check data_type and data
    logger.debug('Data type: "%s", data: "%s"' % (data_type, data))
    if data_type == 'rooms':
        params = dict(id_room=data)
    else:
        lesson_plan_ids = [lp.id for lp in LessonPlans.read(session, **{data_type: data})]
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
                if isinstance(lessons, int):
                    pass
                elif lessons:
                    rettable[week][day][time] = lessons[0]
                else:
                    rettable[week][day][time] = Lessons.read(session, id=1)[0]
    return rettable


def undefined_lp(session, data_type, data):
    if isinstance(session, int):
        return db_codes['session']
    # check data_type and data

    ret_vect = []
    lesson_plans = [lp.id for lp in LessonPlans.read(session, **{data_type: data})]
    for lp in lesson_plans:
        unsorted = lp.amount - len(Lessons.read(session, id_lesson_plan=lp.id))
        for i in range(unsorted):
            ret_vect.append(lp)
    return ret_vect


def check_table(session, only_temp=False):
    if isinstance(session, int):
        return db_codes['session']

    # Can optimize by reading not the all groups/teachers/rooms
    if only_temp:
        groups = Groups.read(session, lesson_plans=LessonPlans.read(
            session, lessons=Lessons.read(session, is_temp=True)
        ))
        teachers = Groups.read(session, lesson_plans=LessonPlans.read(
            session, lessons=Lessons.read(session, is_temp=True)
        ))
        rooms = Groups.read(session, lessons=Lessons.read(session, is_temp=True))
    else:
        groups = Groups.read(session, all_=True)
        teachers = Teachers.read(session, all_=True)
        rooms = Rooms.read(session, all_=True)

    states = [0, 1]
    for group in groups:
        lessons = Lessons.read(
            session, is_temp=states,
            id_lesson_plan=[lp.id for lp in group.lesson_plans]
        )
        time_list = [lesson.row_time for lesson in lessons]
        repeted = [time for time in set(time_list) if time_list.count(time) > 1]
        time_dict = {}

        for time in repeted:
            repeted_less = []
            for lesson in lessons:
                if lesson.row_time == time:
                    repeted_less.append(lesson)
            time_dict.update({time: repeted_less})
            if not ((len(time_dict[time]) == 2) and (time_dict[time][0] == time_dict[time][1])
                    and (time_dict[time][0].is_temp != time_dict[time][1].is_temp)):
                # do something
                logger.info('Problem with %s at %s' % (group.name, time))
                return db_codes['group']
    for teach in teachers:
        lessons = Lessons.read(
            session, is_temp=states,
            id_lesson_plan=[lp.id for lp in teach.lesson_plans]
        )
        time_list = [lesson.row_time for lesson in lessons]
        repeted = [time for time in set(time_list) if time_list.count(time) > 1]
        time_dict = {}
        for time in repeted:
            repeted_less = []
            for lesson in lessons:
                if lesson.row_time == time:
                    repeted_less.append(lesson)
            time_dict.update({time: repeted_less})
            if not (len(time_dict[time]) == 2 and time_dict[time][0] == time_dict[time][1]\
                    and time_dict[time][0].is_temp != time_dict[time][1].is_temp):
                # do something
                logger.info('Problem with %s at %s' % (teach.short_name, time))
                return db_codes['teacher']
    for room in rooms:
        if room.capacity >= 256:
            continue
        lessons = Lessons.read(session, is_temp=states, id_room=room.id)
        time_list = [lesson.row_time for lesson in lessons]
        repeted = [time for time in set(time_list) if time_list.count(time) > 1]
        for time in repeted:
            repeted_less = []
            for lesson in lessons:
                if lesson.row_time == time:
                    repeted_less.append(lesson)
            if not (len(repeted_less) == 2 and repeted_less[0] == repeted_less[1]
                    and repeted_less[0].is_temp != repeted_less[1].is_temp):
                # do something
                logger.info('Problem with %s at %s' % (room.shortname, time))
                return db_codes['room']
    logger.info('Database is correct')

    return db_codes['success']


def save_table(session):
    if isinstance(session, int):
        return db_codes['session']

    result = check_table(session)
    if result == db_codes['success']:
        for lesson in Lessons.read(session, all_=True, is_temp=True):
            lesson.update(session, lesson.id, is_tmp=False)
    return result


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
        try:
            departments = classmate.departments
        except AttributeError:
            departments = [classmate.department]

        if department in departments and is_free(session, cls, classmate.id, **kwargs):
            result.append(classmate)

    return result
from database import *
from structure import *

def get_table(session, data_type, data):
    if isinstance(session, int):
        return db_codes['session']
    # check data_type and data

    rettable = [[[None
                  for i in range(len(Lessons.time_ids))]
                  for j in range(len(Lessons.day_ids))]
                  for k in range(len(Lessons.week_ids))]
    if data_type == 'room':
        for w in Lessons.week_ids:
            for d in Lessons.day_ids:
                for t in Lessons.time_ids:
                    rettable[w - 2][d - 2][t - 2] = Lessons.read(session, id_room=data,
                                                                 id_week=w, id_week_day=d, id_lesson_time=t)
                    if rettable[w - 2][d - 2][t - 2]:
                        rettable[w - 2][d - 2][t - 2] = rettable[w - 2][d - 2][t - 2][0]
                    else:
                        rettable[w - 2][d - 2][t - 2] = Lessons.read(session, id=1)[0]
        return rettable

    else:
        id_lesson_plan = [lp.id for lp in LessonPlans.read(session, **{data_type: data})]

        for w in Lessons.week_ids:
            for d in Lessons.day_ids:
                for t in Lessons.time_ids:
                    rettable[w-2][d-2][t-2] = Lessons.read(session, id_lesson_plan=id_lesson_plan,
                                                     id_week=w, id_week_day=d, id_lesson_time=t)
                    if rettable[w-2][d-2][t-2]:
                        rettable[w - 2][d - 2][t - 2] = rettable[w-2][d-2][t-2][0]
                    else:
                        rettable[w - 2][d - 2][t - 2] = Lessons.read(session, id=1)[0]
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

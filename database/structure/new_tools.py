from sqlalchemy import or_, and_
from database.structure.select_tools import *
from database.structure.db_structure import *
__all__ = [
    'new_degree', 'new_department', 'new_faculty', 'new_group', 'new_lesson',
    'new_lesson_plan', 'new_room', 'new_subject', 'new_teacher',
    'new_university'
]


def new_university(s, full_name='', short_name=''):
    if full_name == '' and short_name == '':
        print "Must be one of the name"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    exists_un = s.query(Universities).filter(and_(Universities.short_name == short_name,
                                                  Universities.full_name == full_name)).first()
    if exists_un:
        print "This university %s, %s already exist with id %d" % (full_name, short_name, exists_un.id)

        return -3

    s.add(Universities(short_name=short_name,
                       full_name=full_name))
    s.commit()

    return 0


def new_faculty(s, full_name='', short_name='', id_un=1):
    if full_name == '' and short_name == '':
        print "Must be one of the name"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    exists_un = s.query(Universities).get(id_un)
    if not exists_un:
        print "Non such university with this id: %d" % id_un
        return -3

    exists_fa = s.query(Faculties).filter(and_(Faculties.short_name == short_name,
                                               Faculties.full_name == full_name,
                                               Faculties.id_university == id_un)).first()
    if exists_fa:
        print "This faculty %s, %s already exist in university %s with id %d" % (full_name, short_name,
                                                                                 exists_fa.universities.short_name,
                                                                                 exists_fa.id)

        return -4

    s.add(Faculties(short_name=short_name,
                    full_name=full_name,
                    id_university=id_un))
    s.commit()

    return 0


def new_department(s, full_name='', short_name='', id_fa=1):
    if full_name == '' and short_name == '':
        print "Must be one of the name"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    exists_fa = s.query(Faculties).get(id_fa)
    if not exists_fa:
        print "Non such faculty with this id: %d" % id_fa

        return -4

    exists_de = s.query(Departments).filter(and_(Departments.short_name == short_name,
                                                 Departments.full_name == full_name,
                                                 Departments.id_faculty == id_fa)).first()
    if exists_de:
        print "This department %s, %s already exist in faculty %s with id %d" % (full_name, short_name,
                                                                                 exists_de.faculties.short_name,
                                                                                 exists_de.id)

        return -5

    s.add(Departments(short_name=short_name,
                      full_name=full_name,
                      id_faculty=id_fa))
    s.commit()

    return 0


def new_group(s, name='', id_dp=1):
    if name == '':
        print "Name must be"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    exists_dp = s.query(Departments).get(id_dp)
    if not exists_dp:
        print "Non such department with this id: %d" % id_dp

        return -5

    exists_gr = s.query(Groups).filter(
        and_(Groups.name == name, Groups.id_department == id_dp)
    ).first()
    if exists_gr:
        print "This group %s already exist in department %s with id %d" % (name,
                                                                           exists_gr.department.short_name,
                                                                           exists_gr.id)

        return -7

    s.add(Groups(name=name, id_department=id_dp))
    s.commit()

    return 0


def new_degree(s, full_name='', short_name=''):
    if full_name == '' and short_name == '':
        print "Must be one of the name"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    exists_de = s.query(Degrees).filter(or_(Degrees.short_name == short_name,
                                            Degrees.full_name == full_name)).first()
    if exists_de:
        print "This degree already exist id %d" % exists_de.id

        return -8

    s.add(Degrees(short_name=short_name,
                  full_name=full_name))
    s.commit()

    return 0


def new_teacher(s, full_name='', short_name='', id_dep=1, id_deg=1):
    if full_name == '' and short_name == '':
        print "Must be one of the name"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    exists_deg = s.query(Degrees).get(id_deg)
    if not exists_deg:
        print "No degree with this id %d" % id_deg

        return -8

    exists_dep = s.query(Departments).get(id_dep)
    if not exists_dep:
        print "No department with this id %d" % id_dep

        return -5

    exists_te = s.query(Teachers).filter(and_(Teachers.short_name == short_name,
                                              Teachers.full_name == full_name,
                                              Teachers.id_department == id_dep,
                                              Teachers.id_degree == id_deg)).first()
    if exists_te:
        print "Teacher %s %s (%s) from %s is already exists with id %d" % (exists_te.degree.short_name,
                                                                           exists_te.full_name,
                                                                           exists_te.short_name,
                                                                           exists_te.department.short_name,
                                                                           exists_te.id)

        return -9

    s.add(Teachers(short_name=short_name,
                   full_name=full_name,
                   id_department=id_dep,
                   id_degree=id_deg))
    s.commit()

    return 0


def new_room(s, name='', cap=32, stuff='', id_des=[1]):
    if name == '':
        print "Name must be"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    for id_de in id_des:
        exist_de = s.query(Departments).get(id_de)
        if not exist_de:
            print "No such department with id %d" % id_de
            return -5

    exist_ro = s.query(Rooms).filter(Rooms.name == name).first()
    if exist_ro:
        print "Room %s already exists in department %s with id %d" % (exist_ro.name,
                                                                      exist_ro.departments[0].short_name,
                                                                      exist_ro.id)

        return -10

    new_r = Rooms(name=name, capacity=cap, additional_stuff=stuff)
    for id_d in id_des:
        d = s.query(Departments).get(id_d)
        new_r.departments.append(d)
    s.add(new_r)
    s.commit()

    return 0


def new_subject(s, short_name='', full_name=''):
    if full_name == '' and short_name == '':
        print "Must be one of the name"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    exists_sub = s.query(Subjects).filter(and_(Subjects.short_name == short_name,
                                               Subjects.full_name == full_name)).first()
    if exists_sub:
        print "This subject %s, %s already exist with id %d" % (full_name, short_name, exists_sub.id)

        return -11

    s.add(Subjects(short_name=short_name,
                   full_name=full_name))
    s.commit()

    return 0


def new_lesson_plan(s, id_sub=0, id_les_type=1, id_grps=[], id_tes=[1],
                    times_for_2_week=0, split_groups=0, capacity=32, needed_stuff=''):
    if times_for_2_week < 1:
        print "Not selected number of lesson"
        return -12
    if not id_grps:
        print "No group selected"
        return -5
    if type(s) is int:
        print "No session"
        return -2

    exist_sub = s.query(Subjects).get(id_sub)
    if not exist_sub:
        print "Non such subject with id %d" % id_sub

        return -11
    for id_gr in id_grps:
        exist_gr = s.query(Groups).get(id_gr)
        if not exist_gr:
            print "Non such group with id %d" % id_gr

            return -7
    for id_te in id_tes:
        exist_te = s.query(Teachers).get(id_te)
        if not exist_te:
            print "Non such teacher with id %d" % id_te

            return -9

    id_grps.sort()
    id_tes.sort()
    groups_checker = ''
    for id_gr in id_grps:
        groups_checker += str(id_gr) + ','
    teacher_checker = ''
    for id_te in id_tes:
        teacher_checker += str(id_te) + ','

    param_checker = "%d,%d,%s%s%d,%d,%d" % (id_sub, id_les_type, groups_checker, teacher_checker,
                                            times_for_2_week, split_groups, capacity)

    exist_lp = s.query(LessonPlans).filter(LessonPlans.param_checker == param_checker).first()
    if exist_lp:
        print "Lesson plan with this parameters already exist"

        return -13

    new_lesson_plan = LessonPlans(id_subject=id_sub,
                                  id_lesson_type=id_les_type,
                                  amount=times_for_2_week,
                                  needed_stuff=needed_stuff,
                                  capacity=capacity,
                                  split_groups=split_groups,
                                  param_checker=param_checker)
    for id_te in id_tes:
        exist_te = s.query(Teachers).get(id_te)
        new_lesson_plan.teachers.append(exist_te)
    for id_gr in id_grps:
        exist_gr = s.query(Groups).get(id_gr)
        new_lesson_plan.groups.append(exist_gr)

    s.add(new_lesson_plan)
    s.commit()

    return 0


def new_lesson(s, id_lp, id_room, row_time):
    if not id_lp:
        print "No lesson_plan selected"
        return -13
    if not id_room:
        print "No room selected"
        return -10
    # if not row_time:
    #     print "No time selected"
    #     return -14
    if row_time < 0 or row_time > 60:
        print "Invalid time"
        return -14
    if type(s) is int:
        print "No session"
        return -2

    exist_lp = s.query(LessonPlans).get(id_lp)
    if not exist_lp:
        print "No such lesson_plan with id %d" % id_lp

        return -13
    exist_rm = s.query(Rooms).get(id_room)
    if not exist_rm:
        print "No such room with id %d" % id_room

        return -10

    exist_ls = s.query(Lessons).filter(Lessons.id_lesson_plan == id_lp).all()
    if len(exist_ls) >= exist_lp.amount:
        print "Can't add new lesson (all lessons already handled) delete some to add new"
        return -15
    for g in s.query(LessonPlans).get(id_lp).groups:
        for lessons in select_lessons(s, id_lesson_plan=[i['id'] for i in
                                                         select_lesson_plans(s, groups=[g.id])]):
            if lessons['row_time'] == row_time:
                print "Invalid time"
                return -14
    for t in s.query(LessonPlans).get(id_lp).teachers:
        for lessons in select_lessons(s, id_lesson_plan=[i['id'] for i in
                                                         select_lesson_plans(s, teachers=[t.id])]):
            if lessons['row_time'] == row_time:
                print "Invalid time"
                return -14

    for l in exist_ls:
        if l.row_time == row_time:
            print "Invalid time"

            return -14
    if id_room != 1:
        for room_checker in s.query(Lessons).filter(Lessons.row_time == row_time).all():
            if room_checker.id_room == id_room:
                print "This room is busy at this time"
                return -16
    if exist_lp.capacity > s.query(Rooms).get(id_room).capacity:
        print "Too small room for this lesson"
        return -10
    if exist_lp.needed_stuff != exist_rm.additional_stuff or exist_lp.needed_stuff != '':
        print "No such stuff"
        return -15

    s.add(Lessons(id_lesson_plan=id_lp,
                  id_room=id_room,
                  row_time=row_time,
                  id_week=int(row_time / 30) + 1,
                  id_week_day=int(row_time % 30 / 6) + 1,
                  id_lesson_time=int(row_time % 5) + 1
                  ))
    s.commit()

    return 0

from sqlalchemy import and_
from database.structure.select_tools import *
from database import db_codes


def update_university(s, id_u=1, full_name='', short_name=''):
    if id_u == 1 or not (full_name or short_name):
        return db_codes['params']
    if type(s) is int:
        return db_codes['session']

    if not s.query(Universities).get(id_u):
        return db_codes['university']

    exists_un = s.query(Universities).filter(
        and_(Universities.short_name == short_name,
             Universities.full_name == full_name)).first()
    if exists_un:
        return db_codes['university']

    u = s.query(Universities).get(id_u)
    u.short_name = short_name
    u.full_name = full_name
    s.commit()

    return db_codes['success']


def update_faculty(s, id_f=1, id_u=1, full_name='', short_name=''):
    if not (full_name or short_name or id_u) or id_f == 1:
        return db_codes['params']
    if type(s) is int:
        return db_codes['session']

    if not s.query(Faculties).get(id_f):
        return db_codes['faculty']
    if not s.query(Universities).get(id_u):
        return db_codes['university']

    exists_f = s.query(Faculties).filter(and_(
        Faculties.short_name == short_name,
        Faculties.full_name == full_name,
        Faculties.id_university == id_u)).first()
    if exists_f:
        return db_codes['faculty']

    f = s.query(Faculties).get(id_f)
    f.short_name = short_name
    f.full_name = full_name
    f.id_university = id_u
    s.commit()

    return db_codes['success']


def update_department(s, id_d=1, id_f=1, full_name='', short_name=''):
    if not(full_name or short_name or id_f) or id_d == 1:
        return db_codes['params']
    if type(s) is int:
        return db_codes['session']

    if not s.query(Departments).get(id_d):
        return db_codes['department']
    if not s.query(Faculties).get(id_f):
        return db_codes['faculty']

    exists_d = s.query(Departments).filter(and_(
        Departments.short_name == short_name,
        Departments.full_name == full_name,
        Departments.id_faculty == id_f)
    ).first()

    if exists_d:
        return db_codes['department']

    d = s.query(Departments).get(id_d)
    d.short_name = short_name
    d.full_name = full_name
    d.id_faculty = id_f
    s.commit()

    return db_codes['success']


def update_group(s, id_g=0, id_d=1, name=''):
    if not name or id_g == 0:
        return db_codes['params']
    if type(s) is int:
        return db_codes['session']

    if not s.query(Groups).get(id_g):
        return db_codes['group']
    if not s.query(Departments).get(id_d):
        return db_codes['department']

    exists_g = s.query(Groups).filter(and_(
        Groups.name == name, Groups.id_department == id_d)
    ).first()

    if exists_g:
        return db_codes['group']

    g = s.query(Groups).get(id_g)
    g.name = name
    g.id_department = id_d
    s.commit()

    return db_codes['success']


def update_degree(s, id_d=1, full_name='', short_name=''):
    if not (full_name or short_name) or id_d == 1:
        return db_codes['params']
    if type(s) is int:
        return db_codes['session']

    if not s.query(Degrees).get(id_d):
        return db_codes['degree']

    exists_de = s.query(Degrees).filter(or_(
        Degrees.short_name == short_name, Degrees.full_name == full_name)
    ).first()

    if exists_de:
        return db_codes['degree']

    d = s.query(Degrees).get(id_d)
    d.short_name = short_name
    d.full_name = full_name
    s.commit()

    return db_codes['success']


def update_teacher(s, id_t=1, full_name='', short_name='', id_dep=1, id_deg=1):
    if not (full_name or short_name or id_dep != 1 or id_deg != 1) or id_t == 1:
        return db_codes['params']
    if type(s) is int:
        return db_codes['session']

    if not s.query(Teachers).get(id_t):
        return db_codes['teacher']
    if not s.query(Degrees).get(id_deg):
        return db_codes['degree']
    if not s.query(Departments).get(id_dep):
        return db_codes['department']

    exists_te = s.query(Teachers).filter(and_(
        Teachers.short_name == short_name,
        Teachers.full_name == full_name,
        Teachers.id_department == id_dep,
        Teachers.id_degree == id_deg)
    ).first()

    if exists_te:
        return db_codes['teacher']

    t = s.query(Teachers).get(id_t)
    t.short_name = short_name
    t.full_name = full_name
    t.id_department = id_dep
    t.id_degree = id_deg
    s.commit()

    return db_codes['success']


def update_room(s, id_r=1, name='', cap=32, stuff='', id_des=[1]):
    if not name or id_r == 1:
        return db_codes['params']
    if type(s) is int:
        return db_codes['session']

    for id_de in id_des:
        exist_de = s.query(Departments).get(id_de)
        if not exist_de:
            return db_codes['department']

    exist_ro = s.query(Rooms).filter(Rooms.name == name).first()
    if exist_ro:
        return db_codes['room']

    for check_cap in select_lessons(s, id_room=id_r):
        if check_cap['lesson_plan'][0]['capacity'] > cap:
            return db_codes['room']

    r = s.query(Rooms).get(id_r)
    r.name = name
    r.capacity = cap
    r.additional_stuff = stuff
    for d in r.departments:
        r.departments.remove(d)
    for id_de in id_des:
        d = s.query(Departments).get(id_de)
        r.departments.append(d)
    s.commit()

    return db_codes['success']


def update_subject(s, id_s=0, short_name='', full_name=''):
    if not (full_name or short_name) or id_s == 0:
        return db_codes['params']
    if type(s) is int:
        return db_codes['session']

    if not s.query(Subjects).get(id_s):
        return db_codes['subject']
    exists_sub = s.query(Subjects).filter(and_(
        Subjects.short_name == short_name, Subjects.full_name == full_name)
    ).first()
    if exists_sub:
        return db_codes['subject']

    sub = s.query(Subjects).get(id_s)
    sub.short_name = short_name
    sub.full_name = full_name
    s.commit()
    return db_codes['success']


def update_lesson_plan(s, id_lp=0, id_sub=0, id_les_type=1, id_grps=[],
                       id_tes=[1],  times_for_2_week=0, split_groups=0,
                       capacity=32, needed_stuff=''):
    if id_lp == 0:
        print 'No lesson plan selected'
        return db_codes['']13
    if times_for_2_week < 1:
        print "Not selected number of lesson"
        return db_codes['']12
    if not id_grps:
        print "No group selected"
        return db_codes['']5
    if type(s) is int:
        print "No session"
        return db_codes['']2

    exist_sub = s.query(Subjects).get(id_sub)
    if not exist_sub:
        print "Non such subject with id %d" % id_sub
        return db_codes['']11
    for id_gr in id_grps:
        exist_gr = s.query(Groups).get(id_gr)
        if not exist_gr:
            print "Non such group with id %d" % id_gr
            return db_codes['']7
    for id_te in id_tes:
        exist_te = s.query(Teachers).get(id_te)
        if not exist_te:
            print "Non such teacher with id %d" % id_te
            return db_codes['']9

    id_grps.sort()
    id_tes.sort()
    groups_checker = ''
    for id_gr in id_grps:
        groups_checker += str(id_gr) + ','
    teacher_checker = ''
    for id_te in id_tes:
        teacher_checker += str(id_te) + ','

    param_checker = "%d,%d,%s%s%d,%d,%d" % (
        id_sub, id_les_type, groups_checker, teacher_checker,
        times_for_2_week, split_groups, capacity)

    exist_lp = s.query(Lesson_plan).filter(
        Lesson_plan.param_checker == param_checker).first()
    if exist_lp:
        print "Lesson plan with this parameters already exist"
        return db_codes['']13

    lp = s.query(Lesson_plan).get(id_lp)
    for l in s.query(Lessons).filter(Lessons.id_lesson_plan == id_lp).all():
        if lp.capacity > l.rooms.capacity:
            print "Impossible to change lesson_plan. Problems with capacity"
            return db_codes['']17
        if lp.additional_stuff != l.rooms.additional_stuff or lp.additional_stuff != '':
            print "Impossible to change lesson_plan. Problem with stuff"
            return db_codes['']17
    lp.id_subject = id_sub
    id_lp.id_lesson_type = id_les_type
    id_lp.times_for_2_week = times_for_2_week
    id_lp.needed_stuff = needed_stuff
    id_lp.capacity = capacity
    id_lp.split_groups = split_groups
    id_lp.param_checker = param_checker
    for t in lp.teachers:
        lp.teachers.remove(t)
    for g in lp.groups:
        lp.groups.remove(g)
    for id_te in id_tes:
        exist_te = s.query(Teachers).get(id_te)
        lp.teachers.append(exist_te)
    for id_gr in id_grps:
        exist_gr = s.query(Groups).get(id_gr)
        lp.groups.append(exist_gr)

    s.commit()

    return db_codes['success']


def update_lesson(s, id_l, id_lp, id_room, row_time):
    if not id_lp:
        print "No lesson_plan selected"
        return db_codes['']13
    if not id_room:
        print "No room selected"
        return db_codes['']10
    # if not row_time:
    #     print "No time selected"
    #     return db_codes['']14
    if row_time < 0 or row_time > 60:
        print "Invalid time"
        return db_codes['']14
    if type(s) is int:
        print "No session"
        return db_codes['']2

    if not s.query(Lessons).get(id_l):
        print "no Such lesson with id %d" % id_l
        return db_codes['']13

    exist_lp = s.query(Lesson_plan).get(id_lp)
    if not exist_lp:
        print "No such lesson_plan with id %d" % id_lp

        return db_codes['']13
    exist_rm = s.query(Rooms).get(id_room)
    if not exist_rm:
        print "No such room with id %d" % id_room

        return db_codes['']10

    exist_ls = s.query(Lessons).filter(Lessons.id_lesson_plan == id_lp).all()
    for g in s.query(Lesson_plan).get(id_lp).groups:
        for lessons in select_lessons(s, id_lesson_plan=[
            i['id'] for i in select_lesson_plans(s, groups=[g.id])
        ]):
            if lessons['row_time'] == row_time:
                print "Invalid time"
                return db_codes['']14
    for t in s.query(Lesson_plan).get(id_lp).teachers:
        for lessons in select_lessons(s, id_lesson_plan=[
            i['id'] for i in select_lesson_plans(s, teachers=[t.id])
        ]):
            if lessons['row_time'] == row_time:
                print "Invalid time"
                return db_codes['']14

    for l in exist_ls:
        if l.row_time == row_time:
            print "Invalid time"
            return db_codes['']14

    if id_room != 1:
        for room_checker in s.query(Lessons).filter(
                        Lessons.row_time == row_time).all():
            if room_checker.id_room == id_room:
                "This room is busy at this time"
        return db_codes['']16
    if exist_lp.capacity > s.query(Rooms).get(id_room).capacity:
        print "Too small room for this lesson"
        return db_codes['']10
    if exist_lp.needed_stuff != exist_rm.additional_stuff or exist_lp.needed_stuff != '':
        print "No such stuff"
        return db_codes['']15

    l = s.query(Lessons).get(id_l)
    l.id_lesson_plan = id_lp
    l.id_room = id_room
    l.row_time = row_time
    if row_time < 60:
        l.id_week = int(row_time / 30) + 1
        l.id_week_day = int(row_time % 30 / 6) + 1
        l.id_lesson_time = int(row_time % 5) + 1
    else:
        l.id_week = 1
        l.id_week_day = 1
        l.id_lesson_time = 1
    s.commit()
    return db_codes['success']


def update_tmp_lesson(s, id_l, id_lp, id_room, row_time):
    if not id_lp:
        print "No lesson_plan selected"
        return db_codes['']13
    if not id_room:
        print "No room selected"
        return db_codes['']10
    # if not row_time:
    #     print "No time selected"
    #     return db_codes['']14
    if row_time < 0 or row_time > 59:
        print "Invalid time"
        return db_codes['']14
    if type(s) is int:
        print "No session"
        return db_codes['']2

    if not s.query(Tmp_lessons).get(id_l):
        print "no Such lesson with id %d" % id_l
        return db_codes['']13

    exist_lp = s.query(Lesson_plan).get(id_lp)
    if not exist_lp:
        print "No such lesson_plan with id %d" % id_lp

        return db_codes['']13
    exist_rm = s.query(Rooms).get(id_room)
    if not exist_rm:
        print "No such room with id %d" % id_room

        return db_codes['']10

    exist_ls = s.query(Tmp_lessons).filter(
        Tmp_lessons.id_lesson_plan == id_lp).all()
    for g in s.query(Lesson_plan).get(id_lp).groups:
        for lessons in select_lessons(s, id_lesson_plan=[
            i['id'] for i in select_lesson_plans(s, groups=[g.id])
        ]):
            if lessons['row_time'] == row_time:
                print "Invalid time"
                return db_codes['']14
    for t in s.query(Lesson_plan).get(id_lp).teachers:
        for lessons in select_lessons(s, id_lesson_plan=[
            i['id'] for i in select_lesson_plans(s, teachers=[t.id])
        ]):
            if lessons['row_time'] == row_time:
                print "Invalid time"
                return db_codes['']14

    for l in exist_ls:
        if l.row_time == row_time:
            print "Invalid time"
            return db_codes['']14

    if id_room != 1:
        for room_checker in s.query(Tmp_lessons).filter(
                        Tmp_lessons.row_time == row_time).all():
            if room_checker.id_room == id_room:
                "This room is busy at this time"
        return db_codes['']16
    if exist_lp.capacity > s.query(Rooms).get(id_room).capacity:
        print "Too small room for this lesson"
        return db_codes['']10
    if exist_lp.needed_stuff != exist_rm.additional_stuff or exist_lp.needed_stuff != '':
        print "No such stuff"
        return db_codes['']15

    l = s.query(Tmp_lessons).get(id_l)
    l.id_lesson_plan = id_lp
    l.id_room = id_room
    l.row_time = row_time
    l.id_week = int(row_time / 30) + 1
    l.id_week_day = int(row_time % 30 / 6) + 1
    l.id_lesson_time = int(row_time % 5) + 1
    s.commit()
    return db_codes['success']


def swap_two_lessons(s, id_l1, id_l2):
    if type(s) is int:
        print "No session"
        return db_codes['']2
    if len(select_lessons(s, [id_l1, id_l2])) != 2:
        print "invalid id_lessons %d %d" % (id_l1, id_l2)
        return db_codes['']11
    ldict = select_lessons(s, [id_l1, id_l2])

    update_lesson(s, id_l1, ldict[0]['id_lesson_plan'][0]['id'],
                  ldict[0]['id_room'], 60)
    update_lesson(s, id_l2, ldict[1]['id_lesson_plan'][0]['id'],
                  ldict[1]['id_room'], ldict[0]['row_time'])
    update_lesson(s, id_l1, ldict[0]['id_lesson_plan'][0]['id'],
                  ldict[0]['id_room'], ldict[1]['row_time'])
    return db_codes['success']

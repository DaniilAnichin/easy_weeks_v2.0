from .. import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_


def update_university(s, id_u=1, full_name='', short_name=''):
    if full_name == '' and short_name == '' and id_u == 1:
        print "Must be one of the name or invalid id"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Universities).get(id_u):
        print "No such university"
        return -3
    exists_un = s.query(Universities).filter(and_(Universities.short_name == short_name,
                                                  Universities.full_name == full_name)).first()
    if exists_un:
        print "This university %s, %s already exist with id %d" % (full_name, short_name, exists_un.id)
        return -3

    u = s.query(Universities).get(id_u)
    u.short_name=short_name
    u.full_name=full_name
    s.commit()

    return 0


def update_faculty(s, id_f=1, id_u=1, full_name='', short_name=''):
    if full_name == '' and short_name == '' and id_f == 1:
        print "Must be one of the name or invalid id"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Faculties).get(id_f):
        print "No such faculty"
        return -4
    if not s.query(Universities).get(id_u):
        print "No such university with id %d to refer" % id_u
        return -3

    exists_f = s.query(Faculties).filter(and_(Faculties.short_name == short_name,
                                              Faculties.full_name == full_name,
                                              Faculties.id_university == id_u)).first()
    if exists_f:
        print "This faculty %s, %s already exist in university %s with id %d" % (full_name, short_name,
                                                                                 exists_f.universities.short_name,
                                                                                 exists_f.id)
        return -4

    f = s.query(Faculties).get(id_f)
    f.short_name = short_name
    f.full_name = full_name
    f.id_university = id_u
    s.commit()

    return 0


def update_department(s, id_d=1, id_f=1, full_name='', short_name=''):
    if full_name == '' and short_name == '' and id_d == 1:
        print "Must be one of the name or invalid id"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Departments).get(id_d):
        print "No such department"
        return -5
    if not s.query(Faculties).get(id_f):
        print "No such faculty with id %d to refer" % id_f
        return -4

    exists_d = s.query(Departments).filter(and_(Departments.short_name == short_name,
                                                Departments.full_name == full_name,
                                                Departments.id_faculty == id_f)).first()
    if exists_d:
        print "This department %s, %s already exist in faculty %s with id %d" % (full_name, short_name,
                                                                                 exists_d.faculty.short_name,
                                                                                 exists_d.id)
        return -5

    d = s.query(Departments).get(id_d)
    d.short_name = short_name
    d.full_name = full_name
    d.id_faculty = id_f
    s.commit()

    return 0


def update_group(s, id_g=0, id_d=1, name=''):
    if name == '' and id_g == 0:
        print "Must be one of the name or invalid id"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Groups).get(id_g):
        print "No such group"
        return -7
    if not s.query(Departments).get(id_d):
        print "No such department with id %d to refer" % id_d
        return -5

    exists_g = s.query(Groups).filter(and_(Groups.name == name,
                                           Groups.id_department == id_d)).first()
    if exists_g:
        print "This group %s already exist in department %s with id %d" % (name, exists_g.department.short_name,
                                                                           exists_g.id)
        return -7

    g = s.query(Groups).get(id_g)
    g.name = name
    g.id_department = id_d
    s.commit()

    return 0


def update_degree(s, id_d=1, full_name='', short_name=''):
    if full_name == '' and short_name == '' and id_d == 1:
        print "Must be one of the name"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Degrees).get(id_d):
        print "No degree with this id %d" % id_d
    exists_de = s.query(Degrees).filter(or_(Degrees.short_name == short_name,
                                            Degrees.full_name == full_name)).first()
    if exists_de:
        print "This degree already exist id %d" % exists_de.id

        return -8

    d = s.query(Degrees).get(id_d)
    d.short_name = short_name
    d.full_name = full_name
    s.commit()

    return 0


def update_teacher(s, id_t, full_name='', short_name='', id_dep=1, id_deg=1):
    if full_name == '' and short_name == '' and id_t:
        print "Must be one of the name"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Teachers).get(id_t):
        print "No teacher with this id %d" % id_t
        return -9
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
        print "Teacher %s %s (%s) from %s is already exists with id %d" % (exists_te.degrees.short_name,
                                                                           exists_te.full_name,
                                                                           exists_te.short_name,
                                                                           exists_te.departments.short_name,
                                                                           exists_te.id)

        return -9
    t = s.query(Teachers).get(id_t)
    t.short_name = short_name
    t.full_name = full_name
    t.id_department = id_dep
    t.id_degree = id_deg
    s.commit()

    return 0


def update_room(s, id_r=1,  name='', cap=32, stuff='', id_des=[1]):
    if name == '' and id_r == 1:
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
                                                                      exist_ro.departments.short_name,
                                                                      exist_ro.id)
        return -10

    for check_cap in select_lessons(s, id_room=id_r):
        if check_cap['lesson_plan'][0]['capacity'] > cap:
            print "Impossible to change room capacity"
            return -10
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

    return 0


def update_subject(s, id_s=0, short_name='', full_name=''):
    if full_name == '' and short_name == '' and id_s == 0:
        print "Must be one of the name"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Subjects).get(id_s):
        print "No such subject with id %d" % id_s
        return -11
    exists_sub = s.query(Subjects).filter(and_(Subjects.short_name == short_name,
                                               Subjects.full_name == full_name)).first()
    if exists_sub:
        print "This subject %s, %s already exist with id %d" % (full_name, short_name, exists_sub.id)
        return -11

    sub = s.query(Subjects).get(id_s)
    sub.short_name = short_name
    sub.full_name = full_name
    s.commit()
    return 0


def update_lesson_plan(s, id_lp=0, id_sub=0, id_les_type=1, id_grps=[], id_tes=[1],
                       times_for_2_week=0, split_groups=0, capacity=32, needed_stuff=''):

    if id_lp == 0:
        print 'No lesson plan selected'
        return -13
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

    exist_lp = s.query(Lesson_plan).filter(Lesson_plan.param_checker == param_checker).first()
    if exist_lp:
        print "Lesson plan with this parameters already exist"
        return -13

    lp = s.query(Lesson_plan).get(id_lp)
    for l in s.query(Lessons).filter(Lessons.id_lesson_plan == id_lp).all():
        if lp.capacity > l.rooms.capacity:
            print "Impossible to change lesson_plan. Problems with capacity"
            return -17
        if lp.additional_stuff != l.rooms.additional_stuff or lp.additional_stuff != '':
            print "Impossible to change lesson_plan. Problem with stuff"
            return -17
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

    return 0


def update_lesson(s, id_l, id_lp, id_room, row_time):
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

    if not s.query(Lessons).get(id_l):
        print "no Such lesson with id %d" % id_l
        return -13

    exist_lp = s.query(Lesson_plan).get(id_lp)
    if not exist_lp:
        print "No such lesson_plan with id %d" % id_lp

        return -13
    exist_rm = s.query(Rooms).get(id_room)
    if not exist_rm:
        print "No such room with id %d" % id_room

        return -10

    exist_ls = s.query(Lessons).filter(Lessons.id_lesson_plan == id_lp).all()
    for g in s.query(Lesson_plan).get(id_lp).groups:
        for lessons in select_lessons(s, id_lesson_plan=[i['id'] for i in
                                                         select_lesson_plans(s, groups=[g.id])]):
            if lessons['row_time'] == row_time:
                print "Invalid time"
                return -14
    for t in s.query(Lesson_plan).get(id_lp).teachers:
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
                "This room is busy at this time"
        return -16
    if exist_lp.capacity > s.query(Rooms).get(id_room).capacity:
        print "Too small room for this lesson"
        return -10
    if exist_lp.needed_stuff != exist_rm.additional_stuff or exist_lp.needed_stuff != '':
        print "No such stuff"
        return -15

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
    return 0


def update_tmp_lesson(s, id_l, id_lp, id_room, row_time):
    if not id_lp:
        print "No lesson_plan selected"
        return -13
    if not id_room:
        print "No room selected"
        return -10
    # if not row_time:
    #     print "No time selected"
    #     return -14
    if row_time < 0 or row_time > 59:
        print "Invalid time"
        return -14
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Tmp_lessons).get(id_l):
        print "no Such lesson with id %d" % id_l
        return -13

    exist_lp = s.query(Lesson_plan).get(id_lp)
    if not exist_lp:
        print "No such lesson_plan with id %d" % id_lp

        return -13
    exist_rm = s.query(Rooms).get(id_room)
    if not exist_rm:
        print "No such room with id %d" % id_room

        return -10

    exist_ls = s.query(Tmp_lessons).filter(Tmp_lessons.id_lesson_plan == id_lp).all()
    for g in s.query(Lesson_plan).get(id_lp).groups:
        for lessons in select_lessons(s, id_lesson_plan=[i['id'] for i in
                                                         select_lesson_plans(s, groups=[g.id])]):
            if lessons['row_time'] == row_time:
                print "Invalid time"
                return -14
    for t in s.query(Lesson_plan).get(id_lp).teachers:
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
        for room_checker in s.query(Tmp_lessons).filter(Tmp_lessons.row_time == row_time).all():
            if room_checker.id_room == id_room:
                "This room is busy at this time"
        return -16
    if exist_lp.capacity > s.query(Rooms).get(id_room).capacity:
        print "Too small room for this lesson"
        return -10
    if exist_lp.needed_stuff != exist_rm.additional_stuff or exist_lp.needed_stuff != '':
        print "No such stuff"
        return -15

    l = s.query(Tmp_lessons).get(id_l)
    l.id_lesson_plan = id_lp
    l.id_room = id_room
    l.row_time = row_time
    l.id_week = int(row_time / 30) + 1
    l.id_week_day = int(row_time % 30 / 6) + 1
    l.id_lesson_time = int(row_time % 5) + 1
    s.commit()
    return 0


def swap_two_lessons(s, id_l1, id_l2):
    if type(s) is int:
        print "No session"
        return -2
    if len(select_lessons(s, [id_l1, id_l2])) != 2:
        print "invalid id_lessons %d %d" % (id_l1, id_l2)
        return -11
    ldict = select_lessons(s, [id_l1, id_l2])
    update_lesson(s, id_l1, ldict[0]['id_lesson_plan'][0]['id'], ldict[0]['id_room'], 60)
    update_lesson(s, id_l2, ldict[1]['id_lesson_plan'][0]['id'], ldict[1]['id_room'], ldict[0]['row_time'])
    update_lesson(s, id_l1, ldict[0]['id_lesson_plan'][0]['id'], ldict[0]['id_room'], ldict[1]['row_time'])
    return 0

from database.structure.db_structure import *
__all__ = [
    'delete_degree', 'delete_department', 'delete_faculty', 'delete_group',
    'delete_lesson', 'delete_lesson_plan', 'delete_room', 'delete_subject',
    'delete_teacher', 'delete_tmp_lesson', 'delete_university'
]


def delete_university(s, id_u):
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Universities).get(id_u):
        print "No such university"
        return -3
    u = s.query(Universities).get(id_u)
    s.delete(u)
    s.commit()
    return 0


def delete_faculty(s, id_f):
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Faculties).get(id_f):
        print "No such faculty"
        return -3
    f = s.query(Faculties).get(id_f)
    s.delete(f)
    s.commit()
    return 0


def delete_department(s, id_d):
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Departments).get(id_d):
        print "No such department"
        return -3
    d = s.query(Departments).get(id_d)
    s.delete(d)
    s.commit()
    return 0


def delete_group(s, id_g):
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Groups).get(id_g):
        print "No such group"
        return -3
    g = s.query(Groups).get(id_g)
    s.delete(g)
    s.commit()
    return 0


def delete_degree(s, id_d):
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Degrees).get(id_d):
        print "No such degree"
        return -3
    d = s.query(Degrees).get(id_d)
    s.delete(d)
    s.commit()
    return 0


def delete_teacher(s, id_t):
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Teachers).get(id_t):
        print "No such teacher"
        return -3
    t = s.query(Teachers).get(id_t)
    s.delete(t)
    s.commit()
    return 0


def delete_room(s, id_r):
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Rooms).get(id_r):
        print "No such room"
        return -3
    r = s.query(Rooms).get(id_r)
    s.delete(r)
    s.commit()
    return 0


def delete_subject(s, id_s):
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Subjects).get(id_s):
        print "No such subject"
        return -3
    sub = s.query(Subjects).get(id_s)
    s.delete(sub)
    s.commit()
    return 0


def delete_lesson_plan(s, id_lp):
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Lesson_plan).get(id_lp):
        print "No such lesson plan"
        return -3
    lp = s.query(Lesson_plan).get(id_lp)
    s.delete(lp)
    s.commit()
    return 0


def delete_lesson(s, id_l):
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Lessons).get(id_l):
        print "No such lesson"
        return -3
    l = s.query(Lessons).get(id_l)
    s.delete(l)
    s.commit()
    return 0


def delete_tmp_lesson(s, id_tl):
    if type(s) is int:
        print "No session"
        return -2

    if not s.query(Tmp_lessons).get(id_tl):
        print "No such tmp lesson"
        return -3
    tl = s.query(Tmp_lessons).get(id_tl)
    s.delete(tl)
    s.commit()
    return 0

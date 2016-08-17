from sqlalchemy import or_, and_
from database.structure.db_structure import *
__all__ = [
    'select_degrees', 'select_department_rooms', 'select_departments',
    'select_faculties', 'select_groups', 'select_lesson_plans',
    'select_lesson_times', 'select_lesson_types', 'select_lessons',
    'select_rooms', 'select_subject', 'select_teachers',
    'select_universities', 'select_week_days', 'select_weeks'
]


def select_universities(s, id_u=0, **kwargs):
    if kwargs.get('full_name', '') == '' and kwargs.get('short_name', '') == '' and not id_u:
        print "Must be one of the name or id"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    univers_dict = []
    if id_u:
        univer = s.query(Universities).get(id_u)
        if not univer:
            univer = s.query(Universities).get(1)
        u_dict = {'id': univer.id, 'short_name': univer.short_name, 'full_name': univer.full_name}
        univers_dict.append(u_dict)

        return univers_dict

    univers = s.query(Universities)
    for key in kwargs.keys():
        if key in Universities.fields():
            univers = univers.filter(getattr(Universities, key) == kwargs[key])
    univers_obj = univers.all()
    for u in univers_obj:
        u_dict = {'id': u.id, 'short_name': u.short_name, 'full_name': u.full_name}
        univers_dict.append(u_dict)
    if not univers_obj:
        univer = s.query(Universities).get(1)
        u_dict = {'id': univer.id, 'short_name': univer.short_name, 'full_name': univer.full_name}
        univers_dict.append(u_dict)
    return univers_dict


def select_faculties(s, id_f=0, **kwargs):
    if kwargs.get('full_name', '') == '' and kwargs.get('short_name', '') == '' \
            and not kwargs.get('id_university', 0) and not id_f:
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    faculties_dict = []
    if id_f:
        faculty = s.query(Faculties).get(id_f)
        if not faculty:
            faculty = s.query(Faculties).get(1)
        f_dict = {'id': faculty.id, 'short_name': faculty.short_name, 'full_name': faculty.full_name,
                  'id_university': faculty.id_university}
        faculties_dict.append(f_dict)

        return faculties_dict

    faculty = s.query(Faculties)
    for key in kwargs.keys():
        if key in Faculties.fields():
            faculty = faculty.filter(getattr(Faculties, key) == kwargs[key])
    faculties_obj = faculty.all()
    for f in faculties_obj:
        f_dict = {'id': f.id, 'short_name': f.short_name, 'full_name': f.full_name,
                  'id_university': f.id_university}
        faculties_dict.append(f_dict)
    if not faculties_obj:
        f = s.query(Faculties).get(1)
        f_dict = {'id': f.id, 'short_name': f.short_name, 'full_name': f.full_name,
                  'id_university': f.id_university}
        faculties_dict.append(f_dict)
    return faculties_dict


def select_departments(s, id_d=0, **kwargs):
    if kwargs.get('full_name', '') == '' and kwargs.get('short_name', '') == '' \
            and not kwargs.get('id_faculty', 0) and not id_d:
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    deps_dict = []
    if id_d:
        dep = s.query(Departments).get(id_d)
        if not dep:
            dep = s.query(Departments).get(1)
        d_dict = {'id': dep.id, 'short_name': dep.short_name, 'full_name': dep.full_name,
                  'id_faculty': dep.id_faculty}
        deps_dict.append(d_dict)

        return deps_dict

    dep = s.query(Departments)
    for key in kwargs.keys():
        if key in Departments.fields():
            dep = dep.filter(getattr(Faculties, key) == kwargs[key])
    dep_obj = dep.all()
    for d in dep_obj:
        d_dict = {'id': d.id, 'short_name': d.short_name, 'full_name': d.full_name,
                  'id_faculty': d.id_faculty}
        deps_dict.append(d_dict)
    if not dep_obj:
        d = s.query(Departments).get(1)
        d_dict = {'id': d.id, 'short_name': d.short_name, 'full_name': d.full_name,
                  'id_faculty': d.id_faculty}
        deps_dict.append(d_dict)
    return deps_dict


def select_groups(s, id_groups=[], **kwargs):
    if kwargs.get('name', '') == '' and not kwargs.get('id_department', 0) and not id_groups:
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    groups_dict = []
    if id_groups:
        for id_g in id_groups:
            g = s.query(Groups).get(id_g)
            if not g:
                print "No such group"
                return -3
            g_dict = {'id': g.id, 'name': g.name, 'id_department': g.id_department}
            groups_dict.append(g_dict)
        return groups_dict

    groups = s.query(Groups)
    for key in kwargs.keys():
        if key in Groups.fields():
            groups = groups.filter(getattr(Groups, key) == kwargs[key])
    groups_obj = groups.all()
    for g in groups_obj:
        g_dict = {'id': g.id, 'name': g.name, 'id_department': g.id_department}
        groups_dict.append(g_dict)

    return groups_dict


def select_degrees(s, id_d=0, **kwargs):
    if kwargs.get('full_name', '') == '' and kwargs.get('short_name', '') == '' and not id_d:
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    degrees_dict = []
    if id_d:
        d = s.query(Degrees).get(id_d)
        if not d:
            d = s.query(Degrees).get(1)
        d_dict = {'id': d.id, 'short_name': d.short_name, 'full_name': d.full_name, 'teachers': d.teachers}
        degrees_dict.append(d_dict)

        print vars(d)
        for pair in vars(d):
            print pair

        return degrees_dict

    d = s.query(Degrees)
    for key in kwargs.keys():
        if key in Degrees.fields():
            d = d.filter(getattr(Degrees, key) == kwargs[key])
    degrees_obj = d.all()
    for d in degrees_obj:
        d_dict = {'id': d.id, 'short_name': d.short_name, 'full_name': d.full_name}
        degrees_dict.append(d_dict)
    if not degrees_obj:
        d = s.query(Degrees).get(1)
        d_dict = {'id': d.id, 'short_name': d.short_name, 'full_name': d.full_name}
        degrees_dict.append(d_dict)
    return degrees_dict


# I'm not sure about this one:
def select_teachers(s, id_t=0, **kwargs):
    if kwargs.get('full_name', '') == '' and kwargs.get('short_name', '') == '' \
            and not kwargs.get('id_department', 0) and not kwargs.get('id_degree', 0) and not id_t:
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    teachers_dict = []
    if id_t:
        t = s.query(Teachers).get(id_t)
        if not t:
            t = s.query(Teachers).get(1)
        t_dict = {'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name,
                  'id_department': t.id_department, 'id_degree': t.id_degree}
        teachers_dict.append(t_dict)

        return teachers_dict

    t = s.query(Teachers)
    for key in kwargs.keys():
        if key in Teachers.fields():
            t = t.filter(getattr(Teachers, key) == kwargs[key])
    teachers_obj = t.all()
    for t in teachers_obj:
        t_dict = {'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name,
                  'id_department': t.id_department, 'id_degree': t.id_degree}
        teachers_dict.append(t_dict)
    if not teachers_obj:
        t = s.query(Teachers).get(1)
        t_dict = {'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name,
                  'id_department': t.id_department, 'id_degree': t.id_degree}
        teachers_dict.append(t_dict)
    return teachers_dict


def select_rooms(s, id_r=0, **kwargs):
    if kwargs.get('name', '') == '' and not kwargs.get('capacity', 0) and kwargs.get('additional_stuff', '') == '' \
            and not kwargs.get('departments', []) and not id_r:
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    rooms_dict = []
    if id_r:
        r = s.query(Rooms).get(id_r)
        if not r:
            print "No such room"
            return -3
        d_vect = []
        for d in r.departments:
            d_vect.append(select_departments(d.id))
        r_dict = {'id': r.id, 'name': r.name, 'capacity': r.capacity,
                  'departments': d_vect, 'additional_stuff': r.additional_stuff}
        rooms_dict.append(r_dict)

        return r
        # return rooms_dict

    r = s.query(Rooms)
    for key in kwargs.keys():
        if key in Rooms.fields():
            if key == 'departments':
                r = r.filter(Rooms.departments.any(Departments.id.in_(kwargs[key])))
            r = r.filter(getattr(Rooms, key) == kwargs[key])
    rooms_obj = r.all()
    for r in rooms_obj:
        d_vect = []
        for d in r.departments:
            d_vect.append(select_departments(d.id))
        r_dict = {'id': r.id, 'name': r.name, 'capacity': r.capacity,
                  'departments': d_vect, 'additional_stuff': r.additional_stuff}
        rooms_dict.append(r_dict)

    return rooms_obj


def select_subject(s, id_s=0, **kwargs):
    if kwargs.get('full_name', '') == '' and kwargs.get('short_name', '') == '' and not id_s:
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    sub_dict = []
    if id_s:
        sub = s.query(Subjects).get(id_s)
        if not sub:
            print "No such subject"

            return -3
        s_dict = {'id': sub.id, 'short_name': sub.short_name, 'full_name': sub.full_name}
        sub_dict.append(s_dict)

        return sub_dict

    sub = s.query(Subjects)
    for key in kwargs.keys():
        if key in Faculties.fields():
            sub = sub.filter(getattr(Subjects, key) == kwargs[key])
    sub_obj = sub.all()
    for sub in sub_obj:
        s_dict = {'id': sub.id, 'short_name': sub.short_name, 'full_name': sub.full_name}
        sub_dict.append(s_dict)

    return sub_dict


def select_lesson_types(s, id_t=0, **kwargs):
    if kwargs.get('full_name', '') == '' and kwargs.get('short_name', '') == '' and not id_t:
        # print "Must be one of the parameters"
        t = s.query(LessonTypes).get(1)
        return [{'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name}]
    if type(s) is int:
        print "No session"
        return -2

    type_dict = []
    if id_t:
        t = s.query(LessonTypes).get(id)
        if not t:
            print "No such type"

            return -3
        t_dict = {'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name}
        type_dict.append(t_dict)

        return type_dict

    t = s.query(LessonTypes)
    for key in kwargs.keys():
        if key in LessonTypes.fields():
            t = t.filter(getattr(LessonTypes, key) == kwargs[key])
    t_obj = t.all()
    for t in t_obj:
        t_dict = {'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name}
        type_dict.append(t_dict)

    return type_dict


def select_lesson_times(s, id_t=0, **kwargs):
    if kwargs.get('full_name', '') == '' and kwargs.get('short_name', '') == '' and not id_t:
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    type_dict = []
    if id_t:
        t = s.query(LessonTimes).get(id)
        if not t:
            print "No such lesson time"

            return -3
        t_dict = {'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name}
        type_dict.append(t_dict)

        return type_dict

    t = s.query(LessonTimes)
    for key in kwargs.keys():
        if key in LessonTimes.fields():
            t = t.filter(getattr(LessonTimes, key) == kwargs[key])
    t_obj = t.all()
    for t in t_obj:
        t_dict = {'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name}
        type_dict.append(t_dict)

    return type_dict


def select_week_days(s, id_t=0, **kwargs):
    if kwargs.get('full_name', '') == '' and kwargs.get('short_name', '') == '' and not id_t:
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    type_dict = []
    if id_t:
        t = s.query(WeekDays).get(id)
        if not t:
            print "No such day"

            return -3
        t_dict = {'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name}
        type_dict.append(t_dict)

        return type_dict

    t = s.query(WeekDays)
    for key in kwargs.keys():
        if key in WeekDays.fields():
            t = t.filter(getattr(WeekDays, key) == kwargs[key])
    t_obj = t.all()
    for t in t_obj:
        t_dict = {'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name}
        type_dict.append(t_dict)

    return type_dict


def select_weeks(s, id_t=0, **kwargs):
    if kwargs.get('full_name', '') == '' and kwargs.get('short_name', '') == '' and not id_t:
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    type_dict = []
    if id_t:
        t = s.query(Weeks).get(id)
        if not t:
            print "No such week"

            return -3
        t_dict = {'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name}
        type_dict.append(t_dict)

        return type_dict

    t = s.query(Weeks)
    for key in kwargs.keys():
        if key in Weeks.fields():
            t = t.filter(getattr(Weeks, key) == kwargs[key])
    t_obj = t.all()
    for t in t_obj:
        t_dict = {'id': t.id, 'short_name': t.short_name, 'full_name': t.full_name}
        type_dict.append(t_dict)

    return type_dict


def select_lesson_plans(s, id_lesson_plan=[], **kwargs):
    if not kwargs.get('id_subject', 0) and not kwargs.get('id_lesson_type', 0) \
            and not kwargs.get('amount') and not kwargs.get('capacity', 0) \
            and not (kwargs.get('split_groups') == 0 or kwargs.get('split_groups') == 1) \
            and kwargs.get('param_checker', '') == '' and not id_lesson_plan and not kwargs.get('groups', []) \
            and not kwargs.get('teachers', []):
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    les_plan_dict = []
    if id_lesson_plan:
        for id_lp in id_lesson_plan:
            lp = s.query(LessonPlans).get(id_lp)
            if not lp:
                print "No such lesson plan"

                return -3
            g_vect = []
            t_vect = []
            for t in lp.teachers:
                t_vect.append(select_teachers(s, t.id))
            lp = s.query(LessonPlans).get(id_lp)
            for g in lp.groups:
                g_vect.append(select_groups(s, [g.id]))
            lp_dict = {'id': lp.id, 'id_subject': lp.id_subject, 'id_lesson_type': lp.id_lesson_type,
                       'amount': lp.amount, 'capacity': lp.capacity,
                       'split_groups': lp.split_groups, 'param_checker': lp.param_checker, 'groups': g_vect,
                       'teachers': t_vect}
            les_plan_dict.append(lp_dict)

        return les_plan_dict

    lp = s.query(LessonPlans)
    for key in kwargs.keys():
        if key == 'groups' or key == 'teachers':
            # for gt in kwargs[key]:
                # lp = lp.filter(getattr(LessonPlans, key).any(getattr(LessonPlans, key) == gt))
            if key == 'groups':
                lp = lp.filter(getattr(LessonPlans, key).any(Groups.id.in_(kwargs[key])))
            else:
                lp = lp.filter(getattr(LessonPlans, key).any(Teachers.id.in_(kwargs[key])))
        elif getattr(LessonPlans, key):
            lp = lp.filter(getattr(LessonPlans, key) == kwargs[key])
    lp_obj = lp.all()
    for lp in lp_obj:
        g_vect = []
        t_vect = []
        for t in lp.teachers:
            t_vect.append(select_teachers(s, t.id))
        for g in lp.groups:
            g_vect.append(select_groups(s, [g.id]))
        lp_dict = {'id': lp.id, 'id_subject': lp.id_subject, 'id_lesson_type': lp.id_lesson_type,
                   'amount': lp.amount, 'capacity': lp.capacity,
                   'split_groups': lp.split_groups, 'param_checker': lp.param_checker, 'groups': g_vect,
                   'teachers': t_vect}
        les_plan_dict.append(lp_dict)

    return les_plan_dict


def select_lessons(s, id_les=[], **kwargs):
    if not kwargs.get('id_lesson_plan', []) and not kwargs.get('id_room', 0) and not kwargs.get('id_lesson_time', 0) \
            and not kwargs.get('id_week_day') and not kwargs.get('id_week', 0) \
            and not kwargs.get('row_time', 0) and not id_les:
        print "Must be one of the parameters"
        return -1

    if type(s) is int:
        print "No session"
        return -2

    lesson_dict = []
    if id_les:
        for id_l in id_les:
            l = s.query(Lessons).get(id_l)
            if not l:
                print "No such lesson"
                return -3
            l_dict = {'id': l.id, 'id_lesson_plan': select_lesson_plans(s, [l.id_lesson_plan]),
                      'id_lesson_time': l.id_lesson_time,
                      'id_week_day': l.id_week_day, 'id_week': l.id_week, 'row_time': l.row_time}
            lesson_dict.append(l_dict)
        return lesson_dict

    l = s.query(Lessons)
    for key in kwargs.keys():
        if key == 'id_lesson_plan':
            lp_dict = [Lessons.id_lesson_plan == id_lp for id_lp in kwargs[key]]
            l = l.filter(or_(*lp_dict))
        elif key in Lessons.fields():
            l = l.filter(getattr(Lessons, key) == kwargs[key])
    l_obj = l.all()
    for l in l_obj:
        l_dict = {'id': l.id, 'id_lesson_plan': select_lesson_plans(s, [l.id_lesson_plan]),
                  'id_lesson_time': l.id_lesson_time,
                  'id_week_day': l.id_week_day, 'id_week': l.id_week, 'row_time': l.row_time}
        lesson_dict.append(l_dict)

    return lesson_dict


def select_department_rooms(s, id_deps=[], id_rooms=[]):
    if not (id_deps or id_rooms):
        print "Must be one of the parameters"
        return -1
    if type(s) is int:
        print "No session"
        return -2

    department_rooms_list = []
    if id_deps:
        if id_rooms:
            for id_d in id_deps:
                for id_r in id_rooms:
                    d_r = s.query(DepartmentRooms).filter(and_(
                        DepartmentRooms.id_department == id_d,
                        DepartmentRooms.id_room == id_r
                    )).all()
                    department_rooms_list += d_r
            return department_rooms_list
        for id_d in id_deps:
            d_r = s.query(DepartmentRooms).filter(
                DepartmentRooms.id_department == id_d
            ).all()
            department_rooms_list += d_r
        return department_rooms_list

    if id_rooms:
        for id_r in id_rooms:
            d_r = s.query(DepartmentRooms).filter(
                DepartmentRooms.id_room == id_r
            ).all()
            department_rooms_list += d_r
        return department_rooms_list

    return department_rooms_list
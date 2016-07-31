#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtCore
from sqlalchemy import Column, Integer, String, ForeignKey
from database.structure.db_structure import *
from database.structure.select_tools import *
from database.start_db.New_db_startup import connect_database
# for f in vars(Universities(short_name=unicode("Unknown", 'utf-8'), full_name=unicode("Unknown", 'utf-8'))):
#     print f

# (getattr(obj,attr))

# ForUp: Could you describe, what kind of improvements do you want to implement?


def get_class_list():
    import db_structure
    class_list = []
    # for var in dir(db_structure):
    for var in db_structure.__all__:
        if not var.startswith('__') and var[0].isupper():
            class_list.append(var)
            print var
    print len(class_list)
    # prin.pop(0)t getattr(db_structure, class_list[0])


def get_fields_list(class_name=''):
    session = connect_database()
    # obj = select_rooms(s, 1)
    # print obj
    print WeekDays.__tablename__
    print WeekDays.single()
    obj = UserDepartments.read(session, True)[0]
    print unicode(obj)
    obj = TeacherPlans.read(session, True)[0]
    print unicode(obj)
    obj = Users.read(session, True)[0]
    print type(unicode(obj))

    # obj = session.query(Departments).all()[0]
    # users = session.query(Users).all()
    # print obj.name
    # print users
    # print dir(obj)
    # print obj.departments[0].fields()
    # print obj.users
    # for merge in session.query(UserDepartments).all():
        # print merge.id_user, ': ', merge.id_department
    # obj.users.pop(1)
    # obj.users.append(users[1])
    # print obj.users

    # print obj.teachers
    # session.delete(obj)
    # session.commit()
    # obj = session.query(Teachers).all()[0]
    # lp = LessonPlans.read(session, id=1)
    # obj = Teachers.read(session, lesson_plans=[lp])[0]
    # print obj
    # setattr(obj, 'id_' + 'department', 0)
    # print obj.department
    # obj.teachers.pop(00)
    # setattr(obj, 'name', u'Unknown')
    # session.commit()
    # print obj.name
    #
    # print type(Departments.id_faculty.table)
    # # print type(Departments.rooms.table)
    # print isinstance(Departments.rooms, Column)
    # print isinstance(Departments.teachers, Column)
    # print isinstance(Departments.id_faculty, Column)

    # print Departments.fields()
    # print obj.fields
    # print obj.columns
    # for field in obj.fields:
    #     print '{0}: {1}'.format(field, getattr(obj, field))
    # for f in dir(obj):
    #     if not f.startswith('_'):
    #         print f
    #         print getattr(Universities, f)
    #         print
    # print getattr(obj, 'staff')


def get_method_list():
    from database import structure
    check_string = '_tools'
    ref_list = []
    import_dict = {}
    with open('all.py', 'wt') as out:
        for var in dir(structure):
            if var.endswith(check_string):
                ref_list.append(var)
                import_list = []
                for foo in dir(getattr(structure, var)):
                    if foo.startswith(var.replace(check_string, '')):
                        import_list.append(foo)
                import_dict.update({var.replace(check_string, ''): import_list})

    print import_dict
    for pair in import_dict:
        print import_dict[pair]
        print len(import_dict[pair])


if __name__ == '__main__':
    get_fields_list()

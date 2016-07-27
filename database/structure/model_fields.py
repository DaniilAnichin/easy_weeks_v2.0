#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtCore
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
    # print getattr(db_structure, class_list[0])


def get_fields_list(class_name=''):
    # except_list = ['delete', 'update', 'select', 'new']
    # for i in dir():
    #     pass

    # s = connect_database()
    # obj = select_universities(s, 1)
    # print obj

    obj = Universities(short_name=unicode("Unknown", 'utf-8'), full_name=unicode("Unknown", 'utf-8'))
    print obj.fields
    print obj.columns
    for field in obj.fields:
        print '{0}: {1}'.format(field, getattr(obj, field))
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


def get_qt_staff():
    for field in dir(QtCore.Qt):
        if field.endswith('Action'):
            print field


if __name__ == '__main__':
    get_qt_staff()

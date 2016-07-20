#!/usr/bin/python
# -*- coding: utf-8 -*-#

import urllib
import json
from db.Database_config import *


def get_teacher_id(s, cur_teacher, add_teacher=True):
    cur_teacher_soname = cur_teacher[cur_teacher.index(' ') + 1:cur_teacher.index(' ', cur_teacher.index(' ') + 1)]

    curURL = "http://api.rozklad.org.ua/v2/teachers/?search={'query': '%s'}" % cur_teacher_soname
    #    webbrowser.open(curURL)
    info = json.load(urllib.urlopen(curURL))
    if info["statusCode"] == 200:
        for row in info['data']:
            if row['teacher_short_name'] == unicode(cur_teacher, 'utf-8'):
                cur_teacher_id = str(row['teacher_id'])
                if add_teacher:
                    new_teacher(s, row['teacher_name'], unicode(cur_teacher[cur_teacher.index(' ') + 1:], 'utf-8'), 1,
                                select_degees(s, short_name=unicode(cur_teacher[:cur_teacher.index(' ')], 'utf-8'))[0]\
                                ['id'])
                return cur_teacher_id
    return -1


def main(args):
    s = create_new_database('FICT_timetable.db')
    #    s = connect_database('FICT_timetable.db')
    with open('_teachers.txt', 'r') as f:
        for teacher in f:
            teacher = teacher[:-2]
            if get_teacher_id(s, teacher) != -1:
                cur_url = "http://api.rozklad.org.ua/v2/teachers/%s/lessons" % get_teacher_id(s, teacher)
                info = json.load(urllib.urlopen(cur_url))
                if info["statusCode"] == 200:
                    lp_dict = []
                    for row in info['data']:
                        for g in row['groups']:
                            new_group(s, g['group_full_name'])
                        new_room(s, row['lesson_room'], 32 * len(row['groups']))
                        new_subject(s, row['lesson_name'], row['lesson_full_name'])
                    for row in info['data']:
                        core_info = {'ln': row['lesson_full_name'],
                                     'lt': row['lesson_type'],
                                     'groups': [i['group_full_name'] for i in row['groups']],
                                     'tf2w': 1}
                        b = True
                        for i in [not (core_info['groups'] == i['groups'] and core_info['ln'] == i['ln'] and \
                                       core_info['lt'] == i['lt']) for i in lp_dict]:
                            b &= i
                        if b or not lp_dict:
                            lp_dict.append(core_info)
                        else:
                            for i in lp_dict:
                                if core_info['groups'] == i['groups'] and core_info['ln'] == i['ln'] and \
                                   core_info['lt'] == i['lt']:
                                    i['tf2w'] += 1
                                    break
                    for lp in lp_dict:
                        id_groups = []
                        for g in lp['groups']:
                            id_groups.append(select_groups(s, name=g)[0]['id'])
                        add_lesson_plan(s, select_subject(s, full_name=lp['ln'])[0]['id'],
                                        select_lesson_types(s, short_name=lp['lt'])[0]['id'],
                                        id_groups,
                                        [select_teachers(s, short_name=unicode(teacher[teacher.index(' ')+1:], 'utf-8'))
                                        [0]['id']],
                                        1, lp['tf2w'], 0, 32 * len(lp['groups']), '')
                    for row in info['data']:
                        id_groups = []
                        for g in row['groups']:
                            id_groups.append(select_groups(s, name=g['group_full_name'])[0]['id'])
                        new_tmp_lesson(s, select_lesson_plans(s, id_subject=select_subject(s,
                                                                                        full_name=
                                                                                        row['lesson_full_name']
                                                                                        )[0]['id'],
                                                          id_lesson_type=select_lesson_types(s,
                                                                                             short_name=
                                                                                             row['lesson_type']
                                                                                             )[0]['id'],
                                                          groups=id_groups)[0]['id'],
                                   select_rooms(s, name=row['lesson_room'])[0]['id'],
                                   int(row['lesson_number']) + (5 * (int(row['day_number'])-1)) + (30 * (int(
                                       row['lesson_week'])-1)))
    s.close_all()


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))

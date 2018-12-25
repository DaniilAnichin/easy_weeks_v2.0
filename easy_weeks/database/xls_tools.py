#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import xlsxwriter
from easy_weeks.database.select_table import get_table
from easy_weeks.database.structure import *


titles = {
    'teachers': lambda element: f'Розклад занять, викладач: {element}',
    'groups': lambda element: f'Розклад занять, група: {element}',
    'rooms': lambda element: f'Розклад занять, аудиторія: {element}',
}


def print_table(session, filename, table, element):
    book = xlsxwriter.Workbook(filename)
    data_type = element.__tablename__

    page = book.add_worksheet('Розклад')
    lformat = book.add_format()
    lformat.set_align('center')
    lformat.set_font_size(15)
    lformat.set_border()

    sformat = book.add_format()
    sformat.set_align('vcenter')
    sformat.set_shrink()
    sformat.set_border()
    page.set_column(0, 0, 10)
    page.set_column(1, 1, 15)
    page.set_column(2, 7, 40)
    page.write(1, 0, 'Час', sformat)
    page.write(1, 1, 'Тиждень', sformat)
    for i in range(2, 8):
        page.write(1, i, WeekDays.read(session, id=i)[0].full_name, lformat)
    for i in range(2, 12, 2):
        page.merge_range(i, 0, i+1, 0, LessonTimes.read(session, id=i - ((i-2)/2))[0].full_name, sformat)
        page.write(i, 1, Weeks.read(session, id=2)[0].full_name, sformat)
        page.write(i+1, 1, Weeks.read(session, id=3)[0].full_name, sformat)
    title = titles.get(data_type, None)
    if title:
        page.merge_range(0, 0, 0, 7, title(element), lformat)

    for l in range(5):
        for d in range(6):
            lesson1 = table[0][d][l]
            lesson2 = table[1][d][l]
            names1 = ''
            names2 = ''
            if data_type == 'teachers':
                names1 = ', '.join([g.name for g in lesson1.lesson_plan.groups])
                names2 = ', '.join([g.name for g in lesson2.lesson_plan.groups])
            elif data_type == 'groups':
                names1 = ', '.join([t.short_name for t in lesson1.lesson_plan.teachers])
                names2 = ', '.join([t.short_name for t in lesson2.lesson_plan.teachers])
            data1 = '\n'.join([
                lesson1.lesson_plan.subject.full_name,
                lesson1.lesson_plan.lesson_type.short_name,
                names1,
                lesson1.room.name
            ])
            data2 = '\n'.join([
                lesson2.lesson_plan.subject.full_name,
                lesson2.lesson_plan.lesson_type.short_name,
                names2,
                lesson2.room.name
            ])
            if data_type == 'rooms':
                data1 = '\n'.join([
                    lesson1.lesson_plan.subject.full_name,
                    lesson1.lesson_plan.lesson_type.short_name,
                    ', '.join([t.short_name for t in lesson1.lesson_plan.teachers]),
                    ', '.join([g.name for g in lesson1.lesson_plan.groups])
                ])
                data2 = '\n'.join([
                    lesson2.lesson_plan.subject.full_name,
                    lesson2.lesson_plan.lesson_type.short_name,
                    ', '.join([t.short_name for t in lesson2.lesson_plan.teachers]),
                    ', '.join([g.name for g in lesson2.lesson_plan.groups])
                ])
            if lesson1.id == 1:
                data1 = ''
            if lesson2.id == 1:
                data2 = ''
            if data1 == data2:
                page.merge_range(2*l+2, d+2, 2*l+3, d+2, data1, sformat)
            else:
                page.write(2*l + 2, d + 2, data1, sformat)
                page.write(2*l + 3, d + 2, data2, sformat)
    for row in range(13):
        page.set_row(row, 75)
    page.set_landscape()
    page.print_area(0, 0, 12, 7)
    page.fit_to_pages(1, 1)
    book.close()


def print_department_table(session, save_dst, data_type, dep_id):
    data_dict = {'teachers': Teachers, 'groups': Groups}
    book = xlsxwriter.Workbook(save_dst)
    page = book.add_worksheet('Розклад')

    page.set_column(0, 0, 5)
    page.set_column(1, 1, 10)
    page.set_column(2, 2, 15)

    lformat = book.add_format()
    lformat.set_align('center')
    lformat.set_font_size(15)
    lformat.set_border()

    sformat = book.add_format()
    sformat.set_align('vcenter')
    sformat.set_shrink()
    sformat.set_border()

    vformat = book.add_format()
    vformat.set_border()
    vformat.set_rotation(90)
    vformat.set_align('vcenter')

    tformat = book.add_format()
    tformat.set_border()
    tformat.set_shrink()
    tformat.set_align('vcenter')

    page.set_row(1, 100, sformat)
    for i in range(2, 53, 10):
        page.merge_range(i, 0, i+9, 0, WeekDays.read(session, id=(i-2)/10+2)[0].full_name, vformat)
        for j in range(5):
            page.merge_range(i+2*j, 1, i+2*j+1, 1, LessonTimes.read(session, id=j+2)[0].full_name, sformat)
            for k in range(2):
                page.write(i+2*j+k, 2, Weeks.read(session, id=k+2)[0].full_name, sformat)

    column_index = 3

    for e in data_dict[data_type].read(session, id_department=dep_id):
        if isinstance(e, Teachers):
            page.write(1, column_index, e.degree.short_name + ' ' + e.short_name, tformat)
        else:
            page.write(1, column_index, e.name, tformat)

        table = get_table(session, e)
        for l in range(5):
            for d in range(6):
                lesson1 = table[0][d][l]
                lesson2 = table[1][d][l]
                names1 = ''
                names2 = ''
                if data_type == 'teachers':
                    names1 = ', '.join([g.name for g in lesson1.lesson_plan.groups])
                    names2 = ', '.join([g.name for g in lesson2.lesson_plan.groups])
                elif data_type == 'groups':
                    names1 = ', '.join([t.short_name for t in lesson1.lesson_plan.teachers])
                    names2 = ', '.join([t.short_name for t in lesson2.lesson_plan.teachers])
                data1 = '\n'.join([
                    lesson1.lesson_plan.subject.full_name,
                    lesson1.lesson_plan.lesson_type.short_name,
                    names1,
                    lesson1.room.name
                ])
                data2 = '\n'.join([
                    lesson2.lesson_plan.subject.full_name,
                    lesson2.lesson_plan.lesson_type.short_name,
                    names2,
                    lesson2.room.name
                ])
                if lesson1.id == 1:
                    data1 = ''
                if lesson2.id == 1:
                    data2 = ''
                if data1 == data2:
                    page.merge_range(2 * l + 2 + 10 * d, column_index, 2 * l + 3 + 10 * d, column_index, data1, sformat)
                else:
                    page.write(2 * l + 2 + 10 * d, column_index, data1, sformat)
                    page.write(2 * l + 3 + 10 * d, column_index, data2, sformat)
        column_index += 1

    column_index -= 1
    page.merge_range(0, 0, 0, column_index, 'Розклад %s кафедри %s' % ('викладачів'
                                                                       if data_type == 'teachers'
                                                                       else 'груп',
                     Departments.read(session, id=dep_id)[0].full_name), lformat)
    for row in range(2, 63):
        page.set_row(row, 75)
    page.set_column(3, column_index, 40)
    page.print_area(0, 0, 62, column_index)
    page.set_paper(8)
    page.set_landscape()
    page.fit_to_pages(1, 1)

    book.close()

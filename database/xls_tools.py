#!/usr/bin/python
# -*- coding: utf-8 -*- #
import xlsxwriter
from database.structure.db_structure import *


def print_table(session, save_dest, table, data_type, data_id):
    book = xlsxwriter.Workbook(save_dest)
    page = book.add_worksheet(u'Розклад')
    lformat = book.add_format()
    lformat.set_align('center')
    lformat.set_font_size(15)
    lformat.set_border()
    sformat = book.add_format()
    sformat.set_border()
    page.set_column(0, 0, 10)
    page.set_column(1, 7, 40)
    page.merge_range(1, 0, 1, 6, u'Тиждень І', lformat)
    for i in range(1, 7):
        page.write(2, i, WeekDays.read(session, id=i + 1)[0].full_name, sformat)
    for i in range(3, 8):
        page.write(i, 0, LessonTimes.read(session, id=i - 1)[0].full_name, sformat)
    page.merge_range(8, 0, 8, 6, u'Тиждень ІІ', lformat)
    for i in range(1, 7):
        page.write(9, i, WeekDays.read(session, id=i + 1)[0].full_name, sformat)
    for i in range(10, 15):
        page.write(i, 0, LessonTimes.read(session, id=i - 8)[0].full_name, sformat)
    if data_type == u'teachers':
        page.merge_range(0, 0, 0, 6,
                         u'Розклад занять, викладач: %s' % Teachers.read(session, id=data_id)[0].full_name,
                         lformat)
        for w in range(2):
            for l in range(5):
                for d in range(6):
                    lesson = table[w][d][l]
                    if not lesson.id == 1:
                        groups = [g.name for g in lesson.lesson_plan.groups]
                        names = u', '.join(groups)
                        page.write(l+3+w*7, d+1, lesson.lesson_plan.subject.full_name + u'\n' +
                                   lesson.lesson_plan.lesson_type.short_name + u'\n' +
                                   names + u'\n' +
                                   lesson.room.name, sformat)
                    else:
                        page.write_blank(l+3+w*7, d+1, u'i_love_assembler', sformat)

    for row in range(15):
        page.set_row(row, 75)
    page.set_landscape()
    page.set_page_view()
    page.print_area(0, 0, 14, 6)
    page.fit_to_pages(1, 1)
    book.close()

#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from PyQt5.QtWidgets import QApplication


# try:
#     _encoding = QApplication.UnicodeUTF8
#
#     def translate(context, text, disambig):
#         return QApplication.translate(context, text, disambig, _encoding)
# except AttributeError:
#     def translate(context, text, disambig):
#         return QApplication.translate(context, text, disambig)


def shorten(item, number=15):
    line = str(item)
    return line[:number] + (line[number:] and '...')


def format_errors(overlay_dict):
    from easy_weeks.database.structure import Lessons
    header = 'Перекриття у заняттях:\n'
    for key in overlay_dict.keys():
        time = map(lambda x: Lessons.from_row(x), overlay_dict[key])
        time_output = map(lambda x: '{0}/{1}/{2}'.format(
            x['id_week'] - 1,
            x['id_week_day'] - 1,
            x['id_lesson_time'] - 1
        ), time)

        header += f'{key}: {", ".join(time_output)}\n'
    return header


translates = {
    'name': 'Назва',
    'capacity': 'Місткість',
    'amount': 'Пар за 2 тиждні',
    'additional_stuff': 'Додатковво',
    'full_name': 'Повне ім\'я',
    'short_name': 'Скорочене ім\'я',
    'nickname': 'Логін',
    'status': 'Статус',
    'hashed_password': 'Закодований пароль',
    'needed_stuff': 'Додатково',
    'split_groups': 'Розбивати групи'
}


titles_for_single = {
    'teachers': lambda element: f'Розклад занять, викладач: {element}',
    'groups': lambda element: f'Розклад занять, група: {element}',
    'rooms': lambda element: f'Розклад занять, аудиторія: {element}',
}


titles_for_many = {
    'teachers': lambda department: f'Розклад викладачів кафедри {department}',
    'groups': lambda department: f'Розклад груп кафедри {department}',
    'rooms': lambda department: f'Розклад аудиторій кафедри {department}',
}

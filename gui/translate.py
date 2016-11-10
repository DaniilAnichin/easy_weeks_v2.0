#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore


try:
    fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


def shorten(line, number):
    return line[:number] + (line[number:] and '...')

translates = {
    'name': u'Назва',
    'capacity': u'Місткість',
    'amount': u'Пар за 2 тиждні',
    'additional_stuff': u'Додатковво',
    'full_name': u'Повне ім\'я',
    'short_name': u'Скорочене ім\'я',
    'nickname': u'Логін',
    'status': u'Статус',
    'hashed_password': u'Закодований пароль',
    'needed_stuff': u'Додатково',
    'split_groups': u'Розбивати групи'
}

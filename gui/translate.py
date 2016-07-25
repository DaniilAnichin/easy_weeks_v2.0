#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui
_encoding = QtGui.QApplication.UnicodeUTF8


def _fromUtf8(s):
    return s


def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig, _encoding)

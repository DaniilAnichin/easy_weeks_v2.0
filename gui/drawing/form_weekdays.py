# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form_weekdays.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_WeekDays(object):
    def setupUi(self, WeekDays):
        WeekDays.setObjectName(_fromUtf8("WeekDays"))
        WeekDays.resize(792, 293)
        self.horizontalLayout = QtGui.QHBoxLayout(WeekDays)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.treeWidget = QtGui.QTreeWidget(WeekDays)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.horizontalLayout.addWidget(self.treeWidget)

        self.retranslateUi(WeekDays)
        QtCore.QMetaObject.connectSlotsByName(WeekDays)

    def retranslateUi(self, WeekDays):
        WeekDays.setWindowTitle(_translate("WeekDays", "Form", None))
        self.treeWidget.headerItem().setText(0, _translate("WeekDays", "id", None))
        self.treeWidget.headerItem().setText(1, _translate("WeekDays", "Скорочена назва", None))
        self.treeWidget.headerItem().setText(2, _translate("WeekDays", "Повна назва", None))


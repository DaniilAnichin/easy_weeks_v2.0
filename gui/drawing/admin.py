# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin.ui'
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

class Ui_Editor(object):
    def setupUi(self, Editor):
        Editor.setObjectName(_fromUtf8("Editor"))
        Editor.resize(841, 659)
        self.centralwidget = QtGui.QWidget(Editor)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.itemsChoice = QtGui.QComboBox(self.centralwidget)
        self.itemsChoice.setObjectName(_fromUtf8("itemsChoice"))
        self.itemsChoice.addItem(_fromUtf8(""))
        self.itemsChoice.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.itemsChoice)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addButton = QtGui.QPushButton(self.centralwidget)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout.addWidget(self.addButton)
        self.deleteButton = QtGui.QPushButton(self.centralwidget)
        self.deleteButton.setEnabled(True)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.horizontalLayout.addWidget(self.deleteButton)
        self.editButton = QtGui.QPushButton(self.centralwidget)
        self.editButton.setObjectName(_fromUtf8("editButton"))
        self.horizontalLayout.addWidget(self.editButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        Editor.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(Editor)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Editor.setStatusBar(self.statusbar)

        self.retranslateUi(Editor)
        QtCore.QMetaObject.connectSlotsByName(Editor)

    def retranslateUi(self, Editor):
        Editor.setWindowTitle(_translate("Editor", "Editor", None))
        self.itemsChoice.setItemText(0, _translate("Editor", "Дни недели", None))
        self.itemsChoice.setItemText(1, _translate("Editor", "Викладачi", None))
        self.addButton.setText(_translate("Editor", "Добавить", None))
        self.deleteButton.setText(_translate("Editor", "Удалить", None))
        self.editButton.setText(_translate("Editor", "Редактировать", None))


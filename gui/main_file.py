#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
import login
from functools import partial
from PyQt4 import QtCore, QtGui
from gui.elements import EasyTab
from gui.translate import translate, fromUtf8


# Check if it works on windows...
# On linux default is good enough
class MyTab(QtGui.QTabWidget):
    def setTabEnabled(self, p_int, bool):
        super(MyTab, self).setTabEnabled(p_int, bool)
        self.setStyleSheet(
            'QTabBar::tab::disabled{width: 0; height: 0; margin: 0; '
            'padding: 0; border: none;}'
        )


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, lesson_set):
        MainWindow.resize(805, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)

        # self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        # self.tabWidget = MyTab(self.centralwidget)
        self.tabWidget = EasyTab(self.centralwidget)
        self.tabWidget.set_table(lesson_set)

        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 19))
        self.menubar.setObjectName(fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(fromUtf8("menu_2"))
        self.menu_3 = QtGui.QMenu(self.menubar)
        self.menu_3.setObjectName(fromUtf8("menu_3"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOneOne = QtGui.QAction(MainWindow)
        self.actionOneOne.setObjectName(fromUtf8("actionOneOne"))
        self.actionOneTwo = QtGui.QAction(MainWindow)
        self.actionOneTwo.setObjectName(fromUtf8("actionOneTwo"))
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName(fromUtf8("action"))
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName(fromUtf8("action_2"))
        self.action_3 = QtGui.QAction(MainWindow)
        self.action_3.setObjectName(fromUtf8("action_3"))
        self.action_5 = QtGui.QAction(MainWindow)
        self.action_5.setObjectName(fromUtf8("action_5"))
        self.action_6 = QtGui.QAction(MainWindow)
        self.action_6.setObjectName(fromUtf8("action_6"))
        self.action_7 = QtGui.QAction(MainWindow)
        self.action_7.setObjectName(fromUtf8("action_7"))
        self.action_9 = QtGui.QAction(MainWindow)
        self.action_9.setObjectName(fromUtf8("action_9"))
        self.action_10 = QtGui.QAction(MainWindow)
        self.action_10.setObjectName(fromUtf8("action_10"))
        self.menu.addAction(self.action)
        self.menu_2.addAction(self.action_2)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action_5)
        self.menu_2.addAction(self.action_6)
        self.menu_3.addAction(self.action_7)
        self.menu_3.addSeparator()
        self.menu_3.addAction(self.action_9)
        self.menu_3.addAction(self.action_10)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(translate("MainWindow", "MainWindow", None))

        self.menu.setTitle(translate("MainWindow", "Відображення", None))
        self.menu_2.setTitle(translate("MainWindow", "Користувач", None))
        self.menu_3.setTitle(translate("MainWindow", "База даних", None))
        self.actionOneOne.setText(translate("MainWindow", "OneOne", None))
        self.actionOneTwo.setText(translate("MainWindow", "OneTwo", None))
        self.action.setText(translate("MainWindow", "Задати розклад", None))
        self.action_2.setText(
            translate("MainWindow", "Заявка на реєстрацію", None))
        self.action_3.setText(translate("MainWindow", "Вхід", None))
        self.action_5.setText(translate("MainWindow", "Вхід", None))
        self.action_6.setText(translate("MainWindow", "Вихід", None))
        self.action_7.setText(translate("MainWindow", "Завантаження", None))
        self.action_9.setText(translate("MainWindow", "Перевірка", None))
        self.action_10.setText(translate("MainWindow", "Збереження", None))


def main():
    from random import randint
    lesson_set = [[randint(0, 2) for i in range(5)] for j in range(12)]

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window, lesson_set)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

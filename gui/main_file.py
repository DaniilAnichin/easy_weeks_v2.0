#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
from functools import partial
from PyQt4 import QtCore, QtGui
from database import Logger
from database.structure import *
from database.start_db.New_db_startup import connect_database
from gui.elements import EasyTab, WeekMenuBar
from gui.translate import translate, fromUtf8
logger = Logger()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, view_args, lesson_set):
        MainWindow.resize(805, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.hbox = QtGui.QHBoxLayout(self.centralwidget)

        menu_data = [
            [
                'Відображення',
                ['Задати розклад', self.show_table_dialog]
            ],
            [
                'Користувач',
                ['Заявка на реєстрацію',  self.make_account_query],
                [],
                ['Вхід', self.login],
                ['Вихід', self.logout]
            ],
            [
                'База даних',
                ['Завантження',  self.load_database],
                [],
                ['Перевірка', self.check_database],
                ['Збереження', self.save_database]
            ]
        ]

        self.tabWidget = EasyTab(self.centralwidget, MainWindow.session)
        self.tabWidget.set_table(lesson_set, view_args)

        self.hbox.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar = WeekMenuBar(MainWindow, menu_data=menu_data)
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)

        # timer = QtCore.QTimer()
        # timer.setSingleShot(True)
        # timer.singleShot(5000, partial(
        #     self.tabWidget.setTabEnabled,
        #     2,
        #     False
        # ))

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(fromUtf8('EasyWeeks'))
        logger.info('Passed MainMenu TranslateUI function')

    def show_table_dialog(self):
        logger.info('Started table choosing dialog function')

    def make_account_query(self):
        logger.info('Started account query sending function')

    def login(self):
        logger.info('Started user login function')

    def logout(self):
        logger.info('Started user logout function')

    def load_database(self):
        logger.info('Started database uploading function')

    def check_database(self):
        logger.info('Started database check function')

    def save_database(self):
        logger.info('Started database saving function')


def main():
    # lesson_set = [[randint(0, 2) for i in range(5)] for j in range(12)]
    session = connect_database()
    lesson_set = [[[Lessons.read(session, id=1)[0]
                    for i in range(len(Lessons.time_ids))]
                   for j in range(len(Lessons.day_ids))]
                  for k in range(len(Lessons.week_ids))]

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    window.session = session
    ui = Ui_MainWindow()
    ui.setupUi(window, 'teachers', lesson_set)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

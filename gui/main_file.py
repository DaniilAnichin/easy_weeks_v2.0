#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
from PyQt4 import QtCore, QtGui
from database import Logger
from database.structure import *
from database.start_db.New_db_startup import connect_database
from database.select_table import get_table
from gui.dialogs import LoginDialog, TableChoosingDialog
from gui.elements import EasyTab, WeekMenuBar
from gui.translate import fromUtf8
logger = Logger()


class WeeksMenu(QtGui.QMainWindow):
    def __init__(self, session):
        super(WeeksMenu, self).__init__()
        self.resize(805, 600)
        self.session = session
        self.center = QtGui.QWidget(self)
        self.hbox = QtGui.QHBoxLayout(self.center)

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
        self.tabs = EasyTab(self.center, self.session)
        self.set_user(Users.read(self.session, nickname='Admin')[0])
        # self.set_user()

        self.hbox.addWidget(self.tabs)
        self.setCentralWidget(self.center)

        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.menubar = WeekMenuBar(self, menu_data=menu_data)
        self.setMenuBar(self.menubar)

        default_data = [get_table(self.session, 'groups', 136), 'groups']
        self.tabs.set_table(*default_data)

        self.retranslateUi()
        self.tabs.setCurrentIndex(0)

    def retranslateUi(self):
        self.setWindowTitle(fromUtf8('EasyWeeks'))
        logger.info('Passed MainMenu TranslateUI function')

    def show_table_dialog(self):
        logger.info('Started table choosing dialog function')
        self.table = TableChoosingDialog(self.session)
        if self.table.exec_() == QtGui.QDialog.Accepted:
            data_type = self.table.data_type
            data_id = self.table.data_id
            logger.debug('%s - %s' % (data_type, data_id))
            self.tabs.set_table(get_table(self.session, data_type, data_id), data_type)

    def make_account_query(self):
        logger.info('Started account query sending function')

    def login(self):
        logger.info('Started user login function')
        self.login = LoginDialog(Users.read(self.session, all_=True))
        if self.login.exec_() == QtGui.QDialog.Accepted:
            self.set_user(self.login.user)
            logger.info("Logged in as %s" % self.user.nickname)

    def set_user(self, user=None):
        self.user = user
        admin_index = self.tabs.indexOf(self.tabs.tab_admin)
        method_index = self.tabs.indexOf(self.tabs.tab_method)
        admin, method = False, False
        if user:
            if user.status == u'admin':
                admin = True
            elif user.status == u'method':
                method = True

        self.tabs.setTabEnabled(method_index, admin or method)
        self.tabs.setTabEnabled(admin_index, admin)

    def logout(self):
        logger.info('Started user logout function')
        self.set_user()

    def load_database(self):
        logger.info('Started database uploading function')

    def check_database(self):
        logger.info('Started database check function')

    def save_database(self):
        logger.info('Started database saving function')


def main():
    session = connect_database()
    app = QtGui.QApplication(sys.argv)

    window = WeeksMenu(session)
    app.aboutToQuit.connect(window.tabs.method_table.before_close)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

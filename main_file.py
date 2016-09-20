#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
from PyQt4 import QtGui
from database import Logger
from database.structure.db_structure import *
from database.start_db.New_db_startup import connect_database
from database.xls_tools import print_table
from database.select_table import get_table, check_table, save_table, recover_empty
from gui.dialogs import LoginDialog, TableChoosingDialog, ImportDialog, \
    AccountQuery
from gui.elements import EasyTab, WeekMenuBar
from gui.translate import fromUtf8
logger = Logger()


class WeeksMenu(QtGui.QMainWindow):
    def __init__(self):
        super(WeeksMenu, self).__init__()
        self.resize(805, 600)
        self.session = connect_database()
        self.center = QtGui.QWidget(self)
        self.hbox = QtGui.QHBoxLayout(self.center)

        menu_data = [
            [
                'Відображення',
                ['Задати розклад', self.set_tabs_table]
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
                ['Завантаження',  self.load_database],
                [],
                ['Перевірка', self.check_database],
                ['Збереження', self.save_database],
                ['Друк', self.print_database]
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

        self.cur_data_type = 'teachers'
        self.cur_data = 69

        self.set_tabs_table([self.cur_data_type, self.cur_data])

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(fromUtf8('EasyWeeks'))
        logger.info('Passed MainMenu TranslateUI function')

    def set_tabs_table(self, data=None):
        if not isinstance(data, list):
            logger.debug('No?')

            data = self.show_table_dialog()
            # data = [self.cur_data_type, self.cur_data]
        self.table_data = get_table(self.session, *data)
        if not self.tabs.set_table(self.table_data, data[0]):
            self.cur_data_type, self.cur_data = tuple(data)

    def show_table_dialog(self):
        logger.info('Started table choosing dialog function')
        self.table = TableChoosingDialog(self.session)
        if self.table.exec_() == QtGui.QDialog.Accepted:
            data = [self.table.data_type, self.table.data_id]
            logger.debug('%s - %s' % (data[0], data[1]))
            return data

    def login(self):
        logger.info('Started user login function')
        self.login = LoginDialog(Users.read(self.session, all_=True))
        if self.login.exec_() == QtGui.QDialog.Accepted:
            self.set_user(self.login.user)
            logger.info("Logged in as %s" % self.user.nickname)

    def make_account_query(self):
        logger.info('Started account query sending function')
        self.query = AccountQuery(self.session)
        self.query.exec_()

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

        self.update = ImportDialog(self.session)
        self.update.show()

    def check_database(self):
        logger.info('Started database check function')
        check_table(self.session)

    def save_database(self):
        logger.info('Started database saving function')
        save_table(self.session)
        self.tabs.method_table.set_edited(False)

    def print_database(self):
        note = u'Збереження файлу для друку'
        teacher_name = Teachers.read(self.session, id=self.cur_data)[0].short_name.replace(u' ', u'_')[:-1]
        name = u'Розклад_%s.xlsx' % teacher_name
        save_dest = QtGui.QFileDialog.getSaveFileName(
            None, note, directory=name, filter=u'ExcelFiles (*.xlsx)'
        )
        save_dest = unicode(save_dest)
        if not save_dest.endswith(u'.xlsx'):
            save_dest += u'.xlsx'
        print_table(self.session, save_dest, self.table_data, self.cur_data_type, self.cur_data)

    def closeEvent(self, event):
        result = self.tabs.method_table.is_editing()
        if not result:
            event.ignore()
        else:
            self.tabs.method_table.clear_table()
            recover_empty(self.session)
            event.accept()


def main():
    app = QtGui.QApplication(sys.argv)
    window = WeeksMenu()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

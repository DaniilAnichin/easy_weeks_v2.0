#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QDesktopServices
from easy_weeks.database import Logger, EW_VERSION
from easy_weeks.database.start_db.db_startup import connect_database
from easy_weeks.database.start_db.seeds import update_departments, save_departments
from easy_weeks.database.select_table import *
from easy_weeks.database.structure import *
from easy_weeks.gui.dialogs import ImportDialog
from easy_weeks.gui.dialogs import InfoDialog
from easy_weeks.gui.elements import EasyTab
from easy_weeks.gui.elements import WeekMenuBar
from easy_weeks.gui.translate import format_errors
logger = Logger()


class WeeksMenu(QtWidgets.QMainWindow):
    def __init__(self):
        super(WeeksMenu, self).__init__()
        self.resize(1024, 700)
        self.session = connect_database(hard=True)
        self.center = QtWidgets.QWidget(self)
        self.hbox = QtWidgets.QHBoxLayout(self.center)

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
                ['Задати кафедри', self.set_departments],
                ['Зберігти кафедри', self.save_departments],
                [],
                ['Перевірка', self.check_database],
                ['Збереження', self.save_database],
                ['Друк', self.print_database]
            ],
            [
                'Допомога',
                ['Посібник користувача', self.docs],
                [EW_VERSION, lambda x: x]
            ]
        ]
        self.tabs = EasyTab(self.center, self.session)
        self.set_user(Users.read(self.session, nickname='Admin')[0])
        # self.set_user()

        self.hbox.addWidget(self.tabs)
        self.setCentralWidget(self.center)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        self.data_label = QtWidgets.QLabel(self)
        self.statusbar.addWidget(self.data_label)

        self.menubar = WeekMenuBar(self, menu_data=menu_data)
        self.setMenuBar(self.menubar)

        try:
            self.element = Groups.read(self.session, id=2)[0]
            self.set_tabs_table(self.element)
        except Exception as e:
            logger.error(e)
            raise e

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle('EasyWeeks')
        logger.info('Passed MainMenu TranslateUI function')

    def set_tabs_table(self, element=None):
        print(type(element))
        if not type(element) in [Teachers, Rooms, Groups]:
            logger.debug('Incorrect data passed')
            element = self.show_table_dialog()

        if not type(element) in [Teachers, Rooms, Groups]:
            return

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.clear_tabs()
        self.table_data = get_table(self.session, element)
        QtWidgets.QApplication.restoreOverrideCursor()

        if not self.tabs.set_table(self.table_data, element.__tablename__):
            self.element = element
            self.data_label.setText(str(element))

    def set_departments(self):
        logger.info('Started department setting function')
        update_departments(self.session)
        logger.info('Success')

    def save_departments(self):
        logger.info('Started department saving function')
        save_departments(self.session)
        logger.info('Success')

    def show_table_dialog(self):
        logger.info('Started table choosing dialog function')
        from easy_weeks.gui.dialogs import TableChoosingDialog
        self.table = TableChoosingDialog(self.session)
        if self.table.exec_() == QtWidgets.QDialog.Accepted:
            data = [self.table.data_type, self.table.data_id]
            element = get_element(self.session, *data)
            logger.debug(f'Schedule for {self.element}')
            return element

    def login(self):
        logger.info('Started user login function')
        from easy_weeks.gui.dialogs import LoginDialog
        self.login_dialog = LoginDialog(Users.read(self.session, all_=True))
        if self.login_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.set_user(self.login_dialog.user)
            logger.info(f'Logged in as {self.user.nickname}')

    def make_account_query(self):
        logger.info('Started account query sending function')
        from easy_weeks.gui.dialogs import AccountQuery
        self.query = AccountQuery(self)
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
        self.update = ImportDialog(self)
        self.update.show()

    def check_database(self):
        logger.info('Started database check function')
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        ret = check_table(self.session, only_temp=True)
        if ret == 0:
            msg = 'Перевірка успішна'
        else:
            msg = format_errors(ret)
        self.info = InfoDialog(msg)
        self.info.show()
        QtWidgets.QApplication.restoreOverrideCursor()

    def save_database(self):
        logger.info('Started database saving function')
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        ret = save_table(self.session)
        QtWidgets.QApplication.restoreOverrideCursor()
        if ret == 0:
            self.tabs.method_table.set_edited(False)
            msg = 'Збережено успішно'
        else:
            msg = format_errors(ret)
        self.info = InfoDialog(msg)
        self.info.show()

    def print_database(self):
        from easy_weeks.gui.dialogs import PrintDialog
        self.print_dialog = PrintDialog(
            self.session, self.element, self.table_data
        )
        self.print_dialog.show()

    def closeEvent(self, event):
        if not self.clear_tabs():
            event.ignore()
        else:
            event.accept()

    def clear_tabs(self):
        result = self.tabs.method_table.is_editing()
        if not result:
            return False
        else:
            self.tabs.method_table.clear_table()
            clear_temp(self.session)
            recover_empty(self.session)
            return True

    def docs(self):
        QDesktopServices.openUrl(QtCore.QUrl('user_manual.pdf'))

    def keyPressEvent(self, e):
        if e.key() == 0x01000030:  # Qt::KEY_F1
            self.docs()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = WeeksMenu()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

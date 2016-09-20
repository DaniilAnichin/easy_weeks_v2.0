#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
import os
import gui.dialogs
from PyQt4 import QtCore, QtGui
from database import Logger
from database.structure import *
from database.start_db.New_db_startup import connect_database
from database.select_table import get_table, check_data
from gui.dialogs import LoginDialog, TableChoosingDialog, ImportDialog, \
    AccountQuery
from gui.elements import EasyTab, WeekMenuBar
from gui.translate import fromUtf8
logger = Logger()

nullfunc = lambda x: None


class WeeksMenu(QtGui.QMainWindow):
    __instance = None
    __init_replaced = False

    def __new__(cls, *a, **kwa):
        if cls.__instance is None:
            cls.__instance = QtGui.QMainWindow.__new__(cls)

        elif not cls.__init_replaced:
            cls.__init__ = nullfunc
            cls.__init_replaced = True

        return cls.__instance

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

        # self.load_database()
        self.cur_data_type = 'teachers'
        self.cur_data = 69

        self.default_data = [get_table(self.session, self.cur_data_type, self.cur_data), self.cur_data_type]
        self.tabs.set_table(*self.default_data)

        self.retranslateUi()
        self.tabs.setCurrentIndex(0)

    def retranslateUi(self):
        self.setWindowTitle(fromUtf8('EasyWeeks'))
        logger.info('Passed MainMenu TranslateUI function')

    def show_table_dialog(self):
        logger.info('Started table choosing dialog function')
        self.table = TableChoosingDialog(self.session)
        if self.table.exec_() == QtGui.QDialog.Accepted:
            self.cur_data_type = self.table.data_type
            self.cur_data = self.table.data_id
            data_type = self.table.data_type
            data_id = self.table.data_id
            logger.debug('%s - %s' % (data_type, data_id))
            self.tabs.set_table(get_table(self.session, data_type, data_id), data_type)

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
        check_data(self.session)

    def save_database(self):
        logger.info('Started database saving function')

    def print_database(self):
        save_dest = QtGui.QFileDialog.getSaveFileName(None, u'Збереження файлу для друку',
                                                      filter=u'ExcelFiles (*.xlsx)')
        save_dest = unicode(save_dest)
        if not save_dest.endswith(u'.xlsx'):
            save_dest += u'.xlsx'
        import xlsxwriter
        book = xlsxwriter.Workbook(save_dest)
        page = book.add_worksheet(u'Розклад')
        lformat = book.add_format()
        lformat.set_align('center')
        lformat.set_font_size(15)
        lformat.set_border()
        sformat = book.add_format()
        sformat.set_border()
        page.set_column(0, 6, cell_format=sformat)
        page.merge_range(1, 0, 1, 6, u'Тиждень І', lformat)
        for i in range(1, 7):
            page.write(2, i, WeekDays.read(self.session, id=i + 1)[0].full_name, sformat)
        for i in range(3, 8):
            page.write(i, 0, LessonTimes.read(self.session, id=i - 1)[0].full_name, sformat)
        page.merge_range(8, 0, 8, 6, u'Тиждень ІІ', lformat)
        for i in range(1, 7):
            page.write(9, i, WeekDays.read(self.session, id=i + 1)[0].full_name, sformat)
        for i in range(10, 15):
            page.write(i, 0, LessonTimes.read(self.session, id=i - 8)[0].full_name, sformat)
        if self.cur_data_type == u'teachers':
            page.merge_range(0, 0, 0, 6,
                             u'Розклад занять, викладач: %s' % Teachers.read(self.session, id=self.cur_data)[0].full_name,
                             lformat)
            for w in range(2):
                for l in range(5):
                    for d in range(6):
                        if not self.default_data[0][w][d][l].is_empty:
                            groups = [g.name for g in self.default_data[0][w][d][l].lesson_plan.groups]
                            names = u''
                            for g in groups:
                                names += g + u', '
                            names = names[:-2]
                            page.write(l+3+w*7, d+1, self.default_data[0][w][d][l].lesson_plan.subject.full_name + u'\n' +
                                       self.default_data[0][w][d][l].lesson_plan.lesson_type.short_name + u'\n' +
                                       names + u'\n' +
                                       self.default_data[0][w][d][l].room.name, sformat)
        for row in range(15):
            page.set_row(row, 50)
        page.set_column(1, 7, 40)
        page.set_landscape()
        page.set_page_view()
        page.print_area(0, 0, 14, 6)
        page.fit_to_pages(1, 1)
        book.close()

    def closeEvent(self, event):
        result = self.tabs.method_table.before_close()
        if result:
            event.ignore()
        else:
            event.accept()


def main():
    # from database.start_db.New_db_startup import DATABASE_NAME
    # from PyQt4.QtCore import QString
    app = QtGui.QApplication(sys.argv)
    #
    # path = QtGui.QFileDialog.getOpenFileName(directory=QString('/home'))
    # path = unicode(path)
    # f = open(path, 'r')
    # data = f.readlines()
    # f.close()
    # f = open(DATABASE_NAME, 'w')
    # f.writelines(data)
    # f.close()

    session = connect_database()
    window = WeeksMenu(session)
    gui.dialogs.danger_singleton = window
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

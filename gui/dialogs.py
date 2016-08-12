#!/usr/bin/python
# -*- coding: utf-8 -*- #
from functools import partial
from PyQt4 import QtGui, QtCore
from database import Logger
from database.structure import db_structure
from translate import fromUtf8
from gui.elements import CompleterCombo, EditableList

logger = Logger()


class LoginDialog(QtGui.QDialog):
    def __init__(self, users, **kwargs):
        self.users = users
        super(LoginDialog, self).__init__(**kwargs)
        self.submit_button = QtGui.QPushButton(self)
        self.submit_button.clicked.connect(self.accept)
        self.login_input = QtGui.QLineEdit(self)
        self.login_label = QtGui.QLabel(self)
        self.password_input = QtGui.QLineEdit(self)
        self.password_input.setEchoMode(QtGui.QLineEdit.Password)
        self.password_label = QtGui.QLabel(self)

        self.login_form = QtGui.QFormLayout(self)
        self.login_form.addRow(self.login_label, self.login_input)
        self.login_form.addRow(self.password_label, self.password_input)
        self.login_form.addRow(self.submit_button)

        self.retranslateUi()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        logger.info('Passed init for %s', self.__class__.__name__)

        self.setFixedSize(300, 115)

    def retranslateUi(self):
        self.setWindowTitle(fromUtf8('Вікно входу'))

        self.login_label.setText(fromUtf8('Логін: '))
        self.password_label.setText(fromUtf8('Пароль: '))
        self.submit_button.setText(fromUtf8('Увійти'))
        logger.info('Translated UI for %s', self.__class__.__name__)

    def accept(self):
        login = unicode(self.login_input.text())
        password = unicode(self.password_input.text())

        login_users = [user for user in self.users if user.nickname == login]

        if login_users:
            if login_users[0].authenticate(password):
                logger.info('Auth passed')
                super(LoginDialog, self).accept()
            else:
                self.login_input.setText(fromUtf8('Невірний пароль!'))
                logger.info('Incorrect password')
        else:
            self.login_input.setText(fromUtf8('Невірний логін!'))
            logger.info('Incorrect login')


class WeeksDialog(QtGui.QDialog):
    def __init__(self, *args, **kwargs):
        super(WeeksDialog, self).__init__(*args, **kwargs)
        self.setModal(True)
        self.hbox = QtGui.QHBoxLayout(self)
        self.left_vbox = QtGui.QVBoxLayout()
        self.right_vbox = QtGui.QVBoxLayout()

        self.hbox.addLayout(self.left_vbox, 1)
        self.hbox.addLayout(self.right_vbox, 1)

    @staticmethod
    def make_text(element):
        if isinstance(element, list):
            this_text = ', '.join(unicode(item) for item in element)
        else:
            this_text = unicode(element)

        return this_text

    def add_left_label(self, data):
        this_label = QtGui.QLabel(self.make_text(data))
        self.left_vbox.addWidget(this_label, 1)

    def add_right_label(self, data):
        this_label = QtGui.QLabel(self.make_text(data))
        self.right_vbox.addWidget(this_label, 1)

    def add_left_button(self, data, callback, *args, **kwargs):
        this_button = QtGui.QPushButton(self.make_text(data))
        this_button.clicked.connect(partial(callback, *args, **kwargs))
        self.left_vbox.addWidget(this_button, 1)

    def add_right_button(self, data, callback, *args, **kwargs):
        this_button = QtGui.QPushButton(self.make_text(data))
        this_button.clicked.connect(partial(callback, *args, **kwargs))
        self.right_vbox.addWidget(this_button, 1)

    def add_right_combo(self, choice_list, name):
        combo = CompleterCombo()
        combo.addItems(unicode(item) for item in choice_list)
        setattr(self, name, combo)
        self.right_vbox.addWidget(combo, 1)
        logger.info('Added combobox with name "%s"' % name)

    def add_right_list(self, values_list, choice_list, name):
        items_list = EditableList(self, values_list, choice_list, name)
        self.right_vbox.addWidget(items_list, 1)
        logger.info('Added list widget with name "%s"' % name)
        # Something else?


class ShowObject(QtGui.QDialog):
    def __init__(self, element, *args, **kwargs):
        super(ShowObject, self).__init__(*args, **kwargs)
        hbox = QtGui.QHBoxLayout(self)
        self.column_box = QtGui.QVBoxLayout()
        self.values_box = QtGui.QVBoxLayout()
        if type(element).__name__ not in db_structure.__all__:
            logger.debug('Wrong params')
        else:
            logger.debug('All right')
            for column in type(element).columns():
                column_value = getattr(element, column)
                logger.debug('Column {}, value {};'.format(column, column_value))
                column_label = QtGui.QLabel(column, self)
                value_label = QtGui.QLabel(fromUtf8(unicode(column_value)), self)
                self.column_box.addWidget(column_label, 1)
                self.values_box.addWidget(value_label, 1)
        hbox.addLayout(self.column_box, 1)
        hbox.addLayout(self.values_box, 1)


class ShowLesson(WeeksDialog):
    def __init__(self, element, *args, **kwargs):
        super(ShowLesson, self).__init__(*args, **kwargs)

        if not isinstance(element, db_structure.Lessons):
            logger.info('Wrong object passed: not a lesson')
            raise ValueError
        logger.info('Setting lesson data')
        self.lesson = element
        self.lp = self.lesson.lesson_plan

        self.set_pair(db_structure.Groups.translated, self.lp.groups)
        self.set_pair(db_structure.Teachers.translated, self.lp.teachers)
        self.set_pair(db_structure.Subjects.translated, self.lp.subject)
        self.set_pair(db_structure.LessonTypes.translated, self.lp.lesson_type)
        self.set_pair(db_structure.Rooms.translated, self.lesson.room)
        self.set_pair(db_structure.Weeks.translated, self.lesson.week)
        self.set_pair(db_structure.WeekDays.translated, self.lesson.week_day)
        self.set_pair(db_structure.LessonTimes.translated, self.lesson.lesson_time)

    def set_pair(self, first_data, second_data):
        self.add_left_label(first_data)
        self.add_right_label(second_data)


def main():
    import sys
    from database.start_db.New_db_startup import connect_database

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    show_button = QtGui.QPushButton('Login', window)
    session = connect_database()
    obj = db_structure.Lessons.read(session, id=1)
    # dialog = ShowObject(obj[0])
    dialog = ShowLesson(obj[0])

    # users = db_structure.Users.read(session, all_=True)
    # dialog = LoginDialog(users)
    show_button.clicked.connect(dialog.show)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

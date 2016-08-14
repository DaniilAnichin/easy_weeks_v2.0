#!/usr/bin/python
# -*- coding: utf-8 -*- #
from functools import partial
from PyQt4 import QtGui, QtCore
from database import Logger
from database.structure import db_structure
from database.structure.db_structure import *
from translate import fromUtf8
from gui import elements
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
        self.vbox = QtGui.QVBoxLayout(self)

    @staticmethod
    def make_text(element):
        if isinstance(element, list):
            this_text = ', '.join(unicode(item) for item in element)
        else:
            this_text = unicode(element)

        return this_text

    def make_button(self, data, callback, *args, **kwargs):
        this_button = QtGui.QPushButton(self.make_text(data))
        this_button.clicked.connect(partial(callback, *args, **kwargs))
        return this_button

    def make_combo(self, choice_list, selected, name):
        combo = elements.CompleterCombo()
        combo.values = [unicode(item) for item in choice_list]
        combo.addItems(combo.values)
        setattr(self, name, combo)
        combo.setCurrentIndex(combo.values.index(unicode(selected)))
        logger.info('Added combobox with name "%s"' % name)
        return combo

    def make_list(self, values_list, choice_list, name):
        text_values_list = [unicode(value) for value in values_list]
        text_choice_list = [unicode(value) for value in choice_list]
        items_list = elements.EditableList(self, text_values_list, text_choice_list, name)
        logger.info('Added list widget with name "%s"' % name)
        return items_list
        # Something else?

    def set_pair(self, first_data, second_data):
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(self.make_text(first_data)), 1)
        hbox.addWidget(QtGui.QLabel(self.make_text(second_data)), 1)
        self.vbox.addLayout(hbox, 1)

    def set_combo_pair(self, first_data, second_data, name, selected=None):
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(self.make_text(first_data)), 1)
        hbox.addWidget(self.make_combo(second_data, selected, name), 1)
        self.vbox.addLayout(hbox, 1)

    def set_list_pair(self, first_data, second_data, third_data, name):
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(self.make_text(first_data)), 1)
        hbox.addWidget(self.make_list(second_data, third_data, name), 1)
        self.vbox.addLayout(hbox, 1)


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
        
        
class AdminEditor(WeeksDialog):
    def __init__(self, element, *args, **kwargs):
        super(AdminEditor, self).__init__(*args, **kwargs)


class ShowLesson(WeeksDialog):
    def __init__(self, element, *args, **kwargs):
        super(ShowLesson, self).__init__(*args, **kwargs)

        if not isinstance(element, Lessons):
            logger.info('Wrong object passed: not a lesson')
            raise ValueError
        logger.info('Setting lesson data')
        self.lesson = element
        self.lp = self.lesson.lesson_plan

        self.set_pair(Groups.translated, self.lp.groups)
        self.set_pair(Teachers.translated, self.lp.teachers)
        self.set_pair(Subjects.translated, self.lp.subject)
        self.set_pair(LessonTypes.translated, self.lp.lesson_type)
        self.set_pair(Rooms.translated, self.lesson.room)
        self.set_pair(Weeks.translated, self.lesson.week)
        self.set_pair(WeekDays.translated, self.lesson.week_day)
        self.set_pair(LessonTimes.translated, self.lesson.lesson_time)


class EditLesson(WeeksDialog):
    def __init__(self, element, session, time=True, *args, **kwargs):
        super(EditLesson, self).__init__(*args, **kwargs)

        self.session = session

        if not isinstance(element, Lessons):
            logger.info('Wrong object passed: not a lesson')
            raise ValueError

        logger.info('Setting lesson data')
        self.lesson = element
        self.lp = self.lesson.lesson_plan
        # self.set_pair(Teachers.translated, self.lp.teachers)
        # self.set_pair(Groups.translated, self.lp.groups)
        for elem in ['groups', 'teachers']:
            self.default_list_pair(elem, lp=True)
        self.default_combo_pair('subject', lp=True)
        # field_list = ['room'] + (['week', 'week_day', 'lesson_time'] if True else [])
        field_list = ['room'] + (['week', 'week_day', 'lesson_time'] if time else [])
        for elem in field_list:
            self.default_combo_pair(elem)

        self.vbox.addWidget(self.make_button(fromUtf8('Підтвердити'), self.save))

    def default_combo_pair(self, param, lp=False):
        getter = self.lp if lp else self.lesson
        cls = type(getattr(getter, param))
        label = cls.translated
        values = cls.read(self.session, all_=True)
        value = getattr(getter, param)
        name = cls.__tablename__
        self.set_combo_pair(label, values, name, value)

    def default_list_pair(self, param, lp=False):
        getter = self.lp if lp else self.lesson
        cls = type(getattr(getter, param)[0])
        label = cls.translated
        values = cls.read(self.session, all_=True)
        selected_values = getattr(getter, param)
        name = cls.__tablename__
        self.set_list_pair(label, selected_values, values, name)

    def save(self):
        logger.debug('Here must be editor saving')
        self.close()


def main():
    import sys
    from database.start_db.New_db_startup import connect_database

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    show_button = QtGui.QPushButton('Login', window)
    session = connect_database()
    obj = Lessons.read(session, id=1)
    # dialog = ShowObject(obj[0])
    dialog = ShowLesson(obj[0])
    dialog = EditLesson(obj[0], session)

    # users = Users.read(session, all_=True)
    # dialog = LoginDialog(users)
    show_button.clicked.connect(dialog.show)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

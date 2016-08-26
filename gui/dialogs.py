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
        self.user = None

        login_users = [user for user in self.users if user.nickname == login]

        if login_users:
            if login_users[0].authenticate(password):
                logger.info('Auth passed')
                self.user = login_users[0]
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

    def make_combo(self, choice_list, selected, name, sort_key):
        combo = elements.CompleterCombo()
        combo.items = choice_list[:]
        combo.items.sort(key=sort_key)
        combo.addItems([sort_key(item) for item in combo.items])
        setattr(self, name, combo)
        if selected:
            combo.setCurrentIndex(combo.items.index(selected))
        # logger.info('Added combobox with name "%s"' % name)
        return combo

    def make_list(self, values_list, choice_list, name):
        items_list = elements.EditableList(self, values_list, choice_list, name)
        # logger.info('Added list widget with name "%s"' % name)
        return items_list

    def set_pair(self, first_data, second_data):
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(self.make_text(first_data)), 1)
        hbox.addWidget(QtGui.QLabel(self.make_text(second_data)), 1)
        self.vbox.addLayout(hbox, 1)

    def set_combo_pair(self, first_data, second_data, name, key=lambda a: unicode(a), selected=None):
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(self.make_text(first_data)), 1)
        hbox.addWidget(self.make_combo(second_data, selected, name, key), 1)
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
    def __init__(self, element, session, empty=False, *args, **kwargs):
        super(AdminEditor, self).__init__(*args, **kwargs)
        self.session = session
        logger.debug('Element is %s' % element)
        self.empty = empty
        self.cls = element if empty else type(element)
        self.cls_name = self.cls.__name__
        self.element = self.cls.read(self.session, id=1)[0] if empty else element

        if self.cls_name not in db_structure.__all__:
            logger.debug('Wrong params')
        else:
            logger.debug('All right')
            for column in self.cls.fields():
                if not column.startswith('id_') and not column == 'id':
                    self.make_pair(column)
            self.vbox.addWidget(self.make_button(fromUtf8('Підтвердити'), self.accept))

    def make_pair(self, param):
        exp_result = getattr(self.element, param)
        if isinstance(exp_result, list):
            self.default_list_pair(param)
        elif isinstance(exp_result, db_structure.Base):
            self.default_combo_pair(param)
        elif isinstance(exp_result, int):
            self.default_int_pair(param)
        elif isinstance(exp_result, (str, unicode, QtCore.QString)):
            self.default_str_pair(param)
        elif isinstance(exp_result, bool):
            self.default_bool_pair(param)
        else:
            logger.info("What is this - %s, man?" % exp_result)
            logger.info("It is %s" % type(exp_result))

    def default_combo_pair(self, param):
        cls = type(getattr(self.element, param))
        label = cls.translated
        values = cls.read(self.session, all_=True)
        value = None if self.empty else getattr(self.element, param)
        name = cls.__tablename__
        self.set_combo_pair(label, values, name, value)

    def default_list_pair(self, param):
        cls = type(getattr(self.element, param)[0])
        label = cls.translated
        values = cls.read(self.session, all_=True)
        selected_values = [] if self.empty else getattr(self.element, param)
        name = cls.__tablename__
        self.set_list_pair(label, selected_values, values, name)

    def default_int_pair(self, param):
        spin = QtGui.QSpinBox()
        spin.setRange(1, 1000000)
        if not self.empty:
            spin.setValue(getattr(self.element, param))
        setattr(self, param, spin)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(param), 1)
        hbox.addWidget(spin, 1)
        self.vbox.addLayout(hbox, 1)

    def default_str_pair(self, param):
        line = QtGui.QLineEdit()
        if not self.empty:
            line.setText(getattr(self.element, param))
        setattr(self, param, line)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(param), 1)
        hbox.addWidget(line, 1)
        self.vbox.addLayout(hbox, 1)

    def default_bool_pair(self, param):
        check = QtGui.QCheckBox()
        if not self.empty:
            check.setChecked(getattr(self.element, param))
        setattr(self, param, check)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(param), 1)
        hbox.addWidget(check, 1)
        self.vbox.addLayout(hbox, 1)

    def accept(self):
        logger.debug('Here must be editor saving')
        super(AdminEditor, self).accept()


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
        logger.debug('This lesson %s temp' % ('is' if self.lesson.is_temp else 'isn\'t'))


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
        field_list = ['room'] + (['week', 'week_day', 'lesson_time'] if time else [])
        # field_list = ['room', 'week', 'week_day', 'lesson_time']
        for elem in field_list:
            self.default_combo_pair(elem)

        self.vbox.addWidget(self.make_button(fromUtf8('Підтвердити'), self.accept))

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

    def accept(self):
        logger.debug('Here must be editor saving')
        super(EditLesson, self).accept()


class TableChoosingDialog(WeeksDialog):
    def __init__(self, session, *args, **kwargs):
        super(TableChoosingDialog, self).__init__(*args, **kwargs)
        self.session = session
        self.data_types = [Teachers, Groups, Rooms]
        self.set_combo_pair(fromUtf8('Для кого розклад: '), self.data_types, 'type', lambda a: a.translated)
        self.type.currentIndexChanged.connect(self.set_list)
        self.set_combo_pair(fromUtf8('Ім\'я: '), [], 'data_choice')
        self.set_list()
        self.vbox.addWidget(self.make_button(fromUtf8('Підтвердити'), self.accept))

    def set_list(self):
        self.data_type = self.type.items[self.type.currentIndex()]
        self.values = self.data_type.read(self.session, all_=True)[:]
        self.values.sort(key=lambda a: unicode(a))
        self.data_choice.clear()
        self.data_choice.addItems([unicode(item) for item in self.values])

    def accept(self):
        self.data_type = self.data_type.__tablename__
        self.data_id = self.values[self.data_choice.currentIndex()].id
        super(TableChoosingDialog, self).accept()


class RUSureDelete(QtGui.QMessageBox):
    def __init__(self, element):
        super(RUSureDelete, self).__init__()
        self.setIcon(QtGui.QMessageBox.Warning)
        info = u'Ви збираєтеся видилити елемент типу %s,' % element.translated
        info += u'\nа саме: %s' % unicode(element)
        self.setInformativeText(fromUtf8(info))
        self.setWindowTitle(fromUtf8('Видалення елемента'))
        self.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        self.setDefaultButton(QtGui.QMessageBox.Yes)


def main():
    import sys
    from database.start_db.New_db_startup import connect_database

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    show_button = QtGui.QPushButton('Login', window)
    session = connect_database()
    obj = Lessons.read(session, id=1)
    dialog = ShowObject(obj[0])
    # dialog = ShowLesson(obj[0])
    # dialog = EditLesson(obj[0], session)

    # users = Users.read(session, all_=True)
    # dialog = LoginDialog(users)
    show_button.clicked.connect(dialog.show)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from database import Logger, db_codes_output
from database.structure.db_structure import Departments, Users
from gui.translate import fromUtf8
logger = Logger()


class AccountQuery(QtGui.QDialog):
    def __init__(self):
        from main_file import WeeksMenu
        super(AccountQuery, self).__init__()
        self.session = WeeksMenu().session
        self.submit_button = QtGui.QPushButton()
        self.submit_button.clicked.connect(self.accept)

        self.mark_label = QtGui.QLabel(self)
        self.login_label = QtGui.QLabel(self)
        self.login_input = QtGui.QLineEdit(self)
        self.password_label = QtGui.QLabel(self)
        self.password_input = QtGui.QLineEdit(self)
        self.password_input.setEchoMode(QtGui.QLineEdit.Password)
        self.note_label = QtGui.QLabel(self)
        self.note_input = QtGui.QLineEdit(self)

        self.login_form = QtGui.QFormLayout(self)
        self.login_form.addRow(self.mark_label)
        self.login_form.addRow(self.login_label, self.login_input)
        self.login_form.addRow(self.password_label, self.password_input)
        self.login_form.addRow(self.note_label, self.note_input)
        self.login_form.addRow(self.submit_button)

        self.translateUi()
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def translateUi(self):
        self.setWindowTitle(fromUtf8('Вікно входу'))

        self.mark_label.setText(fromUtf8('Тут ви можете залишити заявку\n '
                                         'на створення аккаунту користувача'))
        self.login_label.setText(fromUtf8('Бажаний логін: '))
        self.password_label.setText(fromUtf8('Бажаний пароль: '))
        self.note_label.setText(fromUtf8('Примітка(кафедра): '))
        self.submit_button.setText(fromUtf8('Подати заяву'))

    def accept(self):
        login = unicode(self.login_input.text())
        password = unicode(self.password_input.text()).encode('cp1251')
        message = unicode(self.note_input.text())
        department = Departments.read(self.session, id=2)[0]
        exists = Users.read(self.session, nickname=login)

        if not exists:
            result = Users.create(
                self.session, nickname=login, password=password,
                message=message, status=u'method', departments=[department]
            )
            if isinstance(result, int):
                logger.debug(db_codes_output[result])
            super(AccountQuery, self).accept()
        else:
            self.login_input.setText(fromUtf8('Логін вже існує!'))
            logger.info('Incorrect login')

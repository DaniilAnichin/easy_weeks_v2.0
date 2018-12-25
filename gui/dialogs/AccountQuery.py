#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from database import Logger, db_codes_output
from database.structure import Departments, Users
logger = Logger()


class AccountQuery(QtWidgets.QDialog):
    def __init__(self, parent):
        super(AccountQuery, self).__init__()
        self.session = parent.session
        self.submit_button = QtWidgets.QPushButton()
        self.submit_button.clicked.connect(self.accept)

        self.mark_label = QtWidgets.QLabel(self)
        self.login_label = QtWidgets.QLabel(self)
        self.login_input = QtWidgets.QLineEdit(self)
        self.password_label = QtWidgets.QLabel(self)
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.note_label = QtWidgets.QLabel(self)
        self.note_input = QtWidgets.QLineEdit(self)

        self.login_form = QtWidgets.QFormLayout(self)
        self.login_form.addRow(self.mark_label)
        self.login_form.addRow(self.login_label, self.login_input)
        self.login_form.addRow(self.password_label, self.password_input)
        self.login_form.addRow(self.note_label, self.note_input)
        self.login_form.addRow(self.submit_button)

        self.translateUi()
        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def translateUi(self):
        self.setWindowTitle('Вікно входу')

        self.mark_label.setText('Тут ви можете залишити заявку\n '
                                'на створення аккаунту користувача')
        self.login_label.setText('Бажаний логін: ')
        self.password_label.setText('Бажаний пароль: ')
        self.note_label.setText('Примітка(кафедра): ')
        self.submit_button.setText('Подати заяву')

    def accept(self):
        login = str(self.login_input.text())
        password = str(self.password_input.text()).encode('cp1251')
        message = str(self.note_input.text())
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
            self.login_input.setText('Логін вже існує!')
            logger.info('Incorrect login')

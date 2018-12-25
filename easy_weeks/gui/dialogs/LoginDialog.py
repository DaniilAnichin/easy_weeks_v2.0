#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from easy_weeks.database import Logger
logger = Logger()


class LoginDialog(QtWidgets.QDialog):
    def __init__(self, users, **kwargs):
        self.users = users
        super(LoginDialog, self).__init__(**kwargs)
        self.submit_button = QtWidgets.QPushButton(self)
        self.submit_button.clicked.connect(self.accept)
        self.login_input = QtWidgets.QLineEdit(self)
        self.login_label = QtWidgets.QLabel(self)
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_label = QtWidgets.QLabel(self)

        self.login_form = QtWidgets.QFormLayout(self)
        self.login_form.addRow(self.login_label, self.login_input)
        self.login_form.addRow(self.password_label, self.password_input)
        self.login_form.addRow(self.submit_button)

        self.translateUi()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        logger.info('Passed init for %s', self.__class__.__name__)

        self.setFixedSize(300, 115)

    def translateUi(self):
        self.setWindowTitle('Вікно входу')

        self.login_label.setText('Логін: ')
        self.password_label.setText('Пароль: ')
        self.submit_button.setText('Увійти')
        logger.info('Translated UI for %s', self.__class__.__name__)

    def accept(self):
        login = str(self.login_input.text())
        password = str(self.password_input.text())
        self.user = None

        login_users = [user for user in self.users if user.nickname == login]

        if login_users:
            if login_users[0].authenticate(password):
                logger.info('Auth passed')
                self.user = login_users[0]
                super(LoginDialog, self).accept()
            else:
                self.login_input.setText('Невірний пароль!')
                logger.info('Incorrect password')
        else:
            self.login_input.setText('Невірний логін!')
            logger.info('Incorrect login')

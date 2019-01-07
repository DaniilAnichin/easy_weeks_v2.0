#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QPushButton
from easy_weeks.database import Logger, db_codes_output
from easy_weeks.database.structure import Departments, Users
logger = Logger()


class AccountQuery(QDialog):
    def __init__(self, parent):
        super(AccountQuery, self).__init__()
        self.session = parent.session
        self.submit_button = QPushButton()
        self.submit_button.clicked.connect(self.accept)

        self.mark_label = QLabel(self)
        self.login_label = QLabel(self)
        self.login_input = QLineEdit(self)
        self.password_label = QLabel(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.note_label = QLabel(self)
        self.note_input = QLineEdit(self)

        self.login_form = QFormLayout(self)
        self.login_form.addRow(self.mark_label)
        self.login_form.addRow(self.login_label, self.login_input)
        self.login_form.addRow(self.password_label, self.password_input)
        self.login_form.addRow(self.note_label, self.note_input)
        self.login_form.addRow(self.submit_button)

        self.translateUi()
        self.setWindowModality(Qt.ApplicationModal)

    def translateUi(self):
        self.setWindowTitle('Вікно входу')
        self.mark_label.setText('Тут ви можете залишити заявку\nна створення аккаунту користувача')
        self.login_label.setText('Бажаний логін: ')
        self.password_label.setText('Бажаний пароль: ')
        self.note_label.setText('Примітка(кафедра): ')
        self.submit_button.setText('Подати заяву')

    def accept(self):
        login = self.login_input.text()
        password = self.password_input.text().encode('cp1251')
        message = self.note_input.text()
        department = Departments.read(self.session, id=2)[0]
        exists = Users.read(self.session, nickname=login)

        if not exists:
            result = Users.create(
                self.session, nickname=login, password=password,
                message=message, status='method', departments=[department]
            )
            if isinstance(result, int):
                logger.debug(db_codes_output[result])
            super(AccountQuery, self).accept()
        else:
            self.login_input.setText('Логін вже існує!')
            logger.info('Incorrect login')

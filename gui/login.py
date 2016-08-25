#!/usr/bin/python
# -*- coding: utf-8 -*- #
import bcrypt
import sys
from PyQt4 import QtGui, QtCore
from database import Logger
from gui.translate import fromUtf8
logger = Logger()


class User:
    # move whole model to db_structure
    def __init__(self, name, password, status):
        self.name = name
        self.hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        self.status = status

    def check(self, inputed_pw):
        logger.info('User auth passing')
        return bcrypt.hashpw(inputed_pw, self.hashed) == self.hashed


a_user = User('Forest', 'qwerty', 'admin')
m_user = User('Moder', '123456', 'moder')
users = {user.name: user for user in [a_user, m_user]}


class LoginDialog(QtGui.QDialog):
    def __init__(self, **kwargs):
        self.logger = logger
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
        self.setLayout(self.login_form)

        self.retranslateUi()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.logger.info('Passed init for %s', self.__class__.__name__)

        self.setFixedSize(300, 115)

    def retranslateUi(self):
        self.setWindowTitle(fromUtf8('Вікно входу'))

        self.login_label.setText(fromUtf8('Логін: '))
        self.password_label.setText(fromUtf8('Пароль: '))
        self.submit_button.setText(fromUtf8('Увійти'))
        self.logger.info('Translated UI for %s', self.__class__.__name__)

    def accept(self):
        login = unicode(self.login_input.text()).encode('cp1251')
        password = unicode(self.password_input.text()).encode('cp1251')
        try:
            logged_in = users[login].check(password)
            if logged_in:
                self.logger.info('Auth passed')
                super(LoginDialog, self).accept()
            else:
                self.login_input.setText(fromUtf8('Невірний пароль!'))
                self.logger.info('Incorrect password')
        except KeyError:
            self.login_input.setText(fromUtf8('Невірний логін!'))
            self.logger.info('Incorrect login')


def main():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    show_button = QtGui.QPushButton('Login', window)
    dialog = LoginDialog()
    show_button.clicked.connect(dialog.show)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
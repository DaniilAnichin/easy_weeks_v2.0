#!/usr/bin/python
# -*- coding: utf-8 -*- #
import bcrypt
import sys
from PyQt4 import QtGui, QtCore
from gui.translate import _translate, _fromUtf8


class User:
    def __init__(self, name, password, status):
        self.name = name
        self.hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        self.status = status

    def check(self, inputed_pw):
        return bcrypt.hashpw(inputed_pw, self.hashed) == self.hashed


a_user = User('Forest', 'qwerty', 'admin')
m_user = User('Moder', '123456', 'moder')
users = {user.name: user for user in [a_user, m_user]}


class LoginDialog(QtGui.QDialog):
    def __init__(self, **kwargs):
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
        # vbox = QtGui.QVBoxLayout(self)
        # vbox.addWidget(self.login_input, 1)
        # vbox.addWidget(self.password_input, 1)
        # vbox.addWidget(self.submit_button, 1)
        # self.setLayout(vbox)

        self.retranslateUi()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFixedSize(300, 115)

    def retranslateUi(self):
        self.setWindowTitle(_translate('Login', 'Вікно входу', None))

        self.submit_button.setText(_translate('Login', 'Увійти', None))
        self.login_label.setText(_translate('Login', 'Логін: ', None))
        self.password_label.setText(_translate('Login', 'Пароль: ', None))

    def accept(self):
        login = str(self.login_input.text())
        password = str(self.password_input.text())
        try:
            logged_in = users[login].check(password)
            if logged_in:
                print 'Matched'
                super(LoginDialog, self).accept()
            else:
                self.login_input.setText(
                    _translate('Login', 'Невірний пароль!', None)
                    )
        except KeyError:
            self.login_input.setText(
                _translate('Login', 'Невірний логін!', None)
            )


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
'''
    def initUI(self):
        lo = QFormLayout()
        lo.addRow(QLabel("Type some text in textbox and drag it into combo box"))
        edit = QLineEdit()
        edit.setDragEnabled(True)
        com = Combo("Button", self)
        lo.addRow(edit, com)
        self.setLayout(lo)
        self.setWindowTitle('Simpl
        '''
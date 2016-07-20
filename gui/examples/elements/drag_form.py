#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
from PyQt4.QtGui import *


class Combo(QComboBox):
    def __init__(self, title, parent):
        super(Combo, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print e
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.addItem(e.mimeData().text())


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        lo = QFormLayout()
        lo.addRow(QLabel("Type some text in textbox and drag it into combo box"))
        edit = QLineEdit()
        edit.setDragEnabled(True)
        com = Combo("Button", self)
        lo.addRow(edit, com)
        self.setLayout(lo)
        self.setWindowTitle('Simple drag & drop')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main()

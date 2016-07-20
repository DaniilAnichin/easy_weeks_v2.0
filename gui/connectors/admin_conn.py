#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
import sys
from gui.drawing.admin import Ui_Editor


def main():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    ui = Ui_Editor()
    ui.setupUi(window)
    QtCore.QObject.connect(ui.deleteButton, QtCore.SIGNAL("clicked()"), QtGui.qApp.quit)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()


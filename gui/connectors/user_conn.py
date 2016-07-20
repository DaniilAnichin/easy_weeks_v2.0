#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
import sys
from gui.drawing.user import Ui_MainWindow


def main():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    print type(ui)
    print type(8)
    print type(8.)
    print type('8')
    print type(2 ** 1000000)
    ui.setupUi(window)
    QtCore.QObject.connect(ui.pushButton_4, QtCore.SIGNAL("clicked()"), QtGui.qApp.quit)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

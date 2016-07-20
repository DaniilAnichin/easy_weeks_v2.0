#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
import sys
from gui.drawing.dialog_example import Ui_Dialog


def main():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QWidget()
    ui = Ui_Dialog()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

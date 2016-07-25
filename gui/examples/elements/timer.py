#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys

from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication


def tick():
    print 'tick'


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    timer = QTimer()
    timer.setSingleShot(True)
    timer.singleShot(5000, tick)
    # timer.start(1000)
    # run event loop so python doesn't exit
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
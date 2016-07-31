#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
import logging
from PyQt4 import QtGui, QtCore
from database.structure import db_structure
from database.start_db.New_db_startup import connect_database
from database import set_logger
logger = logging.getLogger()
set_logger(logger)

class ShowObject(QtGui.QDialog):
    def __init__(self, element, *args, **kwargs):
        if type(element).__name__ not in db_structure.__all__:
            logger.debug('Wrong params')
        else:
            logger.debug('All right')
        super(ShowObject, self).__init__(*args, **kwargs)


def main():
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    show_button = QtGui.QPushButton('Login', window)
    session = connect_database()
    obj = db_structure.Universities.read(session, True)
    dialog = ShowObject(obj[0])
    show_button.clicked.connect(dialog.show)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
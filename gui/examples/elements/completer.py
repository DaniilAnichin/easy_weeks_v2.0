#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
from PyQt4 import QtGui
from database import base_path
from gui.translate import translate


def main():
    app = QtGui.QApplication(sys.argv)

    edit = QtGui.QLineEdit()
    edit.setWindowTitle('QLineEdit Auto Complete')
    with open(base_path + 'Import_script/' + '_teachers.txt', 'r') as f:
        teacher_list = [translate('myWindow', teacher[:-2], None)
                        for teacher in f.readlines()]
    completer = QtGui.QCompleter(teacher_list, edit)
    # completer = QtGui.QCompleter([strt(i) for i in range(50)])
    edit.setCompleter(completer)
    edit.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

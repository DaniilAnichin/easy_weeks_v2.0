#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
from functools import partial
from PyQt4 import QtCore, QtGui
from database import BASE_DIR
_encoding = QtGui.QApplication.UnicodeUTF8


def _translate(context, text, disambig):
    return QtGui.QApplication.translate(context, text, disambig, _encoding)


class MyClass(object):
    def __init__(self, arg):
        super(MyClass, self).__init__()
        self.arg = arg


class myWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)

        self.comboBox = QtGui.QComboBox(self)
#        with open(BASE_DIR + '/Import_script/' + '_teachers.txt', 'r') as f:
        with open(BASE_DIR + '/Import_script/' + '_teachers.txt', 'r') as f:
                teacher_list = [_translate('myWindow', teacher[:-2], None)
                            for teacher in f.readlines()]
        # self.comboBox.addItems([str(x) for x in range(1000)])
        self.comboBox.addItems(teacher_list)


        self.myObject = MyClass(id(self))

        self.comboBox.activated.connect(partial(self.myFunction, self.myObject, 'someArg'))

    def myFunction(self, arg1=None, arg2=None):
        print 'myFunction(): ', arg1, arg2
        print 'value is: %s' % self.comboBox.currentIndex()


def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('myApp')
    dialog = myWindow()
    dialog.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

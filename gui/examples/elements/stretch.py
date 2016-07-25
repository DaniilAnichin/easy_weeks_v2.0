#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
from PyQt4 import QtGui


class BoxExample(QtGui.QWidget):
    def __init__(self, parent=None):
        super(BoxExample, self).__init__(parent)
        self.setWindowTitle('BoxLayout example')

        ok = QtGui.QPushButton('OK')
        cancel = QtGui.QPushButton('Cancel')
        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        ok.setSizePolicy(size_policy)
        cancel.setSizePolicy(size_policy)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok, 1)
        hbox.addWidget(cancel, 1)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(hbox, 1)
        vbox.setObjectName('vbox')
        print vbox.objectName()

        self.setLayout(vbox)
        self.resize(300, 150)


def main(args):
    app = QtGui.QApplication(args)
    qb = BoxExample()
    qb.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)

#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore


class DragButton(QtGui.QPushButton):
    def __init__(self, *args):
        super(DragButton, self).__init__(*args)
        size_policy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum
        )
        self.setSizePolicy(size_policy)
        self.setAcceptDrops(True)
        self.lesson = 'None'

    def mousePressEvent(self, e):
        QtGui.QPushButton.mousePressEvent(self, e)

        if e.button() == QtCore.Qt.LeftButton:
            # Pressing callback
            print 'Pressing callback'
            pass

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.RightButton:
            return

        mimeData = QtCore.QMimeData()
        mimeData.setText(self.lesson)

        # Grab the button to a pixmap to make it more fancy
        pixmap = QtGui.QPixmap.grabWidget(self)
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
        painter.end()

        # make a QDrag
        drag = QtGui.QDrag(self)
        drag.setPixmap(pixmap)
        drag.setMimeData(mimeData)
        # shift the Pixmap so that it coincides with the cursor position
        drag.setHotSpot(e.pos())

        # start the drag operation
        # exec_ will return the accepted action from dropEvent
        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            print 'moved'
        else:
            print 'copied'

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        # get the relative position from the mime data
        mime = e.mimeData().text()
        if self != e.source():
            if e.keyboardModifiers() & QtCore.Qt.ShiftModifier:
                # Do we need any other modes??
                e.setDropAction(QtCore.Qt.CopyAction)
            else:
                # Perform swap:
                self.setText(e.source().text() + '(1)')
                e.setDropAction(QtCore.Qt.MoveAction)
                # tell the QDrag we accepted it
                e.accept()
        else:
            e.ignore()


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(DragButton('Button1', self), 1)
        vbox.addWidget(DragButton('Button2', self), 1)
        self.setLayout(vbox)

        self.setWindowTitle('Copy or Move')
        self.setGeometry(300, 300, 280, 150)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    # app.setStartDragDistance(10)
    ex = Example()
    ex.show()
    app.exec_()

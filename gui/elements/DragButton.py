#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from database import Logger, db_codes_output
from database.structure import db_structure
from database.structure.db_structure import *
from gui.dialogs.ShowLesson import ShowLesson
from gui.dialogs.EditLesson import EditLesson
logger = Logger()


color_start = '''border: 1px solid #8f8f91;
    border-radius: 6px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                      stop: 0 #{}, stop: 1 #{});
    min-width: 80px;'''

# need other colors, looks ugly
button_colors = {
    u'Unknown': ['ffffff', 'dddddd'],
    u'Лек': ['7777ff', '1111ff'],
    u'Прак': ['77ff77', '11ff11'],
    u'Лаб': ['ff7777', 'ff1111']
}

size_policy = QtGui.QSizePolicy(
    QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum
)


class DragButton(QtGui.QPushButton):
    def __init__(self, weekToolRef, view_args, draggable, time, *args):
        super(DragButton, self).__init__(*args)
        self.weekToolRef = weekToolRef
        self.draggable = draggable
        self.view_args = view_args
        self.setSizePolicy(size_policy)
        self.setAcceptDrops(self.draggable)
        self.set_time(time)

    def mousePressEvent(self, QMouseEvent):
        QtGui.QPushButton.mousePressEvent(self, QMouseEvent)

        if QMouseEvent.button() == QtCore.Qt.RightButton:
            # Pressing callback
            if self.draggable:
                if self.lesson.is_empty:
                    lesson = Lessons.create(self.parent().session, is_temp=True, **self.time)
                    self.edit_dial = EditLesson(lesson, self.parent().session, empty=True)
                else:
                    self.edit_dial = EditLesson(self.lesson, self.parent().session)
                if self.edit_dial.exec_() == EditLesson.Accepted:
                    if self.lesson.is_empty:
                        self.lesson = lesson
                    self.save_changes()
            else:
                if not self.lesson.is_empty:
                    self.show_dial = ShowLesson(self.lesson)
                    self.show_dial.exec_()
                else:
                    logger.debug('Are you kiddig me?')
                    logger.debug(self.lesson.id)
                    logger.debug(self.lesson.is_temp)
                    logger.debug(self.lesson.is_empty)
            logger.info('Pressed: %s' % self.__str__())

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton or not self.draggable:
            return

        mimeData = QtCore.QMimeData()
        mimeData.setText(self.text())

        # Grab the button to a pixmap to make it more fancy
        pixmap = QtGui.QPixmap.grabWidget(self)
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
        painter.end()

        # Make a QDrag with mime and pixmap
        drag = QtGui.QDrag(self)
        drag.setPixmap(pixmap)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos())

        # start the drag operation
        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            logger.debug('Moved: %s' % self)
        else:
            logger.debug('Copied: %s' % self)

    def dragMoveEvent(self, e):
        absp0 = self.weekToolRef.mapToGlobal(self.weekToolRef.tabButtons[0].pos())
        absp1 = self.weekToolRef.mapToGlobal(self.weekToolRef.tabButtons[1].pos())
        r0 = self.weekToolRef.tabButtons[0].rect()
        r1 = self.weekToolRef.tabButtons[1].rect()
        ucorrector = QtCore.QPoint(0, 30)
        dcorrector = QtCore.QPoint(0, 75)
        absr0 = QtCore.QRect(r0.topLeft()+absp0, r0.bottomRight()+absp0+dcorrector)
        absr1 = QtCore.QRect(r1.topLeft()+absp1-ucorrector, r1.bottomRight()+absp1)
        # curMousePos = self.weekToolRef.mapFromGlobal(QtGui.QCursor.pos())
        curMousePos = QtGui.QCursor.pos()
        if self.weekToolRef.currentIndex() == 0:
            if absr1.contains(curMousePos):
                self.weekToolRef.setCurrentIndex(1)
        else:
            if absr0.contains(curMousePos):
                self.weekToolRef.setCurrentIndex(0)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        if self != e.source():
            if e.keyboardModifiers() & QtCore.Qt.ShiftModifier:
                e.setDropAction(QtCore.Qt.CopyAction)
            else:
                # Perform swap:
                content = e.source().lesson
                e.source().set_lesson(self.lesson)
                self.set_lesson(content)

                # tell the QDrag we accepted it
                e.setDropAction(QtCore.Qt.MoveAction)
                e.accept()
        else:
            e.ignore()

    def set_lesson(self, lesson):
        self.lesson = lesson
        if self.draggable and not self.lesson.is_empty:
            if self.time != self.lesson.time():
                self.parent().edited = True
                Lessons.update(self.parent().session, main_id=self.lesson.id, **self.time)
        self.redraw()

    def set_bg_color(self, lesson_type):
        self.setStyleSheet(color_start.format(*button_colors[lesson_type]))

    def set_time(self, time):
        self.time = dict(
            id_week=db_structure.Lessons.week_ids[time[0]],
            id_week_day=db_structure.Lessons.day_ids[time[1]],
            id_lesson_time=db_structure.Lessons.time_ids[time[2]]
        )

    def before_close(self):
        if self.lesson.is_temp and not self.lesson.is_empty:
            ret = type(self.lesson).delete(self.parent().session, self.lesson.id)
            logger.debug(db_codes_output[ret])
            self.deleteLater()

    def save_changes(self):
        self.parent().edited = True
        self.redraw()

    def redraw(self):
        self.set_bg_color(self.lesson.lesson_plan.lesson_type.short_name)
        self.setText(self.lesson.to_table())
        # self.setText(self.lesson.to_table(self.view_args))

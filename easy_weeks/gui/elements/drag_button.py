#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from PyQt5 import QtWidgets
from PyQt5.QtCore import QMimeData, QPoint, QRect, Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QSizePolicy, QWidget
from PyQt5.QtGui import QColor, QCursor, QDrag, QPainter
from easy_weeks.database import Logger, structure, db_codes
from easy_weeks.database.structure import *
from easy_weeks.gui.dialogs import EditLesson
from easy_weeks.gui.dialogs import ShowLesson
from easy_weeks.database.select_table import check_table
logger = Logger()

color_start = '''
    border: 1px solid #8f8f91;
    color: #ffffff;
    font-weight: 500;
    background-color: {};
    min-width: 80px;
'''

button_colors = {
    'Unknown': QColor('white').name(),
    'Лек': QColor(0, 110, 179).name(),
    'Прак': QColor(0, 166, 152).name(),
    'Лаб': QColor(181, 95, 124).name(),
    'issue': QColor('red').name(),
}

size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


class DragButton(QPushButton):
    def __init__(self, weekToolRef, view_args, draggable, time, *args):
        super(DragButton, self).__init__(*args)
        self.weekToolRef = weekToolRef
        self.draggable = draggable
        self.view_args = view_args
        self.setSizePolicy(size_policy)
        self.setAcceptDrops(self.draggable)
        self.set_time(time)

    def mousePressEvent(self, QMouseEvent):
        QPushButton.mousePressEvent(self, QMouseEvent)

        if QMouseEvent.button() == Qt.RightButton:
            # Pressing callback
            if self.draggable:
                if self.lesson.is_empty:
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    lesson = Lessons.create(self.parent().session, is_temp=True, **self.time)
                    QApplication.restoreOverrideCursor()
                    self.edit_dial = EditLesson(lesson, self.parent().session, empty=True)
                else:
                    lesson = None
                    self.edit_dial = EditLesson(self.lesson, self.parent().session)
                result = self.edit_dial.exec_()
                if result == EditLesson.Accepted:
                    if self.edit_dial.deleting:
                        logger.debug('deleting')
                        if not self.lesson.is_empty:
                            self.lesson = Lessons.read(self.parent().session, id=1)[0]
                        self.save_changes()
                        return
                    logger.debug('accepted')
                    if self.lesson.is_empty:
                        self.lesson = lesson
                    self.save_changes()

                    overlay_dict = check_table(self.parent().session, only_temp=True)
                    if overlay_dict != db_codes['success']:
                        overlaying = sum(overlay_dict.values(), [])
                        if self.lesson.id != 1 and overlaying.count(self.lesson.row_time):
                            self.set_error()

            else:
                if not self.lesson.is_empty:
                    self.show_dial = ShowLesson(self.lesson)
                    self.show_dial.exec_()
                else:
                    pass
                    # logger.debug('Are you kiddig me?')
            # logger.info(f'Pressed: {self}')

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton or not self.draggable:
            return

        mimeData = QMimeData()
        mimeData.setText(self.text())

        # Grab the button to a pixmap to make it more fancy
        pixmap = QWidget.grab(self)
        painter = QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QColor(0, 0, 0, 127))
        painter.end()

        # Make a QDrag with mime and pixmap
        drag = QDrag(self)
        drag.setPixmap(pixmap)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos())

        # start the drag operation
        if drag.exec_(Qt.CopyAction | Qt.MoveAction) == Qt.MoveAction:
            logger.debug('Moved: %s' % self)
        else:
            logger.debug('Copied: %s' % self)

    def dragMoveEvent(self, e):
        abs_x = self.weekToolRef.mapToGlobal(self.weekToolRef.tabButtons[0].pos())
        abs_y = self.weekToolRef.mapToGlobal(self.weekToolRef.tabButtons[1].pos())
        r0 = self.weekToolRef.tabButtons[0].rect()
        r1 = self.weekToolRef.tabButtons[1].rect()
        ucorrector = QPoint(0, 30)
        dcorrector = QPoint(0, 75)
        absr0 = QRect(r0.topLeft() + abs_x, r0.bottomRight() + abs_x + dcorrector)
        absr1 = QRect(r1.topLeft() + abs_y - ucorrector, r1.bottomRight() + abs_y)

        curMousePos = QCursor.pos()
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
            if e.keyboardModifiers() & Qt.ShiftModifier:
                # Perform swap:
                content = e.source().lesson
                # e.source().set_lesson(self.lesson)
                self.set_lesson(content.make_temp(self.parent().session, self.time))

                # tell the QDrag we accepted it
                e.setDropAction(Qt.CopyAction)
                self.save_changes()
                e.accept()
            else:
                # Perform swap:
                content = e.source().lesson
                e.source().set_lesson(self.lesson)
                self.set_lesson(content)

                # tell the QDrag we accepted it
                e.setDropAction(Qt.MoveAction)
                e.accept()
            # QApplication.setOverrideCursor(Qt.WaitCursor)
            overlay_dict = check_table(self.parent().session, only_temp=True)
            # QApplication.restoreOverrideCursor()
            self.redraw()
            e.source().redraw()
            if overlay_dict != db_codes['success']:
                overlaying = sum(overlay_dict.values(), [])
                if e.source().lesson.id != 1 and overlaying.count(e.source().lesson.row_time):
                    e.source().set_error()
                if self.lesson.id != 1 and overlaying.count(self.lesson.row_time):
                    self.set_error()
        else:
            e.ignore()

    def set_lesson(self, lesson):
        self.lesson = lesson
        if self.draggable and not self.lesson.is_empty:
            if self.time != self.lesson.time():
                self.parent().edited = True
                Lessons.update(self.parent().session, main_id=self.lesson.id, **self.time)
        self.redraw()

    def set_error(self):
        self.set_bg_color(u'issue')

    def set_bg_color(self, lesson_type):
        self.setStyleSheet(color_start.format(button_colors[lesson_type]))

    def set_time(self, time):
        self.time = {
            'id_week': structure.Lessons.week_ids[time[0]],
            'id_week_day': structure.Lessons.day_ids[time[1]],
            'id_lesson_time': structure.Lessons.time_ids[time[2]],
        }

    def before_close(self):
        if self.lesson.is_temp and not self.lesson.is_empty:
            # ret = type(self.lesson).delete(self.parent().session, self.lesson.id)
            # logger.debug(f'Button deleted:? {db_codes_output[ret]}')
            self.deleteLater()

    def save_changes(self):
        self.parent().edited = True
        self.redraw()

    def redraw(self):
        self.set_bg_color(self.lesson.lesson_plan.lesson_type.short_name)
        self.setText(self.lesson.to_table())
        # self.setText(self.lesson.to_table(self.view_args))

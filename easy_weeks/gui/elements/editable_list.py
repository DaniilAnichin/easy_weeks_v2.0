#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QDialog, QListWidget, QPushButton, QVBoxLayout
from easy_weeks.database import Logger
from easy_weeks.gui.components import CompleterCombo
logger = Logger()


class EditableList(QListWidget):
    def __init__(self, parent, items_list, suggested_list, inner_name, sort_key=str):
        super(EditableList, self).__init__(parent)
        self.sort_key = sort_key
        self.view_items = items_list[:]
        self.view_items.sort(key=self.sort_key)
        self.suggested_items = suggested_list[:]
        self.suggested_items.sort(key=self.sort_key)
        self.addItems([self.sort_key(item) for item in self.view_items])
        self.blocked = False
        setattr(self.parent(), inner_name, self)

    def mousePressEvent(self, QMouseEvent):
        QListWidget.mousePressEvent(self, QMouseEvent)

        if self.blocked:
            # Pause to prevent multiple deleting
            return

        if not (QMouseEvent.modifiers() & Qt.ShiftModifier):
            # Only Shift click performing
            return

        if QMouseEvent.button() == Qt.RightButton:
            # Right button for delete
            index = self.row(self.currentItem())
            self.takeItem(index)
            self.blocked = True
            self.time = QTimer.singleShot(500, self.unblock)
        elif QMouseEvent.button() == Qt.LeftButton:
            # Left button to add
            self.show_completer()

    def unblock(self):
        self.blocked = False

    def addItem(self, *args):
        logger.debug(args)

        if args[0] not in self.suggested_items:
            logger.info('Wrong item')
            return

        self.view_items += [args[0]]
        super(EditableList, self).addItem(self.sort_key(args[0]))
        logger.info(f'Added item "{self.sort_key(args[0])}"')

    def addItemByIndex(self):
        p_int = self.completer.currentIndex()
        logger.debug(self.sort_key(p_int))

        if p_int >= len(self.suggested_items):
            logger.info('Wrong item')
            return

        item = self.completer_items[p_int]
        self.view_items += [item]
        self.view_items.sort(key=self.sort_key)
        index = self.view_items.index(item)
        self.insertItem(index, self.sort_key(item))
        logger.info(f'Added item "{self.sort_key(item)}"')

    def takeItem(self, p_int):
        logger.info(f'Deleted item "{self.sort_key(self.view_items[p_int])}"')
        self.view_items.pop(p_int)
        super(EditableList, self).takeItem(p_int)

    def show_completer(self):
        # Create completer combobox:
        self.completer = CompleterCombo(self)
        self.completer_items = list(set(self.suggested_items) - set(self.view_items))
        self.completer_items.sort(key=self.sort_key)
        self.completer.addItems([self.sort_key(item) for item in self.completer_items])

        # Create modal window
        self.dialog = QDialog()
        self.dialog.setModal(True)

        # Create button, connect
        submit = QPushButton('Додати')
        submit.clicked.connect(self.addItemByIndex)
        submit.clicked.connect(self.dialog.close)

        # Add to layout
        vbox = QVBoxLayout(self.dialog)
        vbox.addWidget(self.completer, 1)
        vbox.addWidget(submit, 1)

        # show
        logger.info('Raised completer window')
        self.dialog.show()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from PyQt5 import QtWidgets
from easy_weeks.database import Logger
from easy_weeks.gui.elements.CompleterCombo import CompleterCombo
from easy_weeks.gui.elements.EditableList import EditableList
logger = Logger()


class WeeksDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(WeeksDialog, self).__init__(*args, **kwargs)
        self.setModal(True)
        self.vbox = QtWidgets.QVBoxLayout(self)

    @staticmethod
    def make_text(element):
        if isinstance(element, list):
            this_text = ', '.join(str(item) for item in element)
        else:
            this_text = str(element)
        return this_text

    def make_button(self, data, callback, *args, **kwargs):
        this_button = QtWidgets.QPushButton(self.make_text(data))
        this_button.clicked.connect(partial(callback, *args, **kwargs))
        return this_button

    def make_combo(self, choice_list, selected, name, sort_key):
        combo = CompleterCombo()
        combo.items = choice_list[:]
        combo.items.sort(key=sort_key)
        combo.addItems([sort_key(item) for item in combo.items])
        setattr(self, name, combo)
        if selected:
            combo.setCurrentIndex(combo.items.index(selected))
        # logger.info('Added combobox with name "%s"' % name)
        return combo

    def make_list(self, values_list, choice_list, name):
        items_list = EditableList(self, values_list, choice_list, name)
        # logger.info('Added list widget with name "%s"' % name)
        return items_list

    def set_pair(self, first_data, second_data):
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel(self.make_text(first_data)), 1)
        hbox.addWidget(QtWidgets.QLabel(self.make_text(second_data)), 1)
        self.vbox.addLayout(hbox, 1)

    def set_combo_pair(self, first_data, second_data, name, key=str, selected=None):
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel(self.make_text(first_data)), 1)
        hbox.addWidget(self.make_combo(second_data, selected, name, key), 1)
        self.vbox.addLayout(hbox, 1)

    def set_list_pair(self, first_data, second_data, third_data, name):
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(QtWidgets.QLabel(self.make_text(first_data)), 1)
        hbox.addWidget(self.make_list(second_data, third_data, name), 1)
        self.vbox.addLayout(hbox, 1)

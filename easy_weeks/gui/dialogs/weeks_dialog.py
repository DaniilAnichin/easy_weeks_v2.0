#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from easy_weeks.database import Logger
from easy_weeks.gui.mixins.combo_mixin import ComboMixin
logger = Logger()


class WeeksDialog(ComboMixin, QDialog):
    def __init__(self, *args, **kwargs):
        super(WeeksDialog, self).__init__(*args, **kwargs)
        self.setModal(True)
        self.vbox = QVBoxLayout(self)

    @staticmethod
    def make_text(element):
        if isinstance(element, list):
            this_text = ', '.join(str(item) for item in element)
        else:
            this_text = str(element)
        return this_text

    def make_button(self, data, callback, *args, **kwargs):
        this_button = QPushButton(self.make_text(data))
        this_button.clicked.connect(partial(callback, *args, **kwargs))
        return this_button

    def make_list(self, values_list, choice_list, name):
        from easy_weeks.gui.elements import EditableList
        items_list = EditableList(self, values_list, choice_list, name)
        return items_list

    def set_pair(self, first_data, second_data):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.make_text(first_data)), 1)
        hbox.addWidget(QLabel(self.make_text(second_data)), 1)
        self.vbox.addLayout(hbox, 1)

    def set_combo_pair(self, first_data, second_data, name, key=str, selected=None):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.make_text(first_data)), 1)
        hbox.addWidget(self.make_combo(second_data, selected, name, key), 1)
        self.vbox.addLayout(hbox, 1)

    def set_list_pair(self, first_data, second_data, third_data, name):
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(self.make_text(first_data)), 1)
        hbox.addWidget(self.make_list(second_data, third_data, name), 1)
        self.vbox.addLayout(hbox, 1)

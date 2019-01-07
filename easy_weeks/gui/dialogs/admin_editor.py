#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QSpinBox, QCheckBox, QLineEdit
from easy_weeks.database import Logger, structure
from easy_weeks.gui.dialogs.weeks_dialog import WeeksDialog
from easy_weeks.gui.translate import translates


logger = Logger()
inner_columns = {'id', 'row_time', 'param_checker', 'additional_stuff', 'split_groups', 'needed_stuff'}
time_classes = {structure.WeekDays, structure.Weeks, structure.LessonTimes}


def safe_column(column_name, cls=None):
    return not (
        column_name.startswith('id_')
        or
        column_name.startswith('is_')
        or
        column_name in inner_columns
        or (
            cls in time_classes
            and
            column_name == 'lessons'
        )
    )


class AdminEditor(WeeksDialog):
    def __init__(self, element, session, empty=False, *args, **kwargs):
        super(AdminEditor, self).__init__(*args, **kwargs)
        self.session = session
        logger.debug('Element is %s' % element)
        self.empty = empty
        self.cls = element if empty else type(element)
        self.cls_name = self.cls.__name__
        if self.cls_name not in structure.tables:
            logger.debug('Wrong params')
            return

        self.example_element = self.cls.read(self.session, id=2 if self.cls in time_classes else 1)[0]
        self.element = self.cls.read(self.session, id=1)[0] if empty else element
        self.fields = [
            column
            for column
            in self.cls.fields()
            if safe_column(column, self.cls)
        ]

        logger.debug('All right')
        for column in self.fields:
            self.make_pair(column)

        self.vbox.addWidget(self.make_button('Підтвердити', self.accept))
        self.setWindowTitle('Створення елементу' if self.empty else 'Редагування елементу')

    def make_pair(self, param):
        exp_result = getattr(self.example_element, param)
        if isinstance(exp_result, list):
            self.default_list_pair(param)
        elif isinstance(exp_result, structure.Base):
            self.default_combo_pair(param)
        elif isinstance(exp_result, bool):
            self.default_bool_pair(param)
        elif isinstance(exp_result, int):
            self.default_int_pair(param)
        elif isinstance(exp_result, str):
            self.default_str_pair(param)
        else:
            logger.info(f'{param} is {type(exp_result)}')

    def get_pair(self, param):
        exp_result = getattr(self.example_element, param)
        if isinstance(exp_result, list):
            return getattr(self, param).view_items
        elif isinstance(exp_result, structure.Base):
            return getattr(self, param).items[getattr(self, param).currentIndex()]
        elif isinstance(exp_result, bool):
            return getattr(self, param).isChecked()
        elif isinstance(exp_result, int):
            return int(getattr(self, param).value())
        elif isinstance(exp_result, str):
            return str(getattr(self, param).text())
        else:
            logger.info(f'{param} is {type(exp_result)}')

    def default_combo_pair(self, param):
        cls = type(getattr(self.example_element, param))
        label = cls.translated
        values = cls.read(self.session, all_=True)
        value = None if self.empty else getattr(self.element, param)
        self.set_combo_pair(label, values, param, selected=value)

    def default_list_pair(self, param):
        cls = type(getattr(self.example_element, param)[0])
        label = cls.translated
        values = cls.read(self.session, all_=True)
        selected_values = [] if self.empty else getattr(self.element, param)
        self.set_list_pair(label, selected_values, values, param)

    def default_int_pair(self, param):
        spin = QSpinBox()
        spin.setRange(0, 1000000)
        if not self.empty:
            spin.setValue(getattr(self.element, param))
        setattr(self, param, spin)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(translates.get(param, param)), 1)
        hbox.addWidget(spin, 1)
        self.vbox.addLayout(hbox, 1)

    def default_str_pair(self, param):
        line = QLineEdit()
        if not self.empty:
            line.setText(getattr(self.element, param))
        setattr(self, param, line)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(translates.get(param, param)), 1)
        hbox.addWidget(line, 1)
        self.vbox.addLayout(hbox, 1)

    def default_bool_pair(self, param):
        check = QCheckBox()
        if not self.empty:
            check.setChecked(getattr(self.element, param))
        setattr(self, param, check)

        hbox = QHBoxLayout()
        hbox.addWidget(QLabel(translates.get(param, param)), 1)
        hbox.addWidget(check, 1)
        self.vbox.addLayout(hbox, 1)

    def accept(self):
        logger.debug('Here is editor saving')
        super(AdminEditor, self).accept()

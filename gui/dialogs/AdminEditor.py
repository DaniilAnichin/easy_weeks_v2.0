#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
from database import Logger
from database.structure import db_structure
from gui.dialogs.WeeksDialog import WeeksDialog
from gui.translate import fromUtf8
logger = Logger()


class AdminEditor(WeeksDialog):
    def __init__(self, element, session, empty=False, *args, **kwargs):
        super(AdminEditor, self).__init__(*args, **kwargs)
        self.session = session
        logger.debug('Element is %s' % element)
        self.empty = empty
        self.cls = element if empty else type(element)
        self.cls_name = self.cls.__name__
        self.example_element = self.cls.read(self.session, id=1)[0]
        self.element = self.cls.read(self.session, id=1)[0] if empty else element

        if self.cls_name not in db_structure.__all__:
            logger.debug('Wrong params')
        else:
            logger.debug('All right')
            for column in self.cls.fields():
                if not (column.startswith('id_') or column == 'id' or column == 'row_time'):
                    self.make_pair(column)
            self.vbox.addWidget(self.make_button(fromUtf8('Підтвердити'), self.accept))
            if self.empty:
                self.setWindowTitle(fromUtf8('Створення елементу'))
            else:
                self.setWindowTitle(fromUtf8('Редагування елементу'))

    def make_pair(self, param):
        exp_result = getattr(self.example_element, param)
        if isinstance(exp_result, list):
            self.default_list_pair(param)
        elif isinstance(exp_result, db_structure.Base):
            self.default_combo_pair(param)
        elif isinstance(exp_result, int):
            self.default_int_pair(param)
        elif isinstance(exp_result, (str, unicode, QtCore.QString)):
            self.default_str_pair(param)
        elif isinstance(exp_result, bool):
            self.default_bool_pair(param)
        else:
            logger.info("What is this - %s, man?" % exp_result)
            logger.info("It is %s" % type(exp_result))

    def get_pair(self, param):
        exp_result = getattr(self.example_element, param)
        if isinstance(exp_result, list):
            return getattr(self, param).view_items
        elif isinstance(exp_result, db_structure.Base):
            return getattr(self, param).items[getattr(self, param).currentIndex()]
        elif isinstance(exp_result, int):
            return int(getattr(self, param).value())
        elif isinstance(exp_result, (str, unicode, QtCore.QString)):
            return unicode(getattr(self, param).text())
        elif isinstance(exp_result, bool):
            return getattr(self, param).isChecked()
        else:
            logger.info("What is this - %s, man?" % exp_result)
            logger.info("It is %s" % type(exp_result))

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
        spin = QtGui.QSpinBox()
        spin.setRange(0, 1000000)
        if not self.empty:
            spin.setValue(getattr(self.element, param))
        setattr(self, param, spin)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(param), 1)
        hbox.addWidget(spin, 1)
        self.vbox.addLayout(hbox, 1)

    def default_str_pair(self, param):
        line = QtGui.QLineEdit()
        if not self.empty:
            line.setText(getattr(self.element, param))
        setattr(self, param, line)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(param), 1)
        hbox.addWidget(line, 1)
        self.vbox.addLayout(hbox, 1)

    def default_bool_pair(self, param):
        check = QtGui.QCheckBox()
        if not self.empty:
            check.setChecked(getattr(self.element, param))
        setattr(self, param, check)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(QtGui.QLabel(param), 1)
        hbox.addWidget(check, 1)
        self.vbox.addLayout(hbox, 1)

    def accept(self):
        logger.debug('Here must be editor saving')
        logger.debug('Values are:')
        for column in self.cls.fields():
            if not (column.startswith('id_') or column == 'id' or column == 'row_time'):
                logger.debug('%s - "%s"' % (column, self.make_text(self.get_pair(column))))
        super(AdminEditor, self).accept()

#!/usr/bin/python
# -*- coding: utf-8 -*-
from database import Logger
from database.structure import Teachers, Groups, Rooms
from gui.dialogs.WeeksDialog import WeeksDialog
from gui.translate import fromUtf8
logger = Logger()


class TableChoosingDialog(WeeksDialog):
    def __init__(self, session, *args, **kwargs):
        super(TableChoosingDialog, self).__init__(*args, **kwargs)
        self.session = session
        self.data_types = [Teachers, Groups, Rooms]
        self.set_combo_pair(fromUtf8('Для кого розклад: '), self.data_types, 'type', lambda a: a.translated)
        self.type.currentIndexChanged.connect(self.set_list)
        self.set_combo_pair(fromUtf8('Назва / Ім\'я: '), [], 'data_choice')
        self.set_list()
        self.vbox.addWidget(self.make_button(fromUtf8('Підтвердити'), self.accept))
        self.setWindowTitle(fromUtf8('Вибір розкладу'))

    def set_list(self):
        self.data_type = self.type.items[self.type.currentIndex()]
        self.values = self.data_type.read(self.session, all_=True)[:]
        self.values.sort(key=lambda a: unicode(a))
        self.data_choice.clear()
        self.data_choice.addItems([unicode(item) for item in self.values])

    def accept(self):
        self.data_type = self.data_type.__tablename__
        self.data_id = self.values[self.data_choice.currentIndex()].id
        # Add data to statusbar
        super(TableChoosingDialog, self).accept()

#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from database import Logger, db_codes, db_codes_output, structure
from gui.dialogs.AdminEditor import AdminEditor
from gui.dialogs.RUSureDelete import RUSureDelete
from gui.dialogs.InfoDialog import InfoDialog
from gui.elements.CompleterCombo import CompleterCombo
from gui.translate import fromUtf8
logger = Logger()


class AdminTab(QtGui.QWidget):
    def __init__(self, parent, session):
        super(AdminTab, self).__init__(parent)
        self.session = session
        self.setObjectName('admin_tab')

        self.vbox = QtGui.QVBoxLayout(self)
        self.hbox = QtGui.QHBoxLayout()

        self.objects = CompleterCombo(self)
        self.objects.items = []
        self.objects.currentIndexChanged.connect(self.set_list)
        self.hbox.addWidget(self.objects)

        spacer = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum
        )
        self.hbox.addItem(spacer)

        self.addButton = QtGui.QPushButton(self)
        self.addButton.clicked.connect(self.show_add)
        self.hbox.addWidget(self.addButton)

        self.deleteButton = QtGui.QPushButton(self)
        self.deleteButton.clicked.connect(self.show_delete)
        self.hbox.addWidget(self.deleteButton)

        self.editButton = QtGui.QPushButton(self)
        self.editButton.clicked.connect(self.show_edit)
        self.hbox.addWidget(self.editButton)

        self.vbox.addLayout(self.hbox)

        self.items_list = QtGui.QListWidget(self)
        self.view_items = []
        self.vbox.addWidget(self.items_list)
        self.translateUI()
        self.set_objects()

    def translateUI(self):
        self.addButton.setText(fromUtf8('Додати'))
        self.deleteButton.setText(fromUtf8('Видалити'))
        self.editButton.setText(fromUtf8('Редагувати'))

    def set_objects(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(3))
        self.objects.items = [getattr(structure, item) for item in structure.__all__]
        for item in self.objects.items:
            columns = item.columns()
            if len(columns) == 2 and columns[0][:3] == columns[1][:3] == 'id_':
                self.objects.items.pop(self.objects.items.index(item))

        self.objects.items.sort(key=lambda a: a.translated)
        self.objects.addItems([item.translated for item in self.objects.items])
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(0))

    def set_list(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(3))
        cls = self.objects.items[self.objects.currentIndex()]
        logger.info('Setting admin list for %s' % cls.__name__)
        self.items_list.clear()
        self.view_items = cls.read(self.session, all_=True)
        self.view_items.sort(key=unicode)
        self.items_list.addItems([unicode(item) for item in self.view_items])
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(0))

    def show_add(self):
        cls = self.objects.items[self.objects.currentIndex()]
        logger.info('Running create dialog for %s' % cls.__name__)

        self.editor = AdminEditor(cls, self.session, empty=True)
        if self.editor.exec_() == AdminEditor.Accepted:
            logger.info('Adding accepted')
            fields = self.editor.fields
            values = {key: self.editor.get_pair(key) for key in fields}
            result = cls.create(self.session, **values)
            logger.debug('Result: "%s"' % unicode(result))
            self.view_items.append(result)
            self.view_items.sort(key=unicode)
            new_index = self.view_items.index(result)
            self.items_list.insertItem(new_index, unicode(result))

    def show_delete(self):
        index = self.items_list.row(self.items_list.currentItem())
        if index < 0 or index > self.view_items.__len__():
            return
        element = self.view_items[index]
        cls = type(element)
        self.warning = RUSureDelete(element)
        if self.warning.exec_() == QtGui.QMessageBox.Yes:
            logger.info('Item %s deleted' % unicode(self.items_list.currentItem().text()))
            self.items_list.takeItem(index)
            self.view_items.pop(index)
            logger.info(db_codes_output[cls.delete(self.session, main_id=element.id)])

    def show_edit(self):
        index = self.items_list.row(self.items_list.currentItem())
        if index < 0 or index > self.view_items.__len__():
            return
        element = self.view_items[index]
        logger.info('Running edit dialog for %s' % unicode(element))

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(3))
        self.editor = AdminEditor(element, self.session)
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(0))
        if self.editor.exec_() == AdminEditor.Accepted:
            logger.info('Editing accepted')
            fields = self.editor.fields
            values = {key: self.editor.get_pair(key) for key in fields}
            result = type(element).update(
                self.session, main_id=element.id, **values
            )
            logger.debug(db_codes_output[result])
            if result == db_codes['exists']:
                self.warning = InfoDialog(fromUtf8(
                    'Збереження не вдалось: елемент вже існує'
                ))
            self.view_items.sort(key=unicode)
            new_index = self.view_items.index(element)
            self.items_list.takeItem(index)
            self.items_list.insertItem(new_index, unicode(element))

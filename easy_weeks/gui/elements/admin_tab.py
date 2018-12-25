#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from easy_weeks.database import Logger, db_codes, db_codes_output, structure
from easy_weeks.gui.dialogs import AdminEditor, RUSureDelete, InfoDialog
from easy_weeks.gui.elements.completer_combo import CompleterCombo
logger = Logger()


class AdminTab(QtWidgets.QWidget):
    def __init__(self, parent, session):
        super(AdminTab, self).__init__(parent)
        self.session = session
        self.setObjectName('admin_tab')

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.hbox = QtWidgets.QHBoxLayout()

        self.objects = CompleterCombo(self)
        self.objects.items = []
        self.objects.currentIndexChanged.connect(self.set_list)
        self.hbox.addWidget(self.objects)

        self.search = QtWidgets.QLineEdit()
        self.search.textChanged.connect(self.set_search)
        self.hbox.addWidget(self.search)

        spacer = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.hbox.addItem(spacer)

        self.addButton = QtWidgets.QPushButton(self)
        self.addButton.clicked.connect(self.show_add)
        self.hbox.addWidget(self.addButton)

        self.deleteButton = QtWidgets.QPushButton(self)
        self.deleteButton.clicked.connect(self.show_delete)
        self.hbox.addWidget(self.deleteButton)

        self.editButton = QtWidgets.QPushButton(self)
        self.editButton.clicked.connect(self.show_edit)
        self.hbox.addWidget(self.editButton)

        self.vbox.addLayout(self.hbox)

        self.items_list = QtWidgets.QListWidget(self)
        self.database_items = []
        self.view_items = []
        self.vbox.addWidget(self.items_list)
        self.translateUI()
        self.set_objects()

    def translateUI(self):
        self.addButton.setText('Додати')
        self.deleteButton.setText('Видалити')
        self.editButton.setText('Редагувати')

    def set_objects(self):
        try:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            self.objects.items = [getattr(structure, item) for item in structure.tables]
            for item in self.objects.items:
                columns = item.columns()
                if len(columns) == 2 and columns[0][:3] == columns[1][:3] == 'id_':
                    self.objects.items.pop(self.objects.items.index(item))

            self.objects.items.sort(key=lambda a: a.translated)
            self.objects.addItems([item.translated for item in self.objects.items])
            QtWidgets.QApplication.restoreOverrideCursor()
        except Exception as e:
            logger.error(e)
            QtWidgets.QApplication.restoreOverrideCursor()

    def set_list(self):
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        cls = self.objects.items[self.objects.currentIndex()]
        logger.info('Setting admin list for %s' % cls.__name__)
        self.items_list.clear()
        self.database_items = cls.read(self.session, all_=True)
        self.database_items.sort(key=str)
        self.view_items = self.database_items[:]
        self.items_list.addItems([str(item) for item in self.view_items])
        QtWidgets.QApplication.restoreOverrideCursor()

    def show_add(self):
        cls = self.objects.items[self.objects.currentIndex()]
        logger.info('Running create dialog for %s' % cls.__name__)

        self.editor = AdminEditor(cls, self.session, empty=True)
        if self.editor.exec_() == AdminEditor.Accepted:
            logger.info('Adding accepted')
            fields = self.editor.fields
            values = {key: self.editor.get_pair(key) for key in fields}
            result = cls.create(self.session, **values)
            logger.debug('Result: "%s"' % str(result))
            self.database_items.append(result)
            self.database_items.sort(key=str)
            self.set_search()
            new_index = self.view_items.index(result)
            self.items_list.insertItem(new_index, str(result))

    def show_delete(self):
        index = self.items_list.row(self.items_list.currentItem())
        if index < 0 or index > self.view_items.__len__():
            return
        element = self.view_items[index]
        cls = type(element)
        self.warning = RUSureDelete(element)
        if self.warning.exec_() == QtWidgets.QMessageBox.Yes:
            logger.info('Item %s deleted' % str(self.items_list.currentItem().text()))
            self.items_list.takeItem(index)
            self.database_items.pop(index)
            logger.info(db_codes_output[cls.delete(self.session, main_id=element.id)])

    def show_edit(self):
        index = self.items_list.row(self.items_list.currentItem())
        if index < 0 or index > self.view_items.__len__():
            return
        element = self.view_items[index]
        logger.info('Running edit dialog for %s' % str(element))

        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.editor = AdminEditor(element, self.session)
        QtWidgets.QApplication.restoreOverrideCursor()
        if self.editor.exec_() == AdminEditor.Accepted:
            logger.info('Editing accepted')
            fields = self.editor.fields
            values = {key: self.editor.get_pair(key) for key in fields}
            result = type(element).update(
                self.session, main_id=element.id, **values
            )
            logger.debug(db_codes_output[result])
            if result != db_codes['success']:
                InfoDialog('Збереження не вдалось').show()
            self.database_items.sort(key=str)
            self.set_search()

    def set_search(self):
        text = str(self.search.text())
        self.items_list.clear()
        self.view_items = filter(lambda x: text in str(x), self.database_items)
        self.items_list.addItems([str(item) for item in self.view_items])

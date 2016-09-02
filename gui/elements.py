#!/usr/bin/python
# -*- coding: utf-8 -*-
from functools import partial
from database import Logger, db_codes_output
from database.structure import db_structure
from PyQt4 import QtGui, QtCore
from gui.translate import fromUtf8

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


class EditableList(QtGui.QListWidget):
    def __init__(self, parent, items_list, suggested_list, inner_name, sort_key=lambda a: unicode(a)):
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
        QtGui.QListWidget.mousePressEvent(self, QMouseEvent)

        if self.blocked:
            # Pause to prevent multiple deleting
            return

        if not (QMouseEvent.modifiers() & QtCore.Qt.ShiftModifier):
            # Only Shift click performing
            return

        if QMouseEvent.button() == QtCore.Qt.RightButton:
            # Right button for delete
            index = self.row(self.currentItem())
            self.takeItem(index)
            self.blocked = True
            self.time = QtCore.QTimer.singleShot(500, self.unblock)
        elif QMouseEvent.button() == QtCore.Qt.LeftButton:
            # Left button to add
            self.show_completer()

    def unblock(self):
        self.blocked = False

    def addItem(self, *__args):
        logger.debug(__args)

        if __args[0] not in self.suggested_items:
            logger.info('Wrong item')
            return

        self.view_items += [__args[0]]
        # self.view_items.sort(key=lambda a: unicode(a))
        # index = self.view_items.index(__args[0])
        # self.insertItem(index, unicode(__args[0]))
        super(EditableList, self).addItem(self.sort_key(__args[0]))
        logger.info('Added item "%s"' % self.sort_key(__args[0]))

    def addItemByIndex(self):
        p_int = self.completer.currentIndex()
        logger.debug(self.sort_key(p_int))

        if p_int >= len(self.suggested_items):
            logger.info('Wrong item')
            return

        item = self.completer_items[p_int]
        # self.view_items += [__args[0]]
        self.view_items += [item]
        self.view_items.sort(key=self.sort_key)
        index = self.view_items.index(item)
        self.insertItem(index, self.sort_key(item))
        # super(EditableList, self).addItem(self.sort_key(item))
        logger.info('Added item "%s"' % self.sort_key(item))

    def takeItem(self, p_int):
        logger.info('Deleted item "%s"' % self.sort_key(self.view_items[p_int]))
        self.view_items.pop(p_int)
        super(EditableList, self).takeItem(p_int)

    def show_completer(self):
        # Create completer combobox:
        self.completer = CompleterCombo(self)
        self.completer_items = list(set(self.suggested_items) - set(self.view_items))
        self.completer_items.sort(key=self.sort_key)
        self.completer.addItems([self.sort_key(item) for item in self.completer_items])

        # Create modal window
        self.dialog = QtGui.QDialog()
        self.dialog.setModal(True)

        # Create button, connect
        submit = QtGui.QPushButton(fromUtf8('Додати'))
        # logger.debug(completer.currentText())
        submit.clicked.connect(self.addItemByIndex)
        submit.clicked.connect(self.dialog.close)

        # Add to layout
        vbox = QtGui.QVBoxLayout(self.dialog)
        vbox.addWidget(self.completer, 1)
        vbox.addWidget(submit, 1)

        # show
        logger.info('Raised completer window')
        self.dialog.show()


class CompleterCombo(QtGui.QComboBox):
    def __init__(self, parent=None):
        super(CompleterCombo, self).__init__(parent)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setEditable(True)

        # add a filter model to filter matching items
        self.pFilterModel = QtGui.QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        # add a completer, which uses the filter model
        self.completer = QtGui.QCompleter(self.pFilterModel, self)
        # always show all (filtered) completions
        self.completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        self.setCompleter(self.completer)

        # connect signals
        self.lineEdit().textEdited[unicode].connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.on_completer_activated)

    # on selection of an item from the completer, select the corresponding item from combobox
    def on_completer_activated(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)
            # self.activated[str].emit(self.itemText(index))

    # on model change, update the models of the filter and completer as well
    def setModel(self, model):
        super(CompleterCombo, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    # on model column change, update the model column of the filter and completer as well
    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(CompleterCombo, self).setModelColumn(column)


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
            from gui.dialogs import ShowLesson, EditLesson

            if self.draggable:
                if self.lesson.is_empty:
                    return
                # self.edit_dial = EditLesson(self.lesson, self.parent().session, time=False)
                self.edit_dial = EditLesson(self.lesson, self.parent().session)
                if self.edit_dial.exec_() == EditLesson.Accepted:
                    self.save_changes()
            else:
                if not self.lesson.is_empty:
                    self.show_dial = ShowLesson(self.lesson)
                    self.show_dial.exec_()
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
        dcorrector = QtCore.QPoint(0, 60)
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
        if lesson.is_temp or lesson.is_empty or not self.draggable:
            self.lesson = lesson
        else:
            self.lesson = lesson.make_temp(self.parent().session)
        self.set_bg_color(self.lesson.lesson_plan.lesson_type.short_name)
        self.setText(self.lesson.to_table(self.view_args))
        if self.draggable and not self.lesson.is_empty:
            type(self.lesson).update(self.parent().session, main_id=self.lesson.id, **self.time)
        # self.lesson.set_time(self.time)

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
            self.deleteLater()

    def save_changes(self):
        logger.debug('Here must be editor saving - button')
        self.parent().edited = True


class ButtonGrid(QtGui.QGridLayout):
    def __init__(self, parent, weekToolRef):
        super(ButtonGrid, self).__init__(parent)
        self.weekToolRef = weekToolRef
        # self.parent_name = parent.objectName()

    def set_table(self, lesson_set, view_args, week, drag_enabled=False):
        for i in range(len(lesson_set)):
            for j in range(len(lesson_set[i])):
                time = [week, i, j]
                lesson_button = DragButton(self.weekToolRef, view_args, drag_enabled, time)
                self.addWidget(lesson_button, j, i, 1, 1)
                lesson_button.set_lesson(lesson_set[i][j])


# class TempGrid(QtGui.QGridLayout):
#     def __init__(self, parent, table_height=5):
#         super(TempGrid, self).__init__(parent)
#         self.table_height = table_height
#         self.buttons = []
#
#         button = DragButton(parent)
#         self.buttons.append(button)
#         self.addWidget(button, 0, 0, 1, 1)
#
#         self.translateUI()
#
#     def add_button(self):
#         button = DragButton(self.parent(), self.empty_text)
#         self.buttons.append(button)
#         x = (len(self.buttons) + 1) / self.table_height
#         y = (len(self.buttons) + 1) % self.table_height
#         self.addWidget(button, x, y, 1, 1)
#
#     def remove_button(self, button):
#         self.buttons.remove(button)
#         self.removeWidget(button)
#         del button
#
#     def translateUI(self):
#         self.empty_text = fromUtf8('Перетягніть\nзаняття сюди')
#         self.buttons[-1].setText(self.empty_text)


class WeekTool(QtGui.QToolBox):
    def __init__(self, parent, session, *args, **kwargs):
        super(WeekTool, self).__init__(parent, *args, **kwargs)
        self.session = session
        self.initUI()

    def initUI(self):
        self.first_panel = QtGui.QWidget(self)
        self.first_panel.acceptDrops()
        self.first_panel.session = self.session
        self.addItem(self.first_panel, '')
        self.first_table = ButtonGrid(self.first_panel, self)

        self.second_panel = QtGui.QWidget(self)
        self.second_panel.acceptDrops()
        self.second_panel.session = self.session
        self.addItem(self.second_panel, '')
        self.second_table = ButtonGrid(self.second_panel, self)

        self.set_edited(False)

        self.setMouseTracking(True)
        self.tabButtons = self.findChildren(QtGui.QAbstractButton)
        for button in self.tabButtons:
            button.setToolTip(QtCore.QString(unicode(self.mapFromParent(button.pos()))))
            button.setMouseTracking(True)

        self.translateUI()

    def set_table(self, lesson_set, view_args, drag_enabled=False):
        if self.check_and_clear_table():
            return 1
        self.set_edited(False)
        self.first_table.set_table(lesson_set[0], view_args, 0, drag_enabled)
        self.second_table.set_table(lesson_set[1], view_args, 1, drag_enabled)
        return 0

    def set_edited(self, boolean):
        self.first_panel.edited = boolean
        self.second_panel.edited = boolean

    def edited(self):
        return self.first_panel.edited or self.second_panel.edited

    def check_and_clear_table(self):
        if self.edited():
            logger.debug('Show dialog asking about table change')
            from gui.dialogs import RUSureChangeTable
            self.rusure = RUSureChangeTable()
            if self.rusure.exec_() == RUSureChangeTable.Yes:
                self.clear_table()
                return 0
            else:
                return 1
        else:
            logger.debug('Clearing table - not edited')
            self.clear_table()
            return 0

    def clear_table(self):
        for child in self.first_panel.findChildren(DragButton):
            child.before_close()
            del child
        for child in self.second_panel.findChildren(DragButton):
            child.before_close()
            del child

    def translateUI(self):
        self.setItemText(0, fromUtf8('Перший тиждень'))
        self.setItemText(1, fromUtf8('Другий тиждень'))

    def dragEnterEvent(self, e):
        e.accept()


class EasyTab(QtGui.QTabWidget):
    def __init__(self, parent, session):
        super(EasyTab, self).__init__(parent)
        self.session = session
        self.parent_name = parent.objectName()
        self.initUI()

    def setTabEnabled(self, p_int, bool):
        super(EasyTab, self).setTabEnabled(p_int, bool)
        self.setStyleSheet(
            'QTabBar::tab::disabled{width: 0; height: 0; margin: 0; '
            'padding: 0; border: none;}'
        )

    def initUI(self):
        self.tab_user = QtGui.QWidget(self)
        self.tab_method = QtGui.QWidget(self)
        self.tab_admin = AdminTab(self, self.session)
        self.tab_search = SearchTab(self, self.session)

        self.user_table = WeekTool(self.tab_user, self.session)
        user_hbox = QtGui.QHBoxLayout(self.tab_user)
        user_hbox.addWidget(self.user_table)
        self.tab_user.setLayout(user_hbox)

        self.method_table = WeekTool(self.tab_method, self.session)
        method_hbox = QtGui.QHBoxLayout(self.tab_method)
        method_hbox.addWidget(self.method_table, 1)
        self.tab_method.setLayout(method_hbox)

        self.translateUI()

    def translateUI(self):
        self.addTab(self.tab_user, fromUtf8('Користувач'))
        self.addTab(self.tab_method, fromUtf8('Методист'))
        self.addTab(self.tab_admin, fromUtf8('Адміністратор'))
        self.addTab(self.tab_search, fromUtf8('Пошук'))

    def set_table(self, lesson_set, view_args):
        result = self.method_table.set_table(lesson_set, view_args, drag_enabled=True)
        if result:
            return
        else:
            self.user_table.set_table(lesson_set, view_args)


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
        self.objects.setCurrentIndex(1)
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
        self.objects.items = [getattr(db_structure, item) for item in db_structure.__all__]
        for item in self.objects.items:
            columns = item.columns()
            if len(columns) == 2 and columns[0][:3] == columns[1][:3] == 'id_':
                self.objects.items.pop(self.objects.items.index(item))

        self.objects.items.sort(key=lambda a: a.translated)
        self.objects.addItems([item.translated for item in self.objects.items])

    def set_list(self):
        cls = self.objects.items[self.objects.currentIndex()]
        logger.info('Setting admin list for %s' % cls.__name__)
        self.items_list.clear()
        self.view_items = cls.read(self.session, all_=True)
        self.view_items.sort(key=lambda a: unicode(a))
        self.items_list.addItems([unicode(item) for item in self.view_items])

    def show_add(self):
        from gui.dialogs import AdminEditor
        cls = self.objects.items[self.objects.currentIndex()]
        logger.info('Running create dialog for %s' % cls.__name__)

        self.editor = AdminEditor(cls, self.session, empty=True)
        if self.editor.exec_() == AdminEditor.Accepted:
            logger.info('Adding accepted')
            fields = [elem for elem in cls.fields() if not (elem.startswith('id_') or elem == 'id' or elem == 'row_time')]
            values = {key: self.editor.get_pair(key) for key in fields}
            result = cls.create(self.session, **values)
            logger.debug('Result: "%s"' % unicode(result))
            self.view_items.append(result)
            self.view_items.sort(key=lambda a: unicode(a))
            new_index = self.view_items.index(result)
            self.items_list.insertItem(new_index, unicode(result))

    def show_delete(self):
        from gui.dialogs import RUSureDelete
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
        from gui.dialogs import AdminEditor
        index = self.items_list.row(self.items_list.currentItem())
        if index < 0 or index > self.view_items.__len__():
            return
        element = self.view_items[index]
        logger.info('Running edit dialog for %s' % unicode(element))

        self.editor = AdminEditor(element, self.session)
        if self.editor.exec_() == AdminEditor.Accepted:
            logger.info('Editing accepted')
            fields = [elem for elem in type(element).fields() if not (elem.startswith('id_') or elem == 'id' or elem == 'row_time')]
            values = {key: self.editor.get_pair(key) for key in fields}
            logger.debug(db_codes_output[type(element).update(
                self.session, main_id=element.id, **values
            )])
            self.view_items.sort(key=lambda a: unicode(a))
            new_index = self.view_items.index(element)
            self.items_list.takeItem(index)
            self.items_list.insertItem(new_index, unicode(element))


class SearchTab(QtGui.QWidget):
    def __init__(self, parent, session):
        super(SearchTab, self).__init__(parent)
        self.session = session
        self.setObjectName('search_tab')
        self.initUI()

    def initUI(self):
        self.hbox = QtGui.QHBoxLayout(self)
        self.hbox.setObjectName('search_tab_hbox')
        self.form = QtGui.QFormLayout()
        self.form.setObjectName('search_tab_form')

        for text in ['object', 'department', 'week', 'day', 'time']:
            setattr(self, text + '_label', QtGui.QLabel())
            setattr(self, text + '_choice', CompleterCombo())
            self.form.addRow(getattr(self, text + '_label'), getattr(self, text + '_choice'))

        spacer = QtGui.QSpacerItem(
            QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum
        )
        self.submit_button = QtGui.QPushButton(self)
        self.submit_button.clicked.connect(self.search)
        self.form.setItem(5, QtGui.QFormLayout.LabelRole, spacer)
        self.form.setWidget(5, QtGui.QFormLayout.FieldRole, self.submit_button)

        self.hbox.addLayout(self.form)
        self.search_list = QtGui.QListWidget(self)
        self.search_list.itemDoubleClicked.connect(self.set_table_by_item)
        self.hbox.addWidget(self.search_list)
        self.translateUI()

    def translateUI(self):
        self.object_label.setText(fromUtf8('Що знайти: '))
        self.object_choice.items = [db_structure.Teachers, db_structure.Rooms]
        self.object_choice.addItems([item.translated for item in self.object_choice.items])

        self.department_label.setText(db_structure.Departments.translated + u':')
        self.department_choice.items = db_structure.Departments.read(self.session, all_=True)
        self.department_choice.addItems([unicode(time) for time in self.department_choice.items])

        self.week_label.setText(db_structure.Weeks.translated + u':')
        self.week_choice.items = db_structure.Weeks.read(self.session, all_=True)
        self.week_choice.addItems([unicode(week) for week in self.week_choice.items])

        self.day_label.setText(db_structure.WeekDays.translated + u':')
        self.day_choice.items = db_structure.WeekDays.read(self.session, all_=True)
        self.day_choice.addItems([unicode(day) for day in self.day_choice.items])

        self.time_label.setText(db_structure.LessonTimes.translated + u':')
        self.time_choice.items = db_structure.LessonTimes.read(self.session, all_=True)
        self.time_choice.addItems([unicode(time) for time in self.time_choice.items])

        self.submit_button.setText(fromUtf8('Знайти'))

    def get_time(self):
        return dict(
            lesson_time=self.time_choice.items[self.time_choice.currentIndex()],
            week_day=self.day_choice.items[self.day_choice.currentIndex()],
            week=self.week_choice.items[self.week_choice.currentIndex()],
        )

    def department(self):
        return dict(department=self.department_choice.items[self.department_choice.currentIndex()])

    def search(self):
        from database.select_table import find_free
        params = self.get_time()
        params.update(self.department())
        cls = self.object_choice.items[self.object_choice.currentIndex()]
        result = find_free(self.session, cls, **params)
        logger.debug('Number of free: "%d"' % len(result))
        self.show_results(result)

    def show_results(self, values):
        self.search_list.clear()
        self.search_list.view_items = values
        self.search_list.addItems([unicode(value) for value in values])
        if not self.search_list.view_items:
            self.search_list.addItem(fromUtf8('На жаль, усі(усе) зайнято'))

    def set_table_by_item(self, *args):
        from database.select_table import get_table
        logger.debug(', '.join([str(arg) for arg in args]))
        logger.debug('%s' % args[0].text())
        logger.debug('%s' % self.search_list.row(args[0]))
        item = self.search_list.view_items[self.search_list.row(args[0])]
        cls_name = type(item).__tablename__
        self.parent().parent().set_table(get_table(self.session, cls_name, item.id), cls_name)


class WeekMenuBar(QtGui.QMenuBar):
    def __init__(self, *args, **kwargs):
        self.menu_data = kwargs.pop('menu_data', [])
        super(WeekMenuBar, self).__init__(*args, **kwargs)

        for menu in self.menu_data:
            menu_element = QtGui.QMenu(self)
            menu_element.setTitle(fromUtf8(menu[0]))
            setattr(self, 'menu_%d' % self.menu_data.index(menu), menu_element)
            for action in menu[1:]:
                if not action:
                    menu_element.addSeparator()
                else:
                    action_element = QtGui.QAction(self.parent())
                    action_element.setText(fromUtf8(action[0]))
                    action_element.triggered.connect(action[1])
                    menu_element.addAction(action_element)
            self.addAction(menu_element.menuAction())

        self.parent().setMenuBar(self)

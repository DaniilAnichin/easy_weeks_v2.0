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
    def __init__(self, parent, items_list, suggested_list, inner_name):
        super(EditableList, self).__init__(parent)
        self.view_items = items_list
        self.view_items.sort(key=lambda a: unicode(a))
        self.suggested_items = suggested_list
        self.suggested_items.sort(key=lambda a: unicode(a))
        self.addItems([unicode(item) for item in self.view_items])
        self.blocked = False
        setattr(self.parent(), inner_name, self)

    def mousePressEvent(self, QMouseEvent):
        QtGui.QListWidget.mousePressEvent(self, QMouseEvent)

        if self.blocked:
            return

        if not (QMouseEvent.modifiers() & QtCore.Qt.ShiftModifier):
            # Only Shift click performing
            return

        if QMouseEvent.button() == QtCore.Qt.RightButton:
            # Right button for delete
            index = self.row(self.currentItem())
            self.takeItem(index)
            logger.debug('Here should be delete')
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
        self.view_items.sort(key=lambda a: unicode(a))
        index = self.view_items.index(__args[0])
        self.insertItem(index, unicode(__args[0]))
        # super(EditableList, self).addItem(unicode(__args[0]))
        logger.info('Added item "%s"' % __args[:1])

    def takeItem(self, p_int):
        logger.info('Deleted item "%s"' % unicode(self.view_items[p_int]))
        self.view_items.pop(p_int)
        super(EditableList, self).takeItem(p_int)

    def show_completer(self):
        # Create completer combobox:
        completer = CompleterCombo(self)
        self.completer_items = list(set(self.suggested_items) - set(self.view_items))
        self.completer_items.sort(key=lambda a: unicode(a))
        completer.addItems([unicode(item) for item in self.completer_items])
        completer.setCurrentIndex(1)

        # Create modal window
        self.dialog = QtGui.QDialog()
        self.dialog.setModal(True)

        # Create button, connect
        submit = QtGui.QPushButton(fromUtf8('Додати'))
        # logger.debug(completer.currentText())
        submit.clicked.connect(partial(
            self.addItem,
            self.completer_items[completer.currentIndex()]
        ))
        submit.clicked.connect(self.dialog.close)

        # Add to layout
        vbox = QtGui.QVBoxLayout(self.dialog)
        vbox.addWidget(completer, 1)
        vbox.addWidget(submit, 1)

        # show
        logger.info('Raised completer window')
        self.dialog.exec_()


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
    def __init__(self, view_args, draggable, time, *args):
        super(DragButton, self).__init__(*args)
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
                self.edit_dial.exec_()
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
        if self.lesson.is_temp:
            type(self.lesson).delete(self.parent().session, self.lesson.id)


class ButtonGrid(QtGui.QGridLayout):
    def __init__(self, parent):
        self.created = False
        super(ButtonGrid, self).__init__(parent)
        # self.parent_name = parent.objectName()

    def set_table(self, lesson_set, view_args, week, drag_enabled=False):
        for i in range(len(lesson_set)):
            for j in range(len(lesson_set[i])):
                time = [week, i, j]
                lesson_button = DragButton(view_args, drag_enabled, time)
                self.addWidget(lesson_button, j, i, 1, 1)
                lesson_button.set_lesson(lesson_set[i][j])
        self.created = True


class TempGrid(QtGui.QGridLayout):
    def __init__(self, parent, table_height=5):
        super(TempGrid, self).__init__(parent)
        self.table_height = table_height
        self.buttons = []

        button = DragButton(parent)
        self.buttons.append(button)
        self.addWidget(button, 0, 0, 1, 1)

        self.translateUI()

    def add_button(self):
        button = DragButton(self.parent(), self.empty_text)
        self.buttons.append(button)
        x = (len(self.buttons) + 1) / self.table_height
        y = (len(self.buttons) + 1) % self.table_height
        self.addWidget(button, x, y, 1, 1)

    def remove_button(self, button):
        self.buttons.remove(button)
        self.removeWidget(button)
        del button

    def translateUI(self):
        self.empty_text = fromUtf8('Перетягніть\nзаняття сюди')
        self.buttons[-1].setText(self.empty_text)


class WeekTool(QtGui.QToolBox):
    def __init__(self, parent, session, *args, **kwargs):
        super(WeekTool, self).__init__(parent, *args, **kwargs)
        self.session = session
        self.first_panel = QtGui.QWidget(parent)
        self.first_panel.session = session
        self.second_panel = QtGui.QWidget(parent)
        self.second_panel.session = session
        self.first_table = ButtonGrid(self.first_panel)
        self.second_table = ButtonGrid(self.second_panel)
        self.addItem(self.first_panel, '')
        self.addItem(self.second_panel, '')
        self.translateUI()

    def set_table(self, lesson_set, view_args, drag_enabled=False):
        self.clear_table()
        self.first_table.set_table(lesson_set[0], view_args, 0, drag_enabled)
        self.second_table.set_table(lesson_set[1], view_args, 1, drag_enabled)

    def clear_table(self):
        for child in self.first_panel.children():
            if isinstance(child, DragButton):
                child.before_close()
                del child
        for child in self.second_panel.children():
            if isinstance(child, DragButton):
                child.before_close()
                del child

    def translateUI(self):
        self.setItemText(0, fromUtf8('Перший тиждень'))
        self.setItemText(1, fromUtf8('Другий тиждень'))

    def before_close(self):
        self.clear_table()
        logger.debug('We\'re going to close')


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
        self.user_table.set_table(lesson_set, view_args)
        self.method_table.set_table(lesson_set, view_args, drag_enabled=True)

'''
        self.tabWidget = MyTab(self.centralwidget)
        self.tabWidget.setObjectName(fromUtf8("tabWidget"))
        self.tab_user = QtGui.QWidget()
        self.tab_user.setObjectName(fromUtf8("tab_user"))

        self.gridLayout = QtGui.QGridLayout(self.tab_user)
        self.gridLayout.setObjectName(fromUtf8("gridLayout"))
        self.toolBox_2 = WeekTool(self.gridLayout.parent())
        self.toolBox_2.set_table(lesson_set)
        self.gridLayout.addWidget(self.toolBox_2)
        self.tabWidget.addTab(self.tab_user, fromUtf8(""))
        self.tab_method = QtGui.QWidget()
        self.tab_method.setObjectName(fromUtf8("tab_method"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_method)
        self.horizontalLayout_3.setObjectName(fromUtf8("horizontalLayout_3"))
        self.toolBox = WeekTool(self.horizontalLayout_3.parent())
        self.toolBox.set_table(lesson_set, drag_enabled=True)
        self.horizontalLayout_3.addWidget(self.toolBox)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(fromUtf8("verticalLayout"))
        self.pushButton_142 = QtGui.QPushButton(self.tab_method)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_142.sizePolicy().hasHeightForWidth())
        self.pushButton_142.setSizePolicy(sizePolicy)
        self.pushButton_142.setAcceptDrops(True)
        self.pushButton_142.setObjectName(fromUtf8("pushButton_142"))
        self.verticalLayout.addWidget(self.pushButton_142)
        self.pushButton_193 = QtGui.QPushButton(self.tab_method)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_193.sizePolicy().hasHeightForWidth())
        self.pushButton_193.setSizePolicy(sizePolicy)
        self.pushButton_193.setAcceptDrops(True)
        self.pushButton_193.setObjectName(fromUtf8("pushButton_193"))
        self.verticalLayout.addWidget(self.pushButton_193)
        self.pushButton_140 = QtGui.QPushButton(self.tab_method)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_140.sizePolicy().hasHeightForWidth())
        self.pushButton_140.setSizePolicy(sizePolicy)
        self.pushButton_140.setAcceptDrops(True)
        self.pushButton_140.setObjectName(fromUtf8("pushButton_140"))
        self.verticalLayout.addWidget(self.pushButton_140)
        self.pushButton_141 = QtGui.QPushButton(self.tab_method)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_141.sizePolicy().hasHeightForWidth())
        self.pushButton_141.setSizePolicy(sizePolicy)
        self.pushButton_141.setAcceptDrops(True)
        self.pushButton_141.setObjectName(fromUtf8("pushButton_141"))
        self.verticalLayout.addWidget(self.pushButton_141)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
'''


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
            # Perform DB call
            # Perform add calld

    def show_delete(self):
        from gui.dialogs import RUSureDelete
        # cls_name = db_structure.__all__[self.objects.currentIndex()]
        # logger.info('Running create dialog for %s' % cls_name)
        #
        # self.editor = AdminEditor(cls_name, self.session, empty=True)
        # self.editor.show()
        index = self.items_list.row(self.items_list.currentItem())
        if index < 0 or index > self.view_items.__len__():
            return
        element = self.view_items[index]
        cls = type(element)
        self.warning = RUSureDelete(element)
        if self.warning.exec_() == QtGui.QMessageBox.Yes:
            logger.info('Item %s deleted' % unicode(self.items_list.currentItem().text()))
            self.items_list.takeItem(index)
            logger.info(db_codes_output[cls.delete(self.session, main_id=element.id)])
            # Perform db call

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
            # Perform DB call
            # Perform add calld


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

        self.object_label = QtGui.QLabel(self)
        self.object_choice = QtGui.QComboBox(self)
        self.form.addRow(self.object_label, self.object_choice)

        self.week_label = QtGui.QLabel(self)
        self.week_choice = QtGui.QComboBox(self)
        self.form.addRow(self.week_label, self.week_choice)

        self.day_label = QtGui.QLabel(self)
        self.day_choice = QtGui.QComboBox(self)
        self.form.addRow(self.day_label, self.day_choice)

        self.time_label = QtGui.QLabel(self)
        self.time_choice = QtGui.QComboBox(self)
        self.form.addRow(self.time_label, self.time_choice)

        spacer = QtGui.QSpacerItem(
            QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum
        )
        self.submit_button = QtGui.QPushButton(self)
        self.submit_button.clicked.connect(self.search)
        self.form.setItem(4, QtGui.QFormLayout.LabelRole, spacer)
        self.form.setWidget(4, QtGui.QFormLayout.FieldRole, self.submit_button)

        self.hbox.addLayout(self.form)
        self.search_list = QtGui.QListView(self)
        self.hbox.addWidget(self.search_list)
        self.translateUI()

    def translateUI(self):
        self.object_label.setText(fromUtf8('Що знайти: '))
        self.object_choice.addItem(fromUtf8('Кімната'))
        self.object_choice.addItem(fromUtf8('Викладач'))

        self.week_label.setText(fromUtf8('Тиждень: '))
        self.week_choice.addItems(
            [unicode(week) for week in db_structure.Weeks.read(self.session, all_=True)]
        )

        self.day_label.setText(fromUtf8('День: '))
        self.day_choice.addItems(
            [unicode(day) for day in db_structure.WeekDays.read(self.session, all_=True)]
        )

        self.time_label.setText(fromUtf8('Час: '))
        self.time_choice.addItems(
            [unicode(time) for time in db_structure.LessonTimes.read(self.session, all_=True)]
        )

        self.submit_button.setText(fromUtf8('Знайти'))

    def search(self):
        logger.debug('Here should be search')


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

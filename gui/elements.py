#!/usr/bin/python
# -*- coding: utf-8 -*-
from functools import partial
from database import Logger
from database.structure import db_structure
from PyQt4 import QtGui, QtCore
from gui.translate import fromUtf8
logger = Logger()


# color_start = 'background-color: '
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


class EditableList(QtGui.QListWidget):
    def __init__(self, parent, items_list, suggested_list, inner_name):
        super(EditableList, self).__init__(parent)
        self.addItems(items_list)
        self.added_items = items_list
        self.suggested_list = suggested_list
        setattr(self.parent(), inner_name, self)

    def mousePressEvent(self, QMouseEvent):
        QtGui.QListWidget.mousePressEvent(self, QMouseEvent)

        if not (QMouseEvent.modifiers() & QtCore.Qt.ShiftModifier):
            # Only Shift click performing
            return

        if QMouseEvent.button() == QtCore.Qt.RightButton:
            # Right button for delete
            self.removeItemWidget(self.currentItem())
            logger.debug('Here should be delete')
        elif QMouseEvent.button() == QtCore.Qt.LeftButton:
            # Left button to add
            self.show_completer()

    def addItem(self, *__args):
        logger.debug(__args)

        if unicode(__args[0]) not in self.suggested_list:
            return

        super(EditableList, self).addItem(*__args[:1])
        # Save to this list, to be able to subtract
        self.added_items += [unicode(__args[0])]
        logger.info('Added item "%s"' % __args[:1])

    def removeItemWidget(self, listWidgetItem):
        try:
            index = self.added_items.index(listWidgetItem.text())
        except AttributeError:
            logger.info('Already deleted')
            return
        self.added_items.pop(index)
        logger.info('Deleted item "%s"' % listWidgetItem.text())
        self.takeItem(self.row(listWidgetItem))

    def show_completer(self):
        # Create completer combobox:
        completer = CompleterCombo(self)
        completer.addItems(list(set(self.suggested_list) - set(self.added_items)))

        # Create modal window
        self.dialog = QtGui.QDialog()
        self.dialog.setModal(True)

        # Create button, connect
        submit = QtGui.QPushButton(fromUtf8('Додати'))
        # logger.debug(completer.currentText())
        submit.clicked.connect(partial(self.addItem, completer.currentText()))
        submit.clicked.connect(self.dialog.close)

        # Add to layout
        vbox = QtGui.QVBoxLayout(self.dialog)
        vbox.addWidget(completer, 1)
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
    def __init__(self, lesson, view_args, draggable, *args):
        super(DragButton, self).__init__(*args)
        self.lesson = lesson
        self.view_args = view_args
        size_policy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum
        )
        self.setSizePolicy(size_policy)
        self.setAcceptDrops(draggable)
        self.draggable = draggable
        logger.debug('Lesson is: %s' % self.lesson)
        if isinstance(self.lesson, list):
            logger.debug('Lesson num is: %s' % len(self.lesson))
        self.setText(self.lesson.to_table(view_args))
        self.set_bg_color(
            self.lesson.lesson_plan.lesson_type.short_name
        )

    def mousePressEvent(self, QMouseEvent):
        QtGui.QPushButton.mousePressEvent(self, QMouseEvent)

        if QMouseEvent.button() == QtCore.Qt.RightButton:
            # Pressing callback
            from gui.dialogs import ShowLesson, EditLesson

            if self.draggable:
                self.edit_dial = EditLesson(self.lesson, self.parent().session, time=False)
                self.edit_dial.show()
            else:
                self.show_dial = ShowLesson(self.lesson)
                self.show_dial.show()
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
        # exec_ will return the accepted action from dropEvent
        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            print 'moved'
        else:
            print 'copied'

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        # get the relative position from the mime data
        mime = e.mimeData().text()
        if self != e.source():
            if e.keyboardModifiers() & QtCore.Qt.ShiftModifier:
                # Do we need any other modes??
                e.setDropAction(QtCore.Qt.CopyAction)
            else:
                # Perform swap:
                # Further add lesson swap
                content = e.source().lesson
                e.source().lesson = self.lesson
                e.source().setText(self.text())
                self.lesson = content
                self.setText(content.to_table(self.view_args))

                # tell the QDrag we accepted it
                e.setDropAction(QtCore.Qt.MoveAction)
                e.accept()
        else:
            e.ignore()

    def set_bg_color(self, lesson_type):
        # palette = self.palette()
        # palette.setColor(
        #     QtGui.QPalette.Button,
        #     button_colors[lesson_type]
        # )
        # self.setAutoFillBackground(True)
        # self.setPalette(palette)
        # self.update()

        self.setStyleSheet(
            # color_start + button_colors[lesson_type].name()
            color_start.format(*button_colors[lesson_type])
            # color_start.format(*button_colors[u'Лек'])
        )


class ButtonGrid(QtGui.QGridLayout):
    def __init__(self, parent):
        super(ButtonGrid, self).__init__(parent)
        # self.parent_name = parent.objectName()

    def set_table(self, lesson_set, view_args, drag_enabled=False):
        for i in range(len(lesson_set)):
            for j in range(len(lesson_set[i])):
                self.addWidget(
                    DragButton(lesson_set[i][j], view_args, drag_enabled),
                    j, i, 1, 1)


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
        self.first = QtGui.QWidget(parent)
        self.first.session = session
        self.second = QtGui.QWidget(parent)
        self.second.session = session

    def set_table(self, lesson_set, view_args, drag_enabled=False):
        first_table = ButtonGrid(self.first)
        first_table.set_table(lesson_set[0], view_args, drag_enabled)
        second_table = ButtonGrid(self.second)
        second_table.set_table(lesson_set[1], view_args, drag_enabled)
        self.addItem(self.first, '')
        self.addItem(self.second, '')
        self.translateUI()

    def translateUI(self):
        self.setItemText(0, fromUtf8('Перший тиждень'))
        self.setItemText(1, fromUtf8('Другий тиждень'))


class EasyTab(QtGui.QTabWidget):
    def __init__(self, parent, session):
        super(EasyTab, self).__init__(parent)
        self.session = session
        # self.user =
        # self.tabWidget.setTabEnabled(
        #     self.tabWidget.indexOf(self.tab_admin), False
        # )
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

        self.translateUI()

    def translateUI(self):
        self.addTab(self.tab_user, fromUtf8('Користувач'))
        self.addTab(self.tab_method, fromUtf8('Методист'))
        self.addTab(self.tab_admin, fromUtf8('Адміністратор'))
        self.addTab(self.tab_search, fromUtf8('Пошук'))

    def set_table(self, lesson_set, view_args):
        self.user_table.set_table(lesson_set, view_args)

        self.method_table.set_table(lesson_set, view_args, drag_enabled=True)
        # self.temp_table = TempGrid(self.tab_method)
        method_hbox = QtGui.QHBoxLayout(self.tab_method)
        method_hbox.addWidget(self.method_table, 1)
        # method_hbox.addLayout(self.temp_table, 1)
        self.tab_method.setLayout(method_hbox)


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


class AdminList(QtGui.QListWidget):
    def __init__(self, *args, **kwargs):
        super(AdminList, self).__init__(*args, **kwargs)

    def addItem(self, *__args):
        logger.info('Item %s added', __args[0])
        super(AdminList, self).addItem(*__args[1:])

    def takeItem(self):
        logger.info('Item %s deleted' % self.currentItem().text())
        self.viewed_items.pop(self.row(self.currentItem()))
        super(AdminList, self).takeItem(self.row(self.currentItem()))


class AdminTab(QtGui.QWidget):
    def __init__(self, parent, session):
        super(AdminTab, self).__init__(parent)
        self.session = session
        self.setObjectName('admin_tab')
        self.initUI()

    def initUI(self):
        self.vbox = QtGui.QVBoxLayout(self)
        self.hbox = QtGui.QHBoxLayout()
        self.objects = CompleterCombo(self)
        self.objects.currentIndexChanged.connect(self.set_list)

        self.hbox.addWidget(self.objects)
        spacer = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum
        )
        self.hbox.addItem(spacer)

        self.items_list = AdminList(self)

        self.addButton = QtGui.QPushButton(self)
        self.addButton.clicked.connect(self.show_add)
        self.deleteButton = QtGui.QPushButton(self)
        self.deleteButton.clicked.connect(partial(self.items_list.takeItem))
        self.editButton = QtGui.QPushButton(self)
        self.editButton.clicked.connect(self.show_edit)
        self.hbox.addWidget(self.addButton)
        self.hbox.addWidget(self.deleteButton)
        self.hbox.addWidget(self.editButton)

        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.items_list)
        self.translateUI()

    def translateUI(self):
        self.objects.addItems(
            [getattr(db_structure, elem).translated for elem in db_structure.__all__]
        )

        self.addButton.setText(fromUtf8('Додати'))
        self.deleteButton.setText(fromUtf8('Видалити'))
        self.editButton.setText(fromUtf8('Редагувати'))

    def set_list(self):
        cls_name = db_structure.__all__[self.objects.currentIndex()]
        logger.info('Setting admin list for %s' % cls_name)
        elements = getattr(db_structure, cls_name).read(self.session, all_=True)
        self.items_list.clear()
        self.items_list.viewed_items = elements
        self.items_list.addItems([unicode(elem) for elem in elements])

    def show_add(self):
        from gui.dialogs import AdminEditor
        cls_name = db_structure.__all__[self.objects.currentIndex()]
        logger.info('Running create dialog for %s' % cls_name)
        # elements = getattr(db_structure, cls_name).read(self.session, all_=True)

    def show_edit(self):
        from gui.dialogs import AdminEditor
        cls_name = db_structure.__all__[self.objects.currentIndex()]
        index = self.items_list.row(self.items_list.currentItem())
        name = self.items_list.currentItem().text()
        logger.info('Running edit dialog for %s - %s' % (cls_name, name))

        element = self.items_list.viewed_items[index]
        # self.edit_dial = AdminEditor()


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
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 19))
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

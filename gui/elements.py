#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from gui.translate import translate, fromUtf8


color_start = 'background-color: '

# need other colors, looks ugly
button_colors = [
    QtGui.QColor(255, 0, 0),
    QtGui.QColor(0, 255, 0),
    QtGui.QColor(0, 0, 255)
]


class DragButton(QtGui.QPushButton):
    def __init__(self, *args):
        super(DragButton, self).__init__(*args)
        size_policy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum
        )
        self.setSizePolicy(size_policy)
        self.setAcceptDrops(True)
        self.lesson = 'None'

    def setAcceptDrags(self, bool):
        if not bool:
            pass
            # delattr(self, 'mousePressEvent')

    def mousePressEvent(self, e):
        QtGui.QPushButton.mousePressEvent(self, e)

        if e.button() == QtCore.Qt.RightButton:
            # Pressing callback
            # print 'Pressing callback'
            print self

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.LeftButton:
            return

        mimeData = QtCore.QMimeData()
        mimeData.setText(self.lesson)

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
                content = e.source().text()
                e.source().setText(self.text())
                self.setText(content)

                # tell the QDrag we accepted it
                e.setDropAction(QtCore.Qt.MoveAction)
                e.accept()
        else:
            e.ignore()


class ButtonGrid(QtGui.QGridLayout):
    def __init__(self, parent):
        super(ButtonGrid, self).__init__(parent)
        self.parent_name = parent.objectName()

    def set_table(self, lesson_set, drag_enabled=False):
        for i in range(len(lesson_set)):
            for j in range(len(lesson_set[i])):
                lesson_button = DragButton(self.parent())
                lesson_button.setAcceptDrops(drag_enabled)
                lesson_button.setText(str(lesson_set[i][j]))
                lesson_button.setStyleSheet(
                    color_start + button_colors[lesson_set[i][j]].name()
                )

                self.addWidget(lesson_button, j, i, 1, 1)


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
    def __init__(self, parent, *args, **kwargs):
        super(WeekTool, self).__init__(parent, *args, **kwargs)
        self.first = QtGui.QWidget(self.parent())
        self.second = QtGui.QWidget(self.parent())
        # self.setObjectName('week_tool_%s' % self.parent().objectName())
        # self.first.setObjectName('first_%s' % self.objectName())
        # self.second.setObjectName('second_%s' % self.objectName())

    def set_table(self, lesson_set, drag_enabled=False):
        first_table = ButtonGrid(self.first)
        first_table.set_table(lesson_set[:len(lesson_set) / 2], drag_enabled)
        second_table = ButtonGrid(self.second)
        second_table.set_table(lesson_set[len(lesson_set) / 2:], drag_enabled)
        self.addItem(self.first, '')
        self.addItem(self.second, '')
        self.translateUI()

    def translateUI(self):
        self.setItemText(0, fromUtf8('Перший тиждень'))
        self.setItemText(1, fromUtf8('Другий тиждень'))


class EasyTab(QtGui.QTabWidget):
    def __init__(self, parent):
        super(EasyTab, self).__init__(parent)
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
        self.tab_admin = AdminTab(self)
        self.tab_search = SearchTab(self)

        self.user_table = WeekTool(self.tab_user)
        user_hbox = QtGui.QHBoxLayout(self.tab_user)
        user_hbox.addWidget(self.user_table)
        self.tab_user.setLayout(user_hbox)
        self.method_table = WeekTool(self.tab_method)

        self.translateUI()

    def translateUI(self):
        self.addTab(self.tab_user, fromUtf8('Користувач'))
        self.addTab(self.tab_method, fromUtf8('Методист'))
        self.addTab(self.tab_admin, fromUtf8('Адміністратор'))
        self.addTab(self.tab_search, fromUtf8('Пошук'))

    def set_table(self, lesson_set):
        self.user_table.set_table(lesson_set)

        self.method_table.set_table(lesson_set, drag_enabled=True)
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


def make_combo_box(parent, model, choice_list):
    # choice_list = [{name: action}, ...]
    combo_box = QtGui.QComboBox(parent)
    combo_box.setObjectName('itemsChoice')
    combo_box.addItem('')
    combo_box.addItem('')
    combo_box.addItem('')
    combo_box.addItem('')
    combo_box.addItem('')
    combo_box.addItem('')


class AdminTab(QtGui.QWidget):
    def __init__(self, parent):
        super(AdminTab, self).__init__(parent)
        self.setObjectName('admin_tab')
        self.initUI()

    def initUI(self):
        self.vbox = QtGui.QVBoxLayout(self)
        self.hbox = QtGui.QHBoxLayout()
        self.objects = QtGui.QComboBox(self)

        self.hbox.addWidget(self.objects)
        spacer = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum
        )
        self.hbox.addItem(spacer)

        self.addButton = QtGui.QPushButton(self)
        self.deleteButton = QtGui.QPushButton(self)
        self.editButton = QtGui.QPushButton(self)
        self.hbox.addWidget(self.addButton)
        self.hbox.addWidget(self.deleteButton)
        self.hbox.addWidget(self.editButton)
        self.vbox.addLayout(self.hbox)

        self.items_list = QtGui.QListWidget(self)
        self.vbox.addWidget(self.items_list)
        self.translateUI()

    def translateUI(self):
        # for j in database.__all__
        #     self.itemsChoice.addItem()...

        self.objects.addItem(fromUtf8('Дні тиждня'))
        self.objects.addItem(fromUtf8('Тиждні'))
        self.objects.addItem(fromUtf8('Предмети'))
        self.objects.addItem(fromUtf8('Рівні викладачів'))
        self.objects.addItem(fromUtf8('Типи занятть'))
        self.objects.addItem(fromUtf8('Викладачi'))

        self.addButton.setText(fromUtf8('Додати'))
        self.deleteButton.setText(fromUtf8('Видалити'))
        self.editButton.setText(fromUtf8('Редагувати'))

        day_list = [
            'Понеділок',
            'Вівторок',
            'Середа',
            'Четвер',
            'П\'ятниця',
            'Субота'
        ]
        for day in day_list * 2:
            item = QtGui.QListWidgetItem(fromUtf8(day))
            self.items_list.addItem(item)


class SearchTab(QtGui.QWidget):
    def __init__(self, parent):
        super(SearchTab, self).__init__(parent)
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
        self.week_choice.addItem(fromUtf8('Перший'))
        self.week_choice.addItem(fromUtf8('Другий'))

        self.day_label.setText(fromUtf8('День: '))
        # Choose from DB
        self.day_choice.addItem(fromUtf8('Понеділок'))
        self.day_choice.addItem(fromUtf8('Вівторок'))
        self.day_choice.addItem(fromUtf8('Середа'))
        self.day_choice.addItem(fromUtf8('Четвер'))
        self.day_choice.addItem(fromUtf8('П\'ятниця'))
        self.day_choice.addItem(fromUtf8('Субота'))

        self.time_label.setText(fromUtf8('Час: '))
        # Choose from DB
        self.time_choice.addItem(fromUtf8('8:30 - 10:05'))
        self.time_choice.addItem(fromUtf8('10:25 - 12:00'))
        self.time_choice.addItem(fromUtf8('12:20 - 13:55'))
        self.time_choice.addItem(fromUtf8('14:15 - 15:50'))
        self.time_choice.addItem(fromUtf8('16:10 - 17:45'))
        self.time_choice.addItem(fromUtf8('18:05 - 19:40'))

        self.submit_button.setText(fromUtf8('Знайти'))


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

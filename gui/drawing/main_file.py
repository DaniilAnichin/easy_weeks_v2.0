#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
import login
from functools import partial
from PyQt4 import QtCore, QtGui
from gui.translate import _translate, _fromUtf8


# try:
#     _fromUtf8 = QtCore.QString.fromUtf8
# except AttributeError:
#     def _fromUtf8(s):
#         return s
#
#
# try:
#     _encoding = QtGui.QApplication.UnicodeUTF8
#
#
#     def _translate(context, text, disambig):
#         return QtGui.QApplication.translate(context, text, disambig, _encoding)
# except AttributeError:
#     def _translate(context, text, disambig):
#         return QtGui.QApplication.translate(context, text, disambig)

color_start = 'background-color: '

# need other colors, looks ugly
button_colors = [
    QtGui.QColor(255, 0, 0),
    QtGui.QColor(0, 255, 0),
    QtGui.QColor(0, 0, 255)
]


def draw_table(lesson_set, parent, drag_enabled=False):
    parent_name = parent.objectName()
    # Grid that will be returned
    lesson_grid = QtGui.QGridLayout(parent)
    lesson_grid.setObjectName(_fromUtf8('grid_from' + parent_name))

    # creating a size policy for button to make them resizable
    size_policy = QtGui.QSizePolicy(
        QtGui.QSizePolicy.Minimum,
        QtGui.QSizePolicy.Minimum
    )

    for i in range(len(lesson_set)):
        for j in range(len(lesson_set[i])):
            lesson_button = QtGui.QPushButton(parent)
            lesson_button.setSizePolicy(size_policy)
            lesson_button.setAcceptDrops(drag_enabled)
            lesson_button.setObjectName(_fromUtf8(
                "button_{0}_{1}_{2}".format(parent_name, i, j)
            ))
            lesson_button.setText('{0}\n{0}'.format(lesson_set[i][j]))
            lesson_button.setStyleSheet(
                color_start + button_colors[lesson_set[i][j]].name()
            )

            lesson_grid.addWidget(lesson_button, j, i, 1, 1)

    return lesson_grid


def make_combo_box(parent, model, choice_list):
    # choice_list = [{name: action}, ...]
    combo_box = QtGui.QComboBox(parent)
    combo_box.setObjectName(_fromUtf8("itemsChoice"))
    combo_box.addItem(_fromUtf8(""))
    combo_box.addItem(_fromUtf8(""))
    combo_box.addItem(_fromUtf8(""))
    combo_box.addItem(_fromUtf8(""))
    combo_box.addItem(_fromUtf8(""))
    combo_box.addItem(_fromUtf8(""))

    pass


# Check if it works on windows...
# On linux default is good enough
class MyTab(QtGui.QTabWidget):
    def setTabEnabled(self, p_int, bool):
        super(MyTab, self).setTabEnabled(p_int, bool)
        self.setStyleSheet(
            'QTabBar::tab::disabled{width: 0; height: 0; margin: 0; '
            'padding: 0; border: none;}'
        )


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, lesson_set):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(805, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        # self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget = MyTab(self.centralwidget)
        # self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_user = QtGui.QWidget()
        self.tab_user.setObjectName(_fromUtf8("tab_user"))
        self.gridLayout = QtGui.QGridLayout(self.tab_user)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.toolBox_2 = QtGui.QToolBox(self.tab_user)
        self.toolBox_2.setObjectName(_fromUtf8("toolBox_2"))
        self.page_3 = QtGui.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 522, 162))
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.gridLayout_2 = draw_table(
            lesson_set[0:len(lesson_set) / 2],
            self.page_3
        )
        self.toolBox_2.addItem(self.page_3, _fromUtf8(""))
        self.page_4 = QtGui.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 765, 446))
        self.page_4.setObjectName(_fromUtf8("page_4"))
        self.gridLayout_3 = draw_table(
            lesson_set[len(lesson_set) / 2:],
            self.page_4
        )
        self.toolBox_2.addItem(self.page_4, _fromUtf8(""))
        self.gridLayout.addWidget(self.toolBox_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_user, _fromUtf8(""))
        self.tab_method = QtGui.QWidget()
        self.tab_method.setObjectName(_fromUtf8("tab_method"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_method)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.toolBox = QtGui.QToolBox(self.tab_method)
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 522, 162))
        self.page.setObjectName(_fromUtf8("page"))
        self.gridLayout_4 = draw_table(
            lesson_set[0:len(lesson_set) / 2],
            self.page
        )
        self.toolBox.addItem(self.page, _fromUtf8(""))
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 678, 446))
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.gridLayout_5 = draw_table(
            lesson_set[len(lesson_set) / 2:],
            self.page_2
        )
        self.toolBox.addItem(self.page_2, _fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.toolBox)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton_142 = QtGui.QPushButton(self.tab_method)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,
                                       QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_142.sizePolicy().hasHeightForWidth())
        self.pushButton_142.setSizePolicy(sizePolicy)
        self.pushButton_142.setAcceptDrops(True)
        self.pushButton_142.setObjectName(_fromUtf8("pushButton_142"))
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
        self.pushButton_193.setObjectName(_fromUtf8("pushButton_193"))
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
        self.pushButton_140.setObjectName(_fromUtf8("pushButton_140"))
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
        self.pushButton_141.setObjectName(_fromUtf8("pushButton_141"))
        self.verticalLayout.addWidget(self.pushButton_141)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab_method, _fromUtf8(""))
        self.tab_admin = QtGui.QWidget()
        self.tab_admin.setObjectName(_fromUtf8("tab_admin"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_admin)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.itemsChoice = QtGui.QComboBox(self.tab_admin)
        self.itemsChoice.setObjectName(_fromUtf8("itemsChoice"))
        self.itemsChoice.addItem(_fromUtf8(""))
        self.itemsChoice.addItem(_fromUtf8(""))
        self.itemsChoice.addItem(_fromUtf8(""))
        self.itemsChoice.addItem(_fromUtf8(""))
        self.itemsChoice.addItem(_fromUtf8(""))
        self.itemsChoice.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.itemsChoice)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.addButton = QtGui.QPushButton(self.tab_admin)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout_2.addWidget(self.addButton)
        self.deleteButton = QtGui.QPushButton(self.tab_admin)
        self.deleteButton.setEnabled(True)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.horizontalLayout_2.addWidget(self.deleteButton)
        self.editButton = QtGui.QPushButton(self.tab_admin)
        self.editButton.setObjectName(_fromUtf8("editButton"))
        self.horizontalLayout_2.addWidget(self.editButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.listWidget = QtGui.QListWidget(self.tab_admin)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidget.addItem(item)
        self.verticalLayout_3.addWidget(self.listWidget)
        self.tabWidget.addTab(self.tab_admin, _fromUtf8(""))
        self.tab_search = QtGui.QWidget()
        self.tab_search.setObjectName(_fromUtf8("tab_search"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.tab_search)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label = QtGui.QLabel(self.tab_search)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.itemsChoice_2 = QtGui.QComboBox(self.tab_search)
        self.itemsChoice_2.setObjectName(_fromUtf8("itemsChoice_2"))
        self.itemsChoice_2.addItem(_fromUtf8(""))
        self.itemsChoice_2.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole,
                                    self.itemsChoice_2)
        self.label_4 = QtGui.QLabel(self.tab_search)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole,
                                    self.label_4)
        self.itemsChoice_3 = QtGui.QComboBox(self.tab_search)
        self.itemsChoice_3.setObjectName(_fromUtf8("itemsChoice_3"))
        self.itemsChoice_3.addItem(_fromUtf8(""))
        self.itemsChoice_3.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole,
                                    self.itemsChoice_3)
        self.label_2 = QtGui.QLabel(self.tab_search)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole,
                                    self.label_2)
        self.itemsChoice_4 = QtGui.QComboBox(self.tab_search)
        self.itemsChoice_4.setObjectName(_fromUtf8("itemsChoice_4"))
        self.itemsChoice_4.addItem(_fromUtf8(""))
        self.itemsChoice_4.addItem(_fromUtf8(""))
        self.itemsChoice_4.addItem(_fromUtf8(""))
        self.itemsChoice_4.addItem(_fromUtf8(""))
        self.itemsChoice_4.addItem(_fromUtf8(""))
        self.itemsChoice_4.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole,
                                    self.itemsChoice_4)
        self.label_3 = QtGui.QLabel(self.tab_search)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole,
                                    self.label_3)
        self.itemsChoice_5 = QtGui.QComboBox(self.tab_search)
        self.itemsChoice_5.setObjectName(_fromUtf8("itemsChoice_5"))
        self.itemsChoice_5.addItem(_fromUtf8(""))
        self.itemsChoice_5.addItem(_fromUtf8(""))
        self.itemsChoice_5.addItem(_fromUtf8(""))
        self.itemsChoice_5.addItem(_fromUtf8(""))
        self.itemsChoice_5.addItem(_fromUtf8(""))
        self.itemsChoice_5.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole,
                                    self.itemsChoice_5)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum,
                                        QtGui.QSizePolicy.Minimum)
        self.formLayout_2.setItem(4, QtGui.QFormLayout.LabelRole, spacerItem1)
        self.addButton_2 = QtGui.QPushButton(self.tab_search)
        self.addButton_2.setObjectName(_fromUtf8("addButton_2"))
        self.formLayout_2.setWidget(4, QtGui.QFormLayout.FieldRole,
                                    self.addButton_2)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.listView = QtGui.QListView(self.tab_search)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.horizontalLayout_4.addWidget(self.listView)
        self.tabWidget.addTab(self.tab_search, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        self.menu_3 = QtGui.QMenu(self.menubar)
        self.menu_3.setObjectName(_fromUtf8("menu_3"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOneOne = QtGui.QAction(MainWindow)
        self.actionOneOne.setObjectName(_fromUtf8("actionOneOne"))
        self.actionOneTwo = QtGui.QAction(MainWindow)
        self.actionOneTwo.setObjectName(_fromUtf8("actionOneTwo"))
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName(_fromUtf8("action"))
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName(_fromUtf8("action_2"))
        self.action_3 = QtGui.QAction(MainWindow)
        self.action_3.setObjectName(_fromUtf8("action_3"))
        self.action_5 = QtGui.QAction(MainWindow)
        self.action_5.setObjectName(_fromUtf8("action_5"))
        self.action_6 = QtGui.QAction(MainWindow)
        self.action_6.setObjectName(_fromUtf8("action_6"))
        self.action_7 = QtGui.QAction(MainWindow)
        self.action_7.setObjectName(_fromUtf8("action_7"))
        self.action_9 = QtGui.QAction(MainWindow)
        self.action_9.setObjectName(_fromUtf8("action_9"))
        self.action_10 = QtGui.QAction(MainWindow)
        self.action_10.setObjectName(_fromUtf8("action_10"))
        self.menu.addAction(self.action)
        self.menu_2.addAction(self.action_2)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.action_5)
        self.menu_2.addAction(self.action_6)
        self.menu_3.addAction(self.action_7)
        self.menu_3.addSeparator()
        self.menu_3.addAction(self.action_9)
        self.menu_3.addAction(self.action_10)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.toolBox_2.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.tabWidget.setTabEnabled(
            self.tabWidget.indexOf(self.tab_admin), False
        )

        timer = QtCore.QTimer()
        timer.setSingleShot(True)
        timer.singleShot(5000, partial(
            self.tabWidget.setTabEnabled,
            self.tabWidget.indexOf(self.tab_admin),
            True
        ))

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_3),
                                   _translate("MainWindow", "Перший тиждень",
                                              None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_4),
                                   _translate("MainWindow", "Другий тиждень",
                                              None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_user),
                                  _translate("MainWindow", "Користувач", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page),
                                 _translate("MainWindow", "Перший тиждень",
                                            None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2),
                                 _translate("MainWindow", "Другий тиждень",
                                            None))
        self.pushButton_142.setText(
            _translate("MainWindow", "PushButton", None))
        self.pushButton_193.setText(
            _translate("MainWindow", "PushButton", None))
        self.pushButton_140.setText(
            _translate("MainWindow", "PushButton", None))
        self.pushButton_141.setText(
            _translate("MainWindow", "PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_method),
                                  _translate("MainWindow", "Методист", None))
        self.itemsChoice.setItemText(0, _translate("MainWindow", "Дні тиждня",
                                                   None))
        self.itemsChoice.setItemText(1,
                                     _translate("MainWindow", "Тиждні", None))
        self.itemsChoice.setItemText(2,
                                     _translate("MainWindow", "Предмети", None))
        self.itemsChoice.setItemText(3, _translate("MainWindow",
                                                   "Рівні викладачів", None))
        self.itemsChoice.setItemText(4, _translate("MainWindow", "Типи занятть",
                                                   None))
        self.itemsChoice.setItemText(5, _translate("MainWindow", "Викладачi",
                                                   None))
        self.addButton.setText(_translate("MainWindow", "Додати", None))
        self.deleteButton.setText(_translate("MainWindow", "Видалити", None))
        self.editButton.setText(_translate("MainWindow", "Редагувати", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Понеділок", None))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Вівторок", None))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Середа", None))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "Четвер", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_admin),
                                  _translate("MainWindow", "Адміністратор",
                                             None))
        self.label.setText(_translate("MainWindow", "Що знайти: ", None))
        self.itemsChoice_2.setItemText(0, _translate("MainWindow", "Кімната",
                                                     None))
        self.itemsChoice_2.setItemText(1, _translate("MainWindow", "Викладач",
                                                     None))
        self.label_4.setText(_translate("MainWindow", "Тиждень:", None))
        self.itemsChoice_3.setItemText(0,
                                       _translate("MainWindow", "Перший", None))
        self.itemsChoice_3.setItemText(1,
                                       _translate("MainWindow", "Другий", None))
        self.label_2.setText(_translate("MainWindow", "День:", None))
        self.itemsChoice_4.setItemText(0, _translate("MainWindow", "Понеділок",
                                                     None))
        self.itemsChoice_4.setItemText(1, _translate("MainWindow", "Вівторок",
                                                     None))
        self.itemsChoice_4.setItemText(2,
                                       _translate("MainWindow", "Середа", None))
        self.itemsChoice_4.setItemText(3,
                                       _translate("MainWindow", "Четвер", None))
        self.itemsChoice_4.setItemText(4, _translate("MainWindow", "П\'ятниця",
                                                     None))
        self.itemsChoice_4.setItemText(5,
                                       _translate("MainWindow", "Субота", None))
        self.label_3.setText(_translate("MainWindow", "Час:", None))
        self.itemsChoice_5.setItemText(0,
                                       _translate("MainWindow", "8:30 - 10:05",
                                                  None))
        self.itemsChoice_5.setItemText(1,
                                       _translate("MainWindow", "10:25 - 12:00",
                                                  None))
        self.itemsChoice_5.setItemText(2,
                                       _translate("MainWindow", "12:20 - 13:55",
                                                  None))
        self.itemsChoice_5.setItemText(3,
                                       _translate("MainWindow", "14:15 - 15:50",
                                                  None))
        self.itemsChoice_5.setItemText(4,
                                       _translate("MainWindow", "16:10 - 17:45",
                                                  None))
        self.itemsChoice_5.setItemText(5,
                                       _translate("MainWindow", "18:05 - 19:40",
                                                  None))
        self.addButton_2.setText(_translate("MainWindow", "Знайти", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_search),
                                  _translate("MainWindow", "Пошук", None))
        self.menu.setTitle(_translate("MainWindow", "Відображення", None))
        self.menu_2.setTitle(_translate("MainWindow", "Користувач", None))
        self.menu_3.setTitle(_translate("MainWindow", "База даних", None))
        self.actionOneOne.setText(_translate("MainWindow", "OneOne", None))
        self.actionOneTwo.setText(_translate("MainWindow", "OneTwo", None))
        self.action.setText(_translate("MainWindow", "Задати розклад", None))
        self.action_2.setText(
            _translate("MainWindow", "Заявка на реєстрацію", None))
        self.action_3.setText(_translate("MainWindow", "Вхід", None))
        self.action_5.setText(_translate("MainWindow", "Вхід", None))
        self.action_6.setText(_translate("MainWindow", "Вихід", None))
        self.action_7.setText(_translate("MainWindow", "Завантаження", None))
        self.action_9.setText(_translate("MainWindow", "Перевірка", None))
        self.action_10.setText(_translate("MainWindow", "Збереження", None))


def main():
    from random import randint
    lesson_set = [[randint(0, 2) for i in range(5)] for j in range(12)]

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window, lesson_set)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget_menu = QtWidgets.QTabWidget(self.frame)
        self.tabWidget_menu.setObjectName("tabWidget_menu")
        self.tab_ConnectedGitSetup = QtWidgets.QWidget()
        self.tab_ConnectedGitSetup.setObjectName("tab_ConnectedGitSetup")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_ConnectedGitSetup)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_2 = QtWidgets.QFrame(self.tab_ConnectedGitSetup)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.gridLayout_4.addWidget(self.frame_4, 0, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton_SSH = QtWidgets.QRadioButton(self.frame_3)
        self.radioButton_SSH.setChecked(True)
        self.radioButton_SSH.setObjectName("radioButton_SSH")
        self.horizontalLayout.addWidget(self.radioButton_SSH)
        self.radioButton_HTTP = QtWidgets.QRadioButton(self.frame_3)
        self.radioButton_HTTP.setObjectName("radioButton_HTTP")
        self.horizontalLayout.addWidget(self.radioButton_HTTP)
        self.gridLayout_4.addWidget(self.frame_3, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem, 3, 0, 1, 1)
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget_git_url_group = QtWidgets.QListWidget(self.frame_5)
        self.listWidget_git_url_group.setObjectName("listWidget_git_url_group")
        self.verticalLayout.addWidget(self.listWidget_git_url_group)
        self.gridLayout_4.addWidget(self.frame_5, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.frame_2, 0, 0, 1, 1)
        self.tabWidget_menu.addTab(self.tab_ConnectedGitSetup, "")
        self.tab_FmodProjectSetup = QtWidgets.QWidget()
        self.tab_FmodProjectSetup.setObjectName("tab_FmodProjectSetup")
        self.tabWidget_menu.addTab(self.tab_FmodProjectSetup, "")
        self.gridLayout_2.addWidget(self.tabWidget_menu, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget_menu.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GitForFMOD"))
        self.label.setText(_translate("MainWindow", "Method to connect to Git"))
        self.radioButton_SSH.setText(_translate("MainWindow", "SSH"))
        self.radioButton_HTTP.setText(_translate("MainWindow", "HTTP"))
        self.tabWidget_menu.setTabText(self.tabWidget_menu.indexOf(self.tab_ConnectedGitSetup), _translate("MainWindow", "ConnectedGitSetup"))
        self.tabWidget_menu.setTabText(self.tabWidget_menu.indexOf(self.tab_FmodProjectSetup), _translate("MainWindow", "FmodProjectSetup"))
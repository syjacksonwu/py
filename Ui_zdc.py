# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'z:\py\zdc.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(724, 665)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("z:\\py\\ico/vw.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QtCore.QSize(32, 32))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txt_Find = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_Find.setObjectName("txt_Find")
        self.horizontalLayout_3.addWidget(self.txt_Find)
        self.btn_Find = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Find.setObjectName("btn_Find")
        self.horizontalLayout_3.addWidget(self.btn_Find)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setAutoFillBackground(True)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.midleft = QtWidgets.QTreeWidget(self.verticalLayoutWidget_2)
        self.midleft.setObjectName("midleft")
        self.midleft.headerItem().setText(0, "1")
        self.midleft.header().setHighlightSections(True)
        self.verticalLayout_2.addWidget(self.midleft)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cb_Tabelle = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.cb_Tabelle.setFont(font)
        self.cb_Tabelle.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cb_Tabelle.setCheckable(True)
        self.cb_Tabelle.setChecked(False)
        self.cb_Tabelle.setTristate(False)
        self.cb_Tabelle.setObjectName("cb_Tabelle")
        self.horizontalLayout.addWidget(self.cb_Tabelle)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_Update_Tree = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Update_Tree.sizePolicy().hasHeightForWidth())
        self.btn_Update_Tree.setSizePolicy(sizePolicy)
        self.btn_Update_Tree.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("z:\\py\\ico/ARROW6A.ICO"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Update_Tree.setIcon(icon1)
        self.btn_Update_Tree.setIconSize(QtCore.QSize(32, 32))
        self.btn_Update_Tree.setObjectName("btn_Update_Tree")
        self.horizontalLayout.addWidget(self.btn_Update_Tree)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.botleft = QtWidgets.QTreeWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.botleft.sizePolicy().hasHeightForWidth())
        self.botleft.setSizePolicy(sizePolicy)
        self.botleft.setObjectName("botleft")
        self.botleft.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.botleft)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cb_PR = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.cb_PR.setFont(font)
        self.cb_PR.setObjectName("cb_PR")
        self.horizontalLayout_2.addWidget(self.cb_PR)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btn_Dump_pr = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_Dump_pr.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("z:\\py\\ico/ARROW6C.ICO"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Dump_pr.setIcon(icon2)
        self.btn_Dump_pr.setIconSize(QtCore.QSize(32, 32))
        self.btn_Dump_pr.setObjectName("btn_Dump_pr")
        self.horizontalLayout_2.addWidget(self.btn_Dump_pr)
        self.btn_Inject_pr = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_Inject_pr.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("z:\\py\\ico/ARROW6D.ICO"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_Inject_pr.setIcon(icon3)
        self.btn_Inject_pr.setIconSize(QtCore.QSize(32, 32))
        self.btn_Inject_pr.setObjectName("btn_Inject_pr")
        self.horizontalLayout_2.addWidget(self.btn_Inject_pr)
        self.btn_Update_PrNr = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_Update_PrNr.setText("")
        self.btn_Update_PrNr.setIcon(icon1)
        self.btn_Update_PrNr.setIconSize(QtCore.QSize(32, 32))
        self.btn_Update_PrNr.setObjectName("btn_Update_PrNr")
        self.horizontalLayout_2.addWidget(self.btn_Update_PrNr)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.topright = QWebEngineView(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topright.sizePolicy().hasHeightForWidth())
        self.topright.setSizePolicy(sizePolicy)
        self.topright.setObjectName("topright")
        self.verticalLayout_3.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 724, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.openMenu = QtWidgets.QAction(MainWindow)
        self.openMenu.setObjectName("openMenu")
        self.menu.addAction(self.openMenu)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ZDC-Browser, beta-1, by wujianjian"))
        self.btn_Find.setText(_translate("MainWindow", "查找"))
        self.cb_Tabelle.setText(_translate("MainWindow", "全选"))
        self.cb_PR.setText(_translate("MainWindow", "全选"))
        self.menu.setTitle(_translate("MainWindow", "文件(&F)"))
        self.openMenu.setText(_translate("MainWindow", "打开(&O)"))
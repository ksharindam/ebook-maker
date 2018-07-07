# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'files/window.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 460)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.tableWidget)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.moveUpBtn = QtWidgets.QToolButton(self.widget_2)
        self.moveUpBtn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/go-up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.moveUpBtn.setIcon(icon)
        self.moveUpBtn.setIconSize(QtCore.QSize(32, 32))
        self.moveUpBtn.setObjectName("moveUpBtn")
        self.verticalLayout.addWidget(self.moveUpBtn)
        self.moveDownBtn = QtWidgets.QToolButton(self.widget_2)
        self.moveDownBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/go-down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.moveDownBtn.setIcon(icon1)
        self.moveDownBtn.setIconSize(QtCore.QSize(32, 32))
        self.moveDownBtn.setObjectName("moveDownBtn")
        self.verticalLayout.addWidget(self.moveDownBtn)
        self.rotateLeftBtn = QtWidgets.QToolButton(self.widget_2)
        self.rotateLeftBtn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/rotateleft.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rotateLeftBtn.setIcon(icon2)
        self.rotateLeftBtn.setIconSize(QtCore.QSize(32, 32))
        self.rotateLeftBtn.setObjectName("rotateLeftBtn")
        self.verticalLayout.addWidget(self.rotateLeftBtn)
        self.rotateRightBtn = QtWidgets.QToolButton(self.widget_2)
        self.rotateRightBtn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/rotateright.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rotateRightBtn.setIcon(icon3)
        self.rotateRightBtn.setIconSize(QtCore.QSize(32, 32))
        self.rotateRightBtn.setObjectName("rotateRightBtn")
        self.verticalLayout.addWidget(self.rotateRightBtn)
        self.horizontalLayout_2.addWidget(self.widget_2)
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 263, 300))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout2.setObjectName("verticalLayout2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 2)
        self.widget_4 = QtWidgets.QWidget(Dialog)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.addFilesBtn = QtWidgets.QPushButton(self.widget_4)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.addFilesBtn.setIcon(icon)
        self.addFilesBtn.setObjectName("addFilesBtn")
        self.horizontalLayout_3.addWidget(self.addFilesBtn)
        self.removeFileBtn = QtWidgets.QPushButton(self.widget_4)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.removeFileBtn.setIcon(icon)
        self.removeFileBtn.setObjectName("removeFileBtn")
        self.horizontalLayout_3.addWidget(self.removeFileBtn)
        self.clearListBtn = QtWidgets.QPushButton(self.widget_4)
        icon = QtGui.QIcon.fromTheme("edit-clear")
        self.clearListBtn.setIcon(icon)
        self.clearListBtn.setObjectName("clearListBtn")
        self.horizontalLayout_3.addWidget(self.clearListBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.gridLayout.addWidget(self.widget_4, 1, 0, 1, 1)
        self.clearBgBtn = QtWidgets.QCheckBox(Dialog)
        self.clearBgBtn.setChecked(True)
        self.clearBgBtn.setObjectName("clearBgBtn")
        self.gridLayout.addWidget(self.clearBgBtn, 1, 1, 1, 1)
        self.widget_5 = QtWidgets.QWidget(Dialog)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widget_5)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.filenameEdit = QtWidgets.QLineEdit(self.widget_5)
        self.filenameEdit.setObjectName("filenameEdit")
        self.verticalLayout_2.addWidget(self.filenameEdit)
        self.gridLayout.addWidget(self.widget_5, 2, 0, 1, 1)
        self.widget_3 = QtWidgets.QWidget(Dialog)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setContentsMargins(0, 22, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.closeBtn = QtWidgets.QPushButton(self.widget_3)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/quit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeBtn.setIcon(icon4)
        self.closeBtn.setIconSize(QtCore.QSize(24, 24))
        self.closeBtn.setObjectName("closeBtn")
        self.horizontalLayout_4.addWidget(self.closeBtn)
        self.createPdfBtn = QtWidgets.QPushButton(self.widget_3)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/pdf.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createPdfBtn.setIcon(icon5)
        self.createPdfBtn.setIconSize(QtCore.QSize(24, 24))
        self.createPdfBtn.setDefault(True)
        self.createPdfBtn.setObjectName("createPdfBtn")
        self.horizontalLayout_4.addWidget(self.createPdfBtn)
        self.gridLayout.addWidget(self.widget_3, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "eBook Maker ( Image to PDF )"))
        self.moveUpBtn.setToolTip(_translate("Dialog", "Move up"))
        self.moveDownBtn.setToolTip(_translate("Dialog", "Move down"))
        self.rotateLeftBtn.setToolTip(_translate("Dialog", "Rotate left"))
        self.rotateRightBtn.setToolTip(_translate("Dialog", "Rotate right"))
        self.addFilesBtn.setText(_translate("Dialog", "Add"))
        self.removeFileBtn.setText(_translate("Dialog", "Remove"))
        self.clearListBtn.setText(_translate("Dialog", "Clear"))
        self.clearBgBtn.setText(_translate("Dialog", "Clear Background"))
        self.label.setText(_translate("Dialog", "Filename :"))
        self.closeBtn.setToolTip(_translate("Dialog", "Esc"))
        self.closeBtn.setText(_translate("Dialog", "Close"))
        self.createPdfBtn.setText(_translate("Dialog", "Create PDF"))

import resources_rc

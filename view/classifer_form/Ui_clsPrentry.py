# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_clsPrentry.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_clsPrentryForm(object):
    def setupUi(self, Prentry):
        Prentry.setObjectName("Prentry")
        Prentry.resize(700, 600)
        self.gridLayout_2 = QtWidgets.QGridLayout(Prentry)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(Prentry)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnConfirm = QtWidgets.QPushButton(Prentry)
        self.btnConfirm.setObjectName("btnConfirm")
        self.horizontalLayout.addWidget(self.btnConfirm)
        self.btnReturn = QtWidgets.QPushButton(Prentry)
        self.btnReturn.setObjectName("btnReturn")
        self.horizontalLayout.addWidget(self.btnReturn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Prentry)
        QtCore.QMetaObject.connectSlotsByName(Prentry)

    def retranslateUi(self, Prentry):
        _translate = QtCore.QCoreApplication.translate
        Prentry.setWindowTitle(_translate("Prentry", "配置信息选择"))
        self.btnConfirm.setText(_translate("Prentry", "确认"))
        self.btnReturn.setText(_translate("Prentry", "返回"))
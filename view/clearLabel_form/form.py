# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClearLabelForm(object):
    def setupUi(self, ClearLabelForm):
        ClearLabelForm.setObjectName("ClearLabelForm")
        ClearLabelForm.resize(1080, 720)
        self.verticalLayout = QtWidgets.QVBoxLayout(ClearLabelForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboCond = QtWidgets.QComboBox(ClearLabelForm)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.comboCond.setFont(font)
        self.comboCond.setObjectName("comboCond")
        self.horizontalLayout.addWidget(self.comboCond)
        self.lineValue = QtWidgets.QLineEdit(ClearLabelForm)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lineValue.setFont(font)
        self.lineValue.setObjectName("lineValue")
        self.horizontalLayout.addWidget(self.lineValue)
        self.btnSelect = QtWidgets.QPushButton(ClearLabelForm)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btnSelect.setFont(font)
        self.btnSelect.setObjectName("btnSelect")
        self.horizontalLayout.addWidget(self.btnSelect)
        self.btnReset = QtWidgets.QPushButton(ClearLabelForm)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.btnReset.setFont(font)
        self.btnReset.setObjectName("btnReset")
        self.horizontalLayout.addWidget(self.btnReset)
        self.btnAssess = QtWidgets.QPushButton(ClearLabelForm)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.btnAssess.setFont(font)
        self.btnAssess.setObjectName("btnAssess")
        self.horizontalLayout.addWidget(self.btnAssess)
        self.btnDel = QtWidgets.QPushButton(ClearLabelForm)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.btnDel.setFont(font)
        self.btnDel.setObjectName("btnDel")
        self.horizontalLayout.addWidget(self.btnDel)
        self.btnDelAll = QtWidgets.QPushButton(ClearLabelForm)
        self.btnDelAll.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.btnDelAll.setFont(font)
        self.btnDelAll.setIconSize(QtCore.QSize(16, 16))
        self.btnDelAll.setObjectName("btnDelAll")
        self.horizontalLayout.addWidget(self.btnDelAll)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(ClearLabelForm)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnReturn = QtWidgets.QPushButton(ClearLabelForm)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.btnReturn.setFont(font)
        self.btnReturn.setObjectName("btnReturn")
        self.horizontalLayout.addWidget(self.btnReturn)
        self.horizontalLayout.setStretch(7, 5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(ClearLabelForm)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(ClearLabelForm)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(ClearLabelForm)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.label_2 = QtWidgets.QLabel(ClearLabelForm)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.pushButton_3 = QtWidgets.QPushButton(ClearLabelForm)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(ClearLabelForm)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.label_3 = QtWidgets.QLabel(ClearLabelForm)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.label_4 = QtWidgets.QLabel(ClearLabelForm)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lineEdit = QtWidgets.QLineEdit(ClearLabelForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.pushButton_5 = QtWidgets.QPushButton(ClearLabelForm)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.verticalLayout.setStretch(1, 8)
        self.verticalLayout.setStretch(3, 1)

        self.retranslateUi(ClearLabelForm)
        QtCore.QMetaObject.connectSlotsByName(ClearLabelForm)

    def retranslateUi(self, ClearLabelForm):
        _translate = QtCore.QCoreApplication.translate
        ClearLabelForm.setWindowTitle(_translate("ClearLabelForm", "Form"))
        self.btnSelect.setText(_translate("ClearLabelForm", "查询"))
        self.btnReset.setText(_translate("ClearLabelForm", "重置"))
        self.btnAssess.setText(_translate("ClearLabelForm", "已评估"))
        self.btnDel.setText(_translate("ClearLabelForm", "删除"))
        self.btnDelAll.setText(_translate("ClearLabelForm", "删除全部"))
        self.label.setText(_translate("ClearLabelForm", "text"))
        self.btnReturn.setText(_translate("ClearLabelForm", "返回"))
        self.pushButton.setText(_translate("ClearLabelForm", "首页"))
        self.pushButton_2.setText(_translate("ClearLabelForm", "上一页"))
        self.label_2.setText(_translate("ClearLabelForm", "TextLabel"))
        self.pushButton_3.setText(_translate("ClearLabelForm", "下一页"))
        self.pushButton_4.setText(_translate("ClearLabelForm", "尾页"))
        self.label_3.setText(_translate("ClearLabelForm", "TextLabel"))
        self.label_4.setText(_translate("ClearLabelForm", "跳到第："))
        self.pushButton_5.setText(_translate("ClearLabelForm", "确定"))

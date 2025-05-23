# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1190, 822)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        # spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout.addItem(spacerItem1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(16)
        self.addButton = QtWidgets.QPushButton(Form)
        self.addButton.setMinimumSize(QtCore.QSize(120, 0))
        self.addButton.setMaximumSize(QtCore.QSize(90, 16777215))
        # font.setBold(True)
        # font.setWeight(75)
        self.addButton.setFont(font)
#         self.addButton.setStyleSheet("background-color: rgb(255, 0, 0);\n"
# "color: rgb(255, 255, 255);")
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.delButton = QtWidgets.QPushButton(Form)
        self.delButton.setMinimumSize(QtCore.QSize(120, 0))
        self.delButton.setMaximumSize(QtCore.QSize(90, 16777215))
        # font.setBold(True)
        # font.setWeight(75)
        self.delButton.setFont(font)
#         self.delButton.setStyleSheet("background-color: rgb(255, 0, 0);\n"
# "color: rgb(255, 255, 255);")
        self.delButton.setObjectName("delButton")
        self.horizontalLayout.addWidget(self.delButton)
        self.editButton = QtWidgets.QPushButton(Form)
        self.editButton.setEnabled(True)
        self.editButton.setMinimumSize(QtCore.QSize(120, 0))
        self.editButton.setMaximumSize(QtCore.QSize(90, 16777215))

        # font.setBold(True)
        # font.setWeight(75)
        self.editButton.setFont(font)
#         self.editButton.setStyleSheet("background-color: rgb(255, 0, 0);\n"
# "color: rgb(255, 255, 255);")
        self.editButton.setObjectName("editButton")
        self.horizontalLayout.addWidget(self.editButton)
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignCenter)

        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(Form)

        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setMaximumSize(QtCore.QSize(300, 31))

        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(Form)

        # font.setBold(True)
        # font.setWeight(75)
        self.pushButton.setFont(font)
        # self.pushButton.setStyleSheet("background-color: rgb(255, 0, 0);\n"
        #                               "color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(Form)

        # font.setBold(True)
        # font.setWeight(75)
        self.pushButton_2.setFont(font)
        # self.pushButton_2.setStyleSheet("background-color: rgb(255, 0, 0);\n"
        #                                 "color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.setStretch(3, 8)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.addButton.setText(_translate("Form", "新增病人"))
        self.delButton.setText(_translate("Form", "病人删除"))
        self.editButton.setText(_translate("Form", "病人修改"))

        self.label.setText(_translate("Form", "关键字："))
        self.comboBox.setItemText(0, _translate("Form", "姓名"))
        self.comboBox.setItemText(1, _translate("Form", "医保卡号"))
        self.comboBox.setItemText(2, _translate("Form", "电话号码"))
        self.pushButton.setText(_translate("Form", "搜索"))
        self.pushButton_2.setText(_translate("Form", "重置"))

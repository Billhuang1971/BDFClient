# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QLineEdit

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1190, 822)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(16)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.label.setFont(font)
        self.horizontalLayout.addWidget(self.label)

        self.theme_lineEdit = QtWidgets.QLineEdit(Form)
        self.theme_lineEdit.setEnabled(True)
        self.theme_lineEdit.setObjectName("theme_lineEdit")
        self.theme_lineEdit.setFont(font)
        self.theme_lineEdit.setMaximumSize(QtCore.QSize(120, 26))
        self.horizontalLayout.addWidget(self.theme_lineEdit)

        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setObjectName("label1")
        self.label1.setFont(font)
        self.horizontalLayout.addWidget(self.label1)

        self.comboBox = QtWidgets.QComboBox(Form)

        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("labelling")
        self.comboBox.addItem("evaluating")
        self.comboBox.addItem("notUsable")
        self.comboBox.addItem("usable")
        self.horizontalLayout.addWidget(self.comboBox)

        self.label2 = QtWidgets.QLabel(Form)

        self.label2.setObjectName("label2")
        self.label2.setFont(font)
        self.horizontalLayout.addWidget(self.label2)

        self.comboBox2 = QtWidgets.QComboBox(Form)

        self.comboBox2.addItem("")
        self.comboBox2.addItem("notStarted")
        self.comboBox2.addItem("labelling")
        self.comboBox2.addItem("labelled")
        self.comboBox2.addItem("qualified")
        self.comboBox2.addItem("notqualified")
        self.comboBox2.setFont(font)
        self.comboBox2.setObjectName("comboBox2")
        self.horizontalLayout.addWidget(self.comboBox2)

        self.pushButton = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(16)
        self.pushButton.setFont(font)
        #self.pushButton.setStyleSheet("background-color: rgb(192, 192, 192);color: rgb(0, 0, 255);")
        self.pushButton.setObjectName("pushButton")

        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setStyleSheet("font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setGeometry(QRect(5, 40, 1780, 760))
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)

        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableWidget)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPixelSize(18)

        self.horizontalLayout_paging = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_paging.setObjectName("horizontalLayout_paging")

        self.horizontalLayout_paging.setSpacing(0)
        self.horizontalLayout_paging.setAlignment(Qt.AlignRight)

        self.homePage = QtWidgets.QPushButton(Form)
        self.homePage.setObjectName("homePage")
        self.homePage.setFont(font)

        self.homePage.setMaximumSize(QtCore.QSize(60, 45))
        self.horizontalLayout_paging.addWidget(self.homePage)

        self.prePage = QtWidgets.QPushButton(Form)
        self.prePage.setObjectName("prePage")
        self.prePage.setFont(font)
        self.prePage.setMaximumSize(QtCore.QSize(100, 45))
        self.horizontalLayout_paging.addWidget(self.prePage)

        self.curPage = QLineEdit(Form)
        self.curPage.setObjectName("curPage")
        self.curPage.setFont(font)
        self.curPage.setMaximumSize(QtCore.QSize(100, 45))
        self.curPage.setReadOnly(True)
        self.curPage.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_paging.addWidget(self.curPage)

        self.nextPage = QtWidgets.QPushButton(Form)
        self.nextPage.setObjectName("nextPage")
        self.nextPage.setFont(font)
        self.nextPage.setMaximumSize(QtCore.QSize(100, 45))
        self.horizontalLayout_paging.addWidget(self.nextPage)

        self.finalPage = QtWidgets.QPushButton(Form)
        self.finalPage.setObjectName("finalPage")
        self.finalPage.setFont(font)
        self.finalPage.setMaximumSize(QtCore.QSize(60, 45))
        self.horizontalLayout_paging.addWidget(self.finalPage)

        self.totalPage = QLabel(Form)
        self.totalPage.setObjectName("totalPage")
        self.totalPage.setFont(font)
        self.totalPage.setMaximumSize(QtCore.QSize(100, 26))
        self.horizontalLayout_paging.addWidget(self.totalPage)

        self.skipLable_0 = QLabel(Form)
        self.skipLable_0.setObjectName("totalPage")
        self.skipLable_0.setFont(font)
        self.skipLable_0.setMaximumSize(QtCore.QSize(70, 30))
        self.horizontalLayout_paging.addWidget(self.skipLable_0)

        self.skipPage = QLineEdit(Form)
        self.skipPage.setObjectName("skipPage")
        self.skipPage.setFont(font)
        self.skipPage.setMaximumSize(QtCore.QSize(48, 32))
        self.skipPage.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_paging.addWidget(self.skipPage)

        self.skipLabel_1 = QLabel(Form)
        self.skipLabel_1.setObjectName("skipLabel_1")
        self.skipLabel_1.setFont(font)
        self.skipLabel_1.setMaximumSize(QtCore.QSize(30, 45))
        self.horizontalLayout_paging.addWidget(self.skipLabel_1)

        self.confirmSkip = QtWidgets.QPushButton(Form)
        self.confirmSkip.setObjectName("confirmSkip")
        self.confirmSkip.setFont(font)
        self.confirmSkip.setMaximumSize(QtCore.QSize(60, 45))
        self.horizontalLayout_paging.addWidget(self.confirmSkip)

        self.verticalLayout.addLayout(self.horizontalLayout_paging)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "[诊断查询]诊断信息列表"))

        self.pushButton.setText(_translate("Form", "查询"))

        self.homePage.setText(_translate("Form", "首页"))
        self.prePage.setText(_translate("Form", "上一页"))
        self.curPage.setText(_translate("Form", "1"))
        self.nextPage.setText(_translate("Form", "下一页"))
        self.finalPage.setText(_translate("Form", "末页"))
        self.totalPage.setText(_translate("Form", "共1页"))
        self.skipLable_0.setText(_translate("Form", "跳到第:"))
        self.skipPage.setText(_translate("Form", "1"))
        self.skipLabel_1.setText(_translate("Form", "页"))
        self.confirmSkip.setText(_translate("Form", "确定"))

        self.label.setText(_translate("Form", "主题名:"))
        self.label1.setText(_translate("Form", "主题状态:"))
        self.label2.setText(_translate("Form", "任务状态:"))



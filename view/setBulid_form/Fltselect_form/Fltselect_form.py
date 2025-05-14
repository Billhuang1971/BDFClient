from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FltsetselectForm(object):
    def setupUi(self, set_table):
        set_table.setObjectName("set_table")
        set_table.resize(1080, 640)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(set_table.sizePolicy().hasHeightForWidth())
        set_table.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(set_table)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_set = QtWidgets.QTableWidget(set_table)
        self.tableWidget_set.setObjectName("tableWidget_set")
        self.tableWidget_set.setColumnCount(0)
        self.tableWidget_set.setRowCount(0)


        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineValue = QtWidgets.QLineEdit(set_table)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineValue.setFont(font)
        self.lineValue.setObjectName("lineValue1")
        self.horizontalLayout.addWidget(self.lineValue)
        self.btnSelect1 = QtWidgets.QPushButton(set_table)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.btnSelect1.setFont(font)
        self.btnSelect1.setObjectName("btnSelect1")
        self.horizontalLayout.addWidget(self.btnSelect1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.tableWidget_set)


        self.retranslateUi(set_table)
        QtCore.QMetaObject.connectSlotsByName(set_table)

    def retranslateUi(self, set_table):
        _translate = QtCore.QCoreApplication.translate
        self.btnSelect1.setText(_translate("set_table", "查询"))
        set_table.setWindowTitle(_translate("set_table", "Form"))

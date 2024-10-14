from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class renameView(QDialog):
    def __init__(self, parent=None, thread=None):
        super(renameView, self).__init__(parent)
        self.thread = thread
        self.init_view()

    def init_view(self):
        self.setWindowTitle("导入集合名称冲突，请重命名")
        self.setFixedSize(240, 100)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.spaceItem_1 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spaceItem_2 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        name = QLabel("集合名称：")
        self.input_lineedit = QLineEdit()
        self.comfirm_button = QPushButton("确认修改")
        font = QFont()
        font.setPointSize(12)
        font1 = QFont()
        font1.setPointSize(9)
        name.setFont(font)
        self.comfirm_button.setFont(font)
        self.input_lineedit.setFont(font1)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        spaceItem1 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spaceItem2 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout_1.addWidget(name)
        self.horizontalLayout_1.addWidget(self.input_lineedit)
        self.horizontalLayout_2.addItem(spaceItem1)
        self.horizontalLayout_2.addWidget(self.comfirm_button)
        self.horizontalLayout_2.addItem(spaceItem2)

        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)



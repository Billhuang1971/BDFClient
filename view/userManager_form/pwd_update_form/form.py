from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore


class pwdUpdateView(QDialog):
    comfirm_signal = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None, controller=None, update_account=None):
        super(pwdUpdateView, self).__init__(parent)
        self.update_account = update_account
        self.controller = controller
        self.controller.update_done_signal.connect(self.update_done)
        self.init_view()
        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    def init_view(self):
        self.setWindowTitle("密码修改")
        self.setFixedSize(240, 100)
        self.spaceItem_1 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spaceItem_2 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        name = QLabel("新密码：")
        self.input_lineedit = QLineEdit()
        self.comfirm_button = QPushButton("确认修改")
        self.comfirm_button.clicked.connect(self.comfirm_emit)
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

    def comfirm_emit(self):
        self.comfirm_signal.emit(self.update_account, self.input_lineedit.text())

    def update_done(self, tag):
        try:
            if tag[0]:
                QMessageBox.information(self, '提示', '密码修改成功！')
                self.close()
            elif tag[0] == False and tag[1] == 0:
                QMessageBox.information(self, "提示", "该用户已经在线,无法修改信息", QMessageBox.Yes)
                self.close()
            elif tag[0] == False and tag[1] == 1:
                QMessageBox.information(self, '提示', '密码修改失败！')
                self.close()
        except Exception as e:
            print('update_done', e)
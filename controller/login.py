from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QLineEdit
from view.login import LoginView
from PyQt5.Qt import *
import sys
import pickle, os
import json


class loginController(QWidget, QObject):
    signal_login_user_info = pyqtSignal()

    def __init__(self, client, cAppUtil):
        super().__init__()
        self.view = LoginView()
        self.cAppUtil = cAppUtil

        self.line_1 = self.view.ui.lineEdit
        self.line_2 = self.view.ui.lineEdit_2
        self.line_2.setEchoMode(QLineEdit.Password)

        self.client = client
        self.client.loginResSig.connect(self.loginRes)
        self.view.ui.pushButton.clicked.connect(self.login)
        self.line_1.returnPressed.connect(self.login)
        self.line_2.returnPressed.connect(self.login)

        self.view.show()

    # 登录
    def login(self):
        self.view.ui.pushButton.setDisabled(True)
        account = self.line_1.text()
        pwd = self.cAppUtil.md5_string(self.line_2.text())
        msg = [account, pwd]
        print(f'Msg: {msg}')
        self.client.login(msg)

    def loginRes(self, case, msg):
        if case == 0:
            QMessageBox.information(self, "登录", f'用户名或密码错误', QMessageBox.Yes)
        elif case == 1:
            QMessageBox.information(self, "登录", f'登录成功', QMessageBox.Yes)

            self.signal_login_user_info.emit()
            self.view.close()
        elif case == 2:
            QMessageBox.information(self, "登录", f'MAC地址异常', QMessageBox.Yes)
        else:
            QMessageBox.information(self, "登录", f'当前用户不存在', QMessageBox.Yes)
        self.view.ui.pushButton.setEnabled(True)

    def exit(self):
        print(f'Login Exit')
        self.client.loginResSig.disconnect()

    def disconnect_login(self):
        self.line_1.returnPressed.disconnect(self.login)
        self.line_2.returnPressed.disconnect(self.login)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = loginController()
    sys.exit(app.exec_())

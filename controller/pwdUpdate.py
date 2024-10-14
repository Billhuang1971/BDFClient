from view.pwdUpdate import PwdUpdateView
from PyQt5.QtWidgets import *
from util.clientAppUtil import clientAppUtil
import sys


# 密码修改模块

class pwdController(QWidget):
    def __init__(self, client, cAppUtil):
        super().__init__()
        self.client = client
        self.client.changePwdResSig.connect(self.pwdRes)
        self.view = PwdUpdateView()
        self.cAppUtil = cAppUtil
        self.view.ui.lineEdit.setEchoMode(QLineEdit.Password)
        self.view.ui.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.view.ui.lineEdit_4.setEchoMode(QLineEdit.Password)
        self.view.ui.pushButton.clicked.connect(self.checkPwd)
        # self.view.show()

    def checkPwd(self):
        # e_pwd = self.client.
        line_2 = self.view.ui.lineEdit_2.text()
        line_4 = self.view.ui.lineEdit_4.text()
        if line_4 != line_2:
            QMessageBox.information(self, "密码修改", "新密码不一致！！", QMessageBox.Yes)
            self.view.ui.lineEdit_2.clear()
            self.view.ui.lineEdit_4.clear()
            return
        else:
            oldPwd = self.cAppUtil.md5_string(self.view.ui.lineEdit.text())
            newPwd = self.cAppUtil.md5_string(line_2)
            REQmsg = [self.client.tUser[0], self.client.tUser[1], oldPwd, newPwd]
            print(f'REQMSG: {REQmsg}')
            self.client.changePwd(REQmsg)

    def pwdRes(self, REPData):
        if REPData[0] == '1':
            QMessageBox.information(self,"密码修改",REPData[2],QMessageBox.Yes)
            self.view.ui.lineEdit.clear()
            self.view.ui.lineEdit_2.clear()
            self.view.ui.lineEdit_4.clear()
        elif REPData[0] == '0':
            QMessageBox.information(self, "密码修改", f'密码修改失败：{REPData[2]}', QMessageBox.Yes)
            self.view.ui.lineEdit.clear()
        else:
            QMessageBox.information(self, "密码修改", f'密码修改失败!出现其它错误，请重新修改', QMessageBox.Yes)
            self.view.ui.lineEdit.clear()
            self.view.ui.lineEdit_2.clear()
            self.view.ui.lineEdit_4.clear()

    def exit(self):
        self.client.changePwdResSig.disconnect()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    comtroller = pwdController()
    sys.exit(app.exec_())

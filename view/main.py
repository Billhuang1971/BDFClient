import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget

from view.main_form.form import Ui_MainWindow

_translate = QtCore.QCoreApplication.translate


class MainView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.user = ""

        # 全屏
        self.showMaximized()

        style_sheet = """
                    QLabel{
                        margin-left: 10px;
                        font-size: 20px;
                    }
                """
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.MyWidget = QWidget()
        self.verticalLayout_1.addWidget(self.MyWidget)
        self.downBar = QtWidgets.QWidget()
        self.downBar.setStyleSheet("background-color: white")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.downBar)
        self.label_1 = QtWidgets.QLabel()
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel()
        self.label_3.setObjectName("label_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)

        # 提供给初始/评估标注 用于显示相关参数信息
        self.label_4 = QtWidgets.QLabel()
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel()

        self.label_5.setObjectName("label_5")
        self.label_5.hide()

        self.horizontalLayout.addWidget(self.label_1)
        self.horizontalLayout.addWidget(self.label_2)
        self.horizontalLayout.addWidget(self.label_3)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.label_4)
        self.horizontalLayout.addItem(spacerItem)
        # self.horizontalLayout.setStretch(3, 1)

        _translate = QtCore.QCoreApplication.translate
        self.label_1.setText(_translate("MainWindow", "当前位置："))
        self.label_2.setText(_translate("MainWindow", "当前用户："))
        self.label_3.setText(_translate("MainWindow", "当前身份："))
        self.label_4.setText(_translate("MainWindow", ""))

        self.ui.verticalLayout.addLayout(self.verticalLayout_1)
        self.ui.verticalLayout.addWidget(self.downBar)
        # self.ui.verticalLayout.addLayout(self.horizontalLayout)
        self.ui.verticalLayout.setStretch(0, 1)
        # self.ui.verticalLayout.setStretch(1, 0)
        self.label_1.setStyleSheet(style_sheet)
        self.label_2.setStyleSheet(style_sheet)
        self.label_3.setStyleSheet(style_sheet)
        self.label_4.setStyleSheet(style_sheet)
        self.disabel_function_button()

    # 禁止使用菜单选项
    def disabel_function_button(self):
        self.ui.menubar.setEnabled(False)

    # 允许使用菜单选项
    def enabel_function_button(self):
        self.ui.menubar.setEnabled(True)
    def updateForEEG(self,sub_view):
        while self.verticalLayout_1.count() > 1:
            witem = self.verticalLayout_1.itemAt(self.verticalLayout_1.count() - 1)
            witem.widget().hide()
            self.verticalLayout_1.removeItem(witem)
        sub_view.showMaximized()
        self.verticalLayout_1.addWidget(sub_view)
        self.label_4.setText("")
    # 设置用户的姓名和身份、工具栏访问权限
    def setUserPermission(self, client):
        self.client = client
        userInfo = self.client.tUser
        print(f'authority: {userInfo[14]}')
        for i in range(2, 34):
            if i != 11 and i != 26 and i != 13:
                exec('self.ui.action_UC{:0>2d}.setEnabled(True)'.format(i))
        for i in userInfo[14]:
            exec('self.ui.action_UC{:02}.setEnabled(False)'.format(i))
        userList = ['管理员', '标注员', '学员', '培训导师', '医生', '研究员']
        identity = ''
        if userInfo[5]:
            identity = userList[0]
        else:
            for position, i in enumerate(userInfo[6:11]):
                if i:
                    identity += f'{userList[position + 1]}\\'
            identity = identity[:-1]
        self.label_2.setText(_translate("MainWindow", "当前用户:{}".format(userInfo[2])))
        self.label_3.setText(_translate("MainWindow", "当前身份：{}".format(identity)))

    def setPosition(self, m_name, b_name):
        if m_name is None:
            self.label_1.setText(_translate("MainWindow", "当前位置： "))
            return
        self.label_1.setText(
            _translate("MainWindow", "当前位置：{}>{}".format(m_name, b_name)))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        studyInfo = self.label_5.text()
        if studyInfo is not None and studyInfo != '':
            QMessageBox.information(self, '提示', '当前正在[诊断学习]中，请先单击[诊断学习]窗口右边的”返回“，之后再关闭退出。',
                                    QMessageBox.Yes)
            a0.ignore()
            return
        reply = QMessageBox.information(self, '提示', '是否退出程序', QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:

                app = QApplication.instance()
                try:
                    self.client.logout('quit')
                except:
                    pass
                 # 退出应用程序
                app.quit()
        else:
            a0.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainView()
    view.show()
    sys.exit(app.exec_())

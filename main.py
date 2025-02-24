import sys

from PyQt5.QtCore import Qt

# from IPython.external.qt_for_kernel import QtCore

from controller.main import MainController
from PyQt5.QtWidgets import *
from util.client import client
from util.clientAppUtil import clientAppUtil

## 测试
##test Seeg
class clientApp(QWidget):
    def __init__(self):
        super().__init__()
        self.cAppUtil = clientAppUtil()
        s_ip, s_port = self.cAppUtil.GetSocketIpFile()
        self.client = client(s_ip=s_ip, s_port=s_port, cAppUtil=self.cAppUtil)
        self.controller = MainController(cAppUtil=self.cAppUtil, client=self.client)


if __name__ == '__main__':
    # # 设置高分辨率屏幕自适应
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 启用高 DPI 缩放
    # QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    a = clientApp()
    sys.exit(app.exec_())

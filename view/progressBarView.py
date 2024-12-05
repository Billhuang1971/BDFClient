import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog

from view.progressBar_form.progressBar import Ui_progressbar


class ProgressBarView(QDialog):
    # window_title: 窗口名称，默认为""
    # maximum: 进度条最大值， 默认值为0（无进度）
    # hasStopBtn: 是否显示取消按钮， 默认为True
    # speed: 进度条流速，默认为1
    def __init__(self, parent=None, window_title="", maximum=100, hasStopBtn=True, speed=100):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.window_title = window_title
        self.maximum = maximum
        self.hasStopBtn = hasStopBtn
        self.pv = 0
        self.nPv = 0
        self.speed = speed
        self.ui = Ui_progressbar(window_title=self.window_title)
        self.ui.setupUi(self)
        self.ui.progressBar.setMaximum(self.maximum)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setValue(self.pv)
        if hasStopBtn is False:
            self.ui.stop_pushButton.hide()
        else:
            self.ui.stop_pushButton.setText("退出上传")  # 设置按钮显示文本
        QApplication.processEvents()

    # 更新当前进度值，进度条会以speed速度到达该值，到达该值后停止
    def updateProgressBar(self, pv):
        self.nPv = pv if pv <= self.maximum else self.maximum
        while self.pv < self.nPv:
            self.pv += self.speed if self.pv + self.speed <= self.nPv else self.nPv - self.pv
            self.ui.progressBar.setValue(self.pv)
            QApplication.processEvents()
            time.sleep(0.5)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = ProgressBarView(window_title="测试", maximum=50, hasStopBtn=False)
    view.updateProgressBar(120)
    sys.exit(app.exec_())
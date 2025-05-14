import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QWidget
from PyQt5.QtCore import Qt

class channelselectView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 设置窗口标题和初始大小
        self.setWindowTitle('通道选择')
        self.setGeometry(100, 100, 800, 600)  # 增大窗口尺寸

        main_layout = QVBoxLayout()

        # 标题标签
        title = QLabel('请选择通道：', self)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title)

        # 创建滚动区域（应对大量选项）
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)

        # 内容布局（网格布局）
        content_widget = QWidget()
        self.grid_layout = QGridLayout(content_widget)
        self.grid_layout.setVerticalSpacing(5)
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)

        # 配置参数
        self.checkboxes = []
        options = ['Default', 'FP1-REF', 'FPZ-REF', 'FP2-REF', 'AF7-REF', 'AF3-REF', 'AFZ-REF', 'AF4-REF',
                   'AF8-REF',
                   'F9-REF', 'F7-REF', 'F5-REF', 'F3-REF', 'F1-REF', 'FZ-REF', 'F2-REF', 'F4-REF', 'F6-REF',
                   'F8-REF',
                   'F10-REF', 'FT9-REF', 'FT7-REF', 'FC5-REF', 'FC3-REF', 'FC1-REF', 'FCZ-REF', 'FC2-REF',
                   'FC4-REF',
                   'FC6-REF', 'FT8-REF', 'FT10-REF', 'LPA/M1-REF', 'RPA/M2-REF', 'T7-REF', 'C5-REF', 'C3-REF',
                   'C1-REF',
                   'CZ-REF', 'C2-REF', 'C4-REF', 'C6-REF', 'T8-REF', 'TP9-REF', 'TP7-REF', 'CP5-REF', 'CP3-REF',
                   'CP1-REF',
                   'CPZ-REF', 'CP2-REF', 'CP4-REF', 'CP6-REF', 'TP8-REF', 'TP10-REF', 'P9-REF', 'P7-REF',
                   'P5-REF', 'P3-REF',
                   'P1-REF', 'PZ-REF', 'P2-REF', 'P4-REF', 'P6-REF', 'P8-REF', 'P10-REF', 'PO7-REF', 'PO3-REF',
                   'POZ-REF',
                   'PO4-REF', 'PO8-REF', 'O1-REF', 'OZ-REF', 'O2-REF', 'CB1-REF', 'CB2-REF']

        # 配置网格参数
        cols = 5  # 每行显示5个选项
        rows = len(options) // cols + 1  # 自动计算行数

        # 动态创建复选框
        for i, text in enumerate(options):
            row = i // 5  # 每行5列
            col = i % 5
            checkbox = QCheckBox(text, content_widget)

            font = QtGui.QFont()
            font.setPixelSize(18)
            checkbox.setFont(font)

            # 设置默认状态：只有Default默认选中
            checkbox.setChecked(text == 'Default')

            checkbox.stateChanged.connect(self.on_checkbox_state_changed)
            self.checkboxes.append(checkbox)
            self.grid_layout.addWidget(checkbox, row, col)

        # 添加确认按钮
        self.btn_confirm = QPushButton('确认选择', self)
        self.btn_confirm.setStyleSheet("font-size: 16px; padding: 10px;")
        self.btn_cancel=QPushButton('取消', self)
        self.btn_cancel.setStyleSheet("font-size: 16px; padding: 10px;")
        # 组合布局
        main_layout.addWidget(scroll)
        btnlayout=QHBoxLayout()
        btnlayout.addWidget(self.btn_confirm)
        btnlayout.addWidget(self.btn_cancel)
        scroll.setWidget(content_widget)
        main_layout.addLayout(btnlayout)
        self.setLayout(main_layout)

    def on_checkbox_state_changed(self, state):
        checkbox = self.sender()
        if not checkbox:
            return

        # 处理Default的互斥逻辑
        if checkbox.text() == 'Default':
            if state == Qt.Checked:
                for cb in self.checkboxes:
                    if cb != checkbox:
                        cb.setChecked(False)
        else:
            # 处理其他选项的互斥逻辑
            if state == Qt.Checked:
                default_cb = next((cb for cb in self.checkboxes if cb.text() == 'Default'), None)
                if default_cb and default_cb.isChecked():
                    default_cb.setChecked(False)



class channelimportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('通道选择')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()

        # 标题标签
        title = QLabel('请选择通道：', self)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title)

        # 输入框
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("输入新选项后按回车")
        self.input.setStyleSheet("font-size: 16px;")
        main_layout.addWidget(self.input)
        self.input.returnPressed.connect(self.add_new_checkbox)

        # 滚动区域
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)

        # 内容布局
        content_widget = QWidget()
        self.grid_layout = QGridLayout(content_widget)
        self.grid_layout.setVerticalSpacing(5)
        self.grid_layout.setHorizontalSpacing(20)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)

        # 初始化默认复选框
        self.checkboxes = []
        self.default_checkbox = QCheckBox('Default', content_widget)
        font = QtGui.QFont()
        font.setPixelSize(18)
        self.default_checkbox.setFont(font)
        self.default_checkbox.setChecked(True)
        self.default_checkbox.stateChanged.connect(self.on_checkbox_state_changed)
        self.checkboxes.append(self.default_checkbox)
        self.grid_layout.addWidget(self.default_checkbox, 0, 0)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # 确认按钮
        btnlayout = QHBoxLayout()
        self.btn_confirm = QPushButton('确认选择', self)
        self.btn_confirm.setStyleSheet("font-size: 16px; padding: 10px;")
        self.btn_cancel = QPushButton('取消', self)
        self.btn_cancel.setStyleSheet("font-size: 16px; padding: 10px;")
        btnlayout.addWidget(self.btn_confirm)
        btnlayout.addWidget(self.btn_cancel)
        main_layout.addLayout(btnlayout)

        self.setLayout(main_layout)

    def add_new_checkbox(self):
        text = self.input.text().strip()
        if not text:
            return

        # 检查重复
        if any(cb.text() == text for cb in self.checkboxes):
            return

        # 创建新复选框
        checkbox = QCheckBox(text, self.grid_layout.parentWidget())
        font = QtGui.QFont()
        font.setPixelSize(18)
        checkbox.setFont(font)
        checkbox.setChecked(False)
        checkbox.stateChanged.connect(self.on_checkbox_state_changed)

        # 计算位置
        index = len(self.checkboxes)
        row = index // 5
        col = index % 5

        # 添加到布局
        self.grid_layout.addWidget(checkbox, row, col)
        self.checkboxes.append(checkbox)
        self.input.clear()

    def on_checkbox_state_changed(self, state):
        checkbox = self.sender()
        if not checkbox:
            return

        if checkbox.text() == 'Default':
            if state == Qt.Checked:
                for cb in self.checkboxes:
                    if cb != checkbox:
                        cb.setChecked(False)
        else:
            if state == Qt.Checked:
                default_cb = next((cb for cb in self.checkboxes if cb.text() == 'Default'), None)
                if default_cb and default_cb.isChecked():
                    default_cb.setChecked(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = channelimportView()
    window.show()
    sys.exit(app.exec_())
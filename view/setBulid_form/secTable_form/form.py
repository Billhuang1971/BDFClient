from PyQt5.QtWidgets import QDialog, QLabel, QGridLayout, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QScrollArea, QApplication, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView


class SectableView(QWidget):
    def __init__(self, description, trainSetInfo, testSetInfo, parent=None):
        super(SectableView, self).__init__(parent)
        self.setStyleSheet("background-color: white; font-size: 14pt;")
        self.setFixedSize(700, 600)  # 设置窗口的固定大小


        self.data_entries = [
            ('类型', description['type']),
            ('采样率', description['sampleRate']),
            ('采样点数量', description['span']),
            ('通道数量', description['nChannel']),
            ('通道', description['channels']),
            ('数据来源', description['source']),
            ('主题ID', description['themeID']),
            ('正反比例', description['ratio']),
            ('训练数据比例', description['trainRatio']),
            ('反例方案', description['scheme']),
            ('延拓方式', description['extension'])
        ]

        self.trainSetInfo = trainSetInfo
        self.testSetInfo = testSetInfo
        self.init_view()

    def init_view(self):
        scroll_area = QScrollArea(self)  # 创建滚动区域
        scroll_area.setWidgetResizable(True)  # 允许内容自适应尺寸
        content_widget = QWidget()  # 创建内容部件
        layout = QVBoxLayout(content_widget)  # 给内容部件设置垂直布局

        grid_layout = QGridLayout()  # 创建网格布局
        for i, (label, value) in enumerate(self.data_entries):
            label_widget = QLabel(label)
            value_widget = QLabel(str(value))
            value_widget.setWordWrap(True)  # 允许值标签换行
            grid_layout.addWidget(label_widget, i, 0)
            grid_layout.addWidget(value_widget, i, 1)

        layout.addLayout(grid_layout)

        # 添加训练数据和测试数据的表格
        self.add_table(self.trainSetInfo, '训练数据', layout)
        self.add_table(self.testSetInfo, '测试数据', layout)

        scroll_area.setWidget(content_widget)  # 将内容部件设置到滚动区域中
        main_layout = QVBoxLayout(self)  # 创建主布局
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def add_table(self, data_info, title, layout):
        title_label = QLabel(title)
        layout.addWidget(QLabel(''))
        layout.addWidget(title_label)

        table = QTableWidget(len(data_info), 2)
        table.setHorizontalHeaderLabels(['标签', '数量'])
        table.setFont(QFont('SansSerif', 10))
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)

        for i, (label, count) in enumerate(data_info.items()):
            table.setItem(i, 0, QTableWidgetItem(str(label)))
            table.setItem(i, 1, QTableWidgetItem(str(count)))

        row_height = table.rowHeight(0)  # Get the height of a single row
        header_height = table.horizontalHeader().height()  # Get the height of the header
        table_height = (row_height * len(data_info)) + header_height  # Calculate total height
        table.setFixedHeight(table_height + 8)

        layout.addWidget(table)  # 将表格添加到布局中

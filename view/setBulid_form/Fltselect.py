from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget,
                             QHeaderView, QAbstractItemView, QSizePolicy,
                             QHBoxLayout, QPushButton, QMessageBox,QAbstractScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
import sys

class ChannelDataViewer(QMainWindow):
    def __init__(self, channel,data_list=None):
        super().__init__()
        self.reference_channels = None  # 用于存储参考通道集合
        self.all_match = True  # 是否全部匹配标志
        self.store_channels=[] #保存通过匹配的所有通道历史集合
        self.data_list=data_list #保存每次传入的需要保存的数据
        self.existing_values = set()#存储已经存在的文件名（避免重复添加

        # 窗口初始化设置
        self.setWindowTitle("通道数据审查器")
        self.setGeometry(100, 100, 1200, 800)

        # 主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 主布局
        self.main_layout = QVBoxLayout(self.central_widget)

        # 创建表格
        self.table = self._create_table()
        self.main_layout.addWidget(self.table)

        # 创建按钮布局
        self.button_layout = QHBoxLayout()

        # 创建按钮
        self.pass_btn = QPushButton("匹配通过")
        self.pass_btn.setFont(QFont("Arial", 16))

        self.close_btn = QPushButton("关闭")
        self.close_btn.setFont(QFont("Arial", 16))
        self.close_btn.clicked.connect(self.close_state)
        self.pass_btn.clicked.connect(self.select_store)

        # 添加按钮到布局
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.pass_btn)
        self.button_layout.addWidget(self.close_btn)
        self.button_layout.addStretch()

        self.main_layout.addLayout(self.button_layout)

        # 初始化数据
        if data_list:
            self.init_data(channel,data_list)
        self.showEvent = self._on_show_event.__get__(self, self.__class__)
    def close_state(self):
        self.table.setRowCount(0)  # 清空原有数据
        self.close()
    def _create_table(self):
        """创建并配置表格控件"""
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["文件名", "通道数量", "通道信息"])
        table.setRowCount(0)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 字体设置
        header_font = QFont("微软雅黑", 16, QFont.Bold)
        content_font = QFont("Consolas", 13)
        table.horizontalHeader().setFont(header_font)
        table.setFont(content_font)


        # 列宽设置
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignCenter)

        # 其他设置
        table.verticalHeader().setVisible(True)
        table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        table.setWordWrap(True)
        table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        return table

    def init_data(self, channel,data_list):
        """初始化表格数据并进行检查"""
        self.table.setRowCount(0)  # 清空原有数据
        self.all_match = True
        self.table.setRowCount(len(data_list))

        # 设置参考通道（default使用第一条数据，or指定通道）
        if data_list:
            try:
                if channel[0] != 'Default':
                    self.reference_channels = set(channel)
                else:
                    self.reference_channels = data_list[0][0]
            except (IndexError, TypeError) as e:
                QMessageBox.critical(self, "错误", "数据格式不正确")
                print(f"数据格式错误: {e}")
                return

        for row, item in enumerate(data_list):
            try:
                current_channels, filename = item[0], item[1]
                # current_channels = set(channels)
            except (IndexError, TypeError) as e:
                print(f"数据格式错误: {e}")
                continue

            # 填充表格数据
            self._fill_row(row, filename, current_channels)

            # 检查通道匹配（从第二行开始检查）
            if row >= 0:
                if self.reference_channels - current_channels != set():  # 不为空集即 当前比参考缺少了的元素
                    self._handle_mismatch(row, filename, current_channels)

        # 更新按钮状态
        self.pass_btn.setEnabled(self.all_match)

        # 调整布局
        self._adjust_table_layout()
    def update_data(self,channel,data_list):
        self.table.setRowCount(0)  # 清空原有数据
        self.all_match = True
        current_data=[]
        current_data.extend(self.store_channels)
        tempt=[]
        for item in data_list:
            if item[1] not in self.existing_values: #查看历史是否有同名文件
                tempt.append(item)
            else:
                QMessageBox.information(self, "提示", "存在重复匹配的文件，已自动过滤")
        self.data_list=tempt #存储本次可能需要保存的通道项
        current_data.extend(tempt)
        self.table.setRowCount(len(current_data))
        # 设置参考通道（使用第一条数据）
        if current_data:
            try:
                if channel[0]!='Default':
                    self.reference_channels=set(channel)
                else:
                    if len(self.store_channels)!=0: #上次成功匹配
                        self.reference_channels = self.store_channels[0][0]
                    else:
                        self.reference_channels=data_list[0][0]
            except IndexError:
                QMessageBox.critical(self, "错误", "数据格式不正确")
                return

        for row, item in enumerate(current_data):
            try:
                current_channels, filename = item[0], item[1]
                # current_channels = set(channels)
            except (IndexError, TypeError) as e:
                print(f"数据格式错误: {e}")
                continue

            # 填充表格数据
            self._fill_row(row, filename, current_channels)

            # 检查通道匹配（从新数据的第一行开始检测）
            if row >= len(self.store_channels):
                if self.reference_channels - current_channels != set():  # 不为空集即 当前比参考缺少了的元素
                    self._handle_mismatch(row, filename, current_channels)

        # 更新按钮状态
        self.pass_btn.setEnabled(self.all_match)

        # 调整布局
        self._adjust_table_layout()

    def select_store(self):
        """通过匹配后保存当前表格项"""
        self.store_channels.extend(self.data_list)
        for item in self.store_channels:
            self.existing_values.add(item[1])
    def _fill_row(self, row, filename, channels):
        """填充表格行数据"""
        # 文件名
        file_item = QTableWidgetItem(filename)
        file_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.table.setItem(row, 0, file_item)

        # 通道数量
        count_item = QTableWidgetItem(str(len(channels)))
        count_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 1, count_item)

        # 通道信息
        channel_str = self._format_channels(channels)
        channel_item = QTableWidgetItem(channel_str)
        channel_item.setTextAlignment(Qt.AlignLeft)
        self.table.setItem(row, 2, channel_item)


    def _format_channels(self, channels):
        """格式化通道字符串"""
        sorted_channels = sorted(channels)
        return "  ".join(sorted_channels)

    def _handle_mismatch(self, row, filename, current_channels):
        """处理不匹配情况"""
        self.all_match = False

        # 高亮显示不匹配行
        for col in range(3):
            item = self.table.item(row, col)
            item.setBackground(QColor(255, 200, 200))  # 浅红色背景

        # 显示警告对话框
        diff = self._get_difference(current_channels)
        msg = f"文件 {filename} 通道不匹配！\n\n差异：{diff}"
        QMessageBox.warning(self, "通道不匹配", msg)

    def _get_difference(self, current_channels):
        """获取通道差异信息"""
        missing = self.reference_channels - current_channels
        # extra = current_channels - self.reference_channels
        diff = []
        if missing:
            diff.append(f"缺少通道：{', '.join(sorted(missing))}")
        # if extra:
        #     diff.append(f"多余通道：{', '.join(sorted(extra))}")
        return "\n".join(diff) if diff else "无差异"

    def _adjust_table_layout(self):
        """调整表格布局"""
        self.table.resizeRowsToContents()
        for row in range(self.table.rowCount()):
            self.table.setRowHeight(row, self.table.sizeHintForRow(row))
        # 强制刷新行高，避免残留空白
        # for row in range(self.table.rowCount()):
        #     self.table.setRowHeight(row, self.table.rowHeight(row))
        self.table.horizontalHeader().setStretchLastSection(True)
        self.main_layout.update()  # 更新主布局

    def resizeEvent(self, event):
        """重写resizeEvent方法，在窗口大小变化时重新调整表格布局"""
        super().resizeEvent(event)
        self._adjust_table_layout()

    def _on_show_event(self, event):
        """窗口显示时的处理函数，手动触发布局更新"""
        self._adjust_table_layout()
        QMainWindow.showEvent(self, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 测试数据
    test_data = [[{'ACC4-REF', 'OFG2-REF', 'F34-REF', 'HP11-REF', 'ACC2-REF', 'OFG3-REF', 'MCC2-REF', 'F112-REF',
                   'F32-REF', 'IL10-REF', 'F19-REF', 'MCC1-REF',
                   'ACC1-REF', 'OFG10-REF', 'MCC10-REF', 'ACC6-REF', 'F12-REF', 'F11-REF', 'OFG9-REF', 'F212-REF',
                   'HP3-REF', 'F18-REF', 'ACC5-REF', 'F23-REF',
                   'F27-REF', 'HB12-REF', 'F24-REF', 'F21-REF', 'F16-REF', 'F39-REF', 'OFG1-REF', 'HP8-REF',
                   'ACC11-REF', 'IL6-REF', 'ACC8-REF', 'OFG8-REF',
                   'F31-REF', 'HB8-REF', 'F29-REF', 'MCC12-REF', 'F33-REF', 'MCC5-REF', 'F14-REF', 'OFG11-REF',
                   'F36-REF', 'MCC6-REF', 'OFG6-REF', 'F110-REF',
                   'HB3-REF', 'HB2-REF', 'HP4-REF', 'ACC3-REF', 'IL2-REF', 'ACC9-REF', 'F26-REF', 'F25-REF', 'F13-REF',
                   'OFG4-REF', 'HB4-REF', 'HP10-REF',
                   'IL9-REF', 'IL4-REF', 'HP6-REF', 'F312-REF', 'IL1-REF', 'F28-REF', 'F17-REF', 'MCC11-REF', 'HB9-REF',
                   'MCC7-REF', 'OFG5-REF', 'ACC10-REF',
                   'OFG12-REF', 'HP2-REF', 'F15-REF', 'HP1-REF', 'MCC4-REF', 'IL8-REF', 'IL5-REF', 'F311-REF',
                   'MCC3-REF', 'F211-REF', 'F37-REF', 'HB5-REF',
                   'F210-REF', 'HB11-REF', 'HP5-REF', 'HP9-REF', 'ACC12-REF', 'HB6-REF', 'HB10-REF', 'ACC7-REF',
                   'OFG7-REF', 'HB1-REF', 'F38-REF', 'IL7-REF',
                   'HP7-REF', 'IL3-REF', 'MCC9-REF', 'F35-REF', 'F310-REF', 'MCC8-REF', 'HP12-REF', 'HB7-REF',
                   'F111-REF', 'F22-REF'}, 'bdftest01-1']]
    window = ChannelDataViewer(test_data)
    window.show()
    # test_data1=[{'R1_3-REF', "IL'7-REF", "OFC'11-REF", 'R2_10-REF', 'R5_3-REF', 'R3_3-REF', 'R1_5-REF', 'R6_2-REF',
    #                "OFC'15-REF", 'L1_4-REF', 'R3_5-REF',
    #                "OFC'16-REF", "OFC'13-REF", 'L1_9-REF', "OFC'7-REF", 'R5_5-REF', "OFC'2-REF", 'R1_4-REF', 'R1_1-REF',
    #                'R3_2-REF', 'L1_5-REF', 'L2_6-REF',
    #                'R6_3-REF', 'L1_1-REF', 'R6_5-REF', 'R1_9-REF', 'R5_11-REF', 'R6_1-REF', 'R3_8-REF', 'R3_14-REF',
    #                'R5_6-REF', 'L1_12-REF', 'R3_10-REF',
    #                'R2_7-REF', 'L2_10-REF', 'R6_12-REF', 'R1_8-REF', 'L1_8-REF', 'L1_7-REF', 'R5_4-REF', "OFC'9-REF",
    #                "OFC'1-REF", 'R4_5-REF', 'R4_4-REF',
    #                'R3_12-REF', 'R4_1-REF', "OFC'4-REF", 'R5_12-REF', "OFC'6-REF", "OFC'10-REF", 'L1_10-REF',
    #                'L1_3-REF', 'R3_6-REF', "OFC'5-REF", 'R5_2-REF',
    #                'R2_4-REF', 'R5_7-REF', 'R1_2-REF', "IL'8-REF", 'R1_7-REF', "IL'1-REF", 'R2_1-REF', 'R2_8-REF',
    #                'R3_4-REF', 'L1_15-REF', 'L2_8-REF',
    #                'R3_13-REF', 'R3_15-REF', 'R4_3-REF', 'R6_11-REF', 'R2_9-REF', 'L2_1-REF', 'L1_11-REF', 'R2_2-REF',
    #                'R4_6-REF', 'R4_10-REF', "OFC'12-REF",
    #                'L2_4-REF', 'L1_13-REF', 'R4_8-REF', "OFC'18-REF", 'R6_10-REF', "IL'2-REF", "OFC'17-REF", "IL'5-REF",
    #                'R1_10-REF', 'L1_6-REF', "OFC'3-REF",
    #                'R6_4-REF', 'R6_9-REF', 'R5_8-REF', 'L2_2-REF', 'R5_10-REF', 'R6_7-REF', "OFC'8-REF", 'R1_6-REF',
    #                'R5_9-REF', 'L1_14-REF', 'L2_5-REF',
    #                'L2_9-REF', 'R4_11-REF', 'R2_5-REF', 'R5_1-REF', 'R2_6-REF', 'R6_8-REF', 'R4_7-REF', 'R4_12-REF',
    #                'R3_9-REF', "IL'6-REF", 'L1_2-REF',
    #                'R2_3-REF', "IL'4-REF", 'R3_1-REF', 'R3_11-REF', 'R3_7-REF', "OFC'14-REF", 'L2_3-REF', "IL'3-REF",
    #                'L2_7-REF', 'R6_6-REF', 'R4_2-REF',
    #                'R4_9-REF'}, 'bdftest010-1']
    # window.update_data(test_data1)

    sys.exit(app.exec_())
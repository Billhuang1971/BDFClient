import sys
from copy import deepcopy
from functools import partial

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QBrush

from view.trainmodel_form.train import Ui_Trainning
from view.trainmodel_form.parameter_1 import Ui_Parameter
from PyQt5.QtWidgets import *

class modelTrainView(QWidget):
    page_control_signal = pyqtSignal(list)
    page_control_signal_1 = pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Trainning()
        self.ui.setupUi(self)
        self.train_algorithm_header = ['算法名称', '算法类型', '查看参数设置']
        self.train_algorithm_field = ['alg_id', 'alg_type', '']
        self.header = ['数据集合名称']
        self.field = ['set_name']
        self.ui.pushButton_2.clicked.connect(self.__home_page)
        self.ui.pushButton_3.clicked.connect(self.__pre_page)
        self.ui.pushButton_4.clicked.connect(self.__next_page)
        self.ui.pushButton_5.clicked.connect(self.__final_page)
        self.ui.pushButton_13.clicked.connect(self.__confirm_skip)
        self.ui.pushButton_6.clicked.connect(self.__home_page_1)
        self.ui.pushButton_7.clicked.connect(self.__pre_page_1)
        self.ui.pushButton_8.clicked.connect(self.__next_page_1)
        self.ui.pushButton_9.clicked.connect(self.__final_page_1)
        self.ui.pushButton_14.clicked.connect(self.__confirm_skip_1)

    # 初始化算法管理主页面
    def initAlgorithmTable(self, algorithm_info, show_parameter_setting):
        try:
            data = algorithm_info
            col_num = len(self.train_algorithm_header)
            row_num = len(data)
            self.ui.algorithm_tableWidget.setColumnCount(col_num)
            self.ui.algorithm_tableWidget.setRowCount(row_num)
            # 设置表格高度
            for i in range(row_num):
                self.ui.algorithm_tableWidget.setRowHeight(i, 55)
            for i in range(col_num - 1):
                self.ui.algorithm_tableWidget.setColumnWidth(i, 200)
            self.ui.algorithm_tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.ui.algorithm_tableWidget.setHorizontalHeaderLabels(self.train_algorithm_header)
            # 设置表头格式
            self.ui.algorithm_tableWidget.horizontalHeader().setStyleSheet(
                '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
            # 使表格填满整个widget
            self.ui.algorithm_tableWidget.horizontalHeader().setStretchLastSection(True)

            for r in range(row_num):
                for c in range(col_num - 1):
                    if c == 0:
                        self.item = QTableWidgetItem(str(data[r][1]))
                        self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        font = self.item.font()
                        font.setPointSize(10)
                        self.item.setFont(font)
                        self.ui.algorithm_tableWidget.setItem(r, c, self.item)
                    if c == 1:
                        cur_algorithm_type = data[r][17]
                        if cur_algorithm_type == 'waveform':
                            self.item = QTableWidgetItem('波形标注算法')
                            self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = self.item.font()
                            font.setPointSize(10)
                            self.item.setFont(font)
                            self.ui.algorithm_tableWidget.setItem(r, c, self.item)
                        else:
                            self.item = QTableWidgetItem('状态标注算法')
                            self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = self.item.font()
                            font.setPointSize(10)
                            self.item.setFont(font)
                            self.ui.algorithm_tableWidget.setItem(r, c, self.item)
                layout = QHBoxLayout()
                self.ui.algorithm_tableWidget.setCellWidget(r, col_num - 1, QWidget())
                showSettingBtn = QPushButton('查看参数设置')
                showSettingBtn.clicked.connect(partial(show_parameter_setting, r))
                showSettingBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                showSettingBtn.setCursor(Qt.PointingHandCursor)
                layout.addWidget(showSettingBtn)
                layout.setStretch(0, 1)
                self.ui.algorithm_tableWidget.cellWidget(r, col_num - 1).setLayout(layout)
            # 按字段长度进行填充
            # self.ui.algorithm_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            # 只能选中一行
            self.ui.algorithm_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.ui.algorithm_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        except Exception as e:
            print('initAlgorithmTable', e)


    def initSetTable(self, set_info):
        try:
            data = deepcopy(set_info)
            col_num = len(self.header)
            row_num = 0
            # 删除不必要的信息，只留下算法名称和训练参数
            if data:
                data = np.delete(data, [0, 2, 3, 4], axis=1)
                row_num = len(data)
            self.ui.trainset_tableWidget.setColumnCount(col_num)
            self.ui.trainset_tableWidget.setRowCount(row_num)
            for i in range(row_num):
                self.ui.trainset_tableWidget.setRowHeight(i, 40)
            for i in range(col_num):
                header_item = QTableWidgetItem(self.header[i])
                font = header_item.font()
                font.setPointSize(16)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                header_item.setData(Qt.UserRole, self.field[i])
                self.ui.trainset_tableWidget.setHorizontalHeaderItem(i, header_item)
                # 拉伸表格列项，使其铺满
                self.ui.trainset_tableWidget.horizontalHeader().setStretchLastSection(True)

                for r in range(row_num):
                    for c in range(col_num):
                        self.item = QTableWidgetItem(str(data[r][c]))
                        self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        font = self.item.font()
                        font.setPointSize(10)
                        self.item.setFont(font)
                        self.ui.trainset_tableWidget.setItem(r, c, self.item)
                # self.init_comboCond()
                self.ui.trainset_tableWidget.horizontalHeader().setHighlightSections(False)
                #   按字段长度进行填充
                self.ui.trainset_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                # 增加和查询的时候列数会改变，所以需要保存原来列数
                # self.col = self.view.ui.trainset_tableWidget.columnCount()
                # 设置算法列表不可编辑
                self.ui.trainset_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
                # 点击就选中整行
                self.ui.trainset_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        except Exception as e:
            print('initSetTable', e)

    def __home_page(self):
        """点击首页信号"""
        self.page_control_signal.emit(["home", self.ui.label_3.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.page_control_signal.emit(["pre", self.ui.label_3.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.page_control_signal.emit(["next", self.ui.label_3.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.page_control_signal.emit(["final", self.ui.label_3.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.page_control_signal.emit(["confirm", self.ui.lineEdit_4.text()])

    def __home_page_1(self):
        """点击首页信号"""
        self.page_control_signal_1.emit(["home", self.ui.label_4.text()])

    def __pre_page_1(self):
        """点击上一页信号"""
        self.page_control_signal_1.emit(["pre", self.ui.label_4.text()])

    def __next_page_1(self):
        """点击下一页信号"""
        self.page_control_signal_1.emit(["next", self.ui.label_4.text()])

    def __final_page_1(self):
        """尾页点击信号"""
        self.page_control_signal_1.emit(["final", self.ui.label_4.text()])

    def __confirm_skip_1(self):
        """跳转页码确定"""
        self.page_control_signal_1.emit(["confirm", self.ui.lineEdit_5.text()])


    def reject(self):
        pass

class Parameter_view(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Parameter()
        self.ui.setupUi(self)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = modelTrainView()
    view.show()
    sys.exit(app.exec_())

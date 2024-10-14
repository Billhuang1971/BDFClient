import datetime
import sys
from view.sampleState import QComboCheckBox
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *


class sectableView(QDialog):
    def __init__(self, parent=None, data_source=None, type_name=None, patient_name=None, measure_date=None,
                 file_name=None, montage=None,
                 type_user=None, type_model=None, mtype_name=None):
        super(sectableView, self).__init__(parent)
        self.data_source = data_source
        self.type_name = type_name
        self.patient_name = patient_name
        self.measure_date = measure_date
        self.file_name = file_name
        self.montage = montage
        self.type_user = type_user
        self.type_model = type_model
        self.mtype_name = mtype_name
        self.evaluate_result = ['符合', '不符合']
        # 默认可选的过滤器，根据数据来源会进行变化
        self.defaultFilter = ['病人姓名', '测量日期', '文件名', '导联', '标注用户']
        # 选中的过滤器
        self.filters_text = []
        self.init_view()

    def init_view(self):
        self.setWindowTitle("明细")
        self.resize(1280, 720)

        self.tableWideget = QTableWidget()

        self.label_3 = QLabel('数据来源:{}'.format(self.data_source))
        self.label_2 = QLabel('标注类型: {}'.format(self.type_name))
        self.label_1 = QLabel('筛选条件:')

        font = QFont()
        font.setPointSize(12)
        self.label_1.setFont(font)
        self.label_2.setFont(font)
        self.label_3.setFont(font)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()

        if self.type_model is not None:
            self.defaultFilter.append('标注模型')
        if self.mtype_name is not None:
            self.defaultFilter.append('模型标注类型')
            self.defaultFilter.append('评估结果')

        self.comboBox_1 = QComboCheckBox(self.defaultFilter, default_check=False)

        self.spaceItem_1 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spaceItem_2 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spaceItem_3 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spaceItem_4 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayout.addWidget(self.label_3)
        self.horizontalLayout.addItem(self.spaceItem_4)

        self.horizontalLayout.addWidget(self.label_2)
        self.horizontalLayout.addItem(self.spaceItem_3)

        self.horizontalLayout.addWidget(self.label_1)
        self.horizontalLayout.addWidget(self.comboBox_1)
        self.horizontalLayout.addItem(self.spaceItem_1)

        self.horizontalLayout.setStretch(6, 7)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.verticalLayout.addWidget(self.tableWideget)
        self.verticalLayout.setStretch(2, 9)

    def init_table(self, table, tag=False):
        # print(self.filters_text)
        row_num = len(table)
        col_num = len(self.filters_text) + 1
        # 设置列头
        temp = self.filters_text[:]
        if tag:
            col_num = col_num - 1
            temp.pop()
        temp.append('数量')
        col_label = temp

        # print(col_num)
        self.tableWideget.setRowCount(row_num)
        self.tableWideget.setColumnCount(col_num)
        # 设置表格高度
        for i in range(row_num):
            self.tableWideget.setRowHeight(i, 55)

        # if self.data_source == '评估标注':
        #     temp.append('评估结果')
        # print(col_label)
        self.tableWideget.setHorizontalHeaderLabels(col_label)

        # 各列均分
        self.tableWideget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWideget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.tableWideget.horizontalHeader().setStyleSheet(
            '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
        # 使表格填满整个widget
        self.tableWideget.horizontalHeader().setStretchLastSection(True)
        self.tableWideget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # print(user_info)
        for row in range(0, row_num):
            for col in range(0, col_num):
                if isinstance(table[row][col], int):
                    self.text_item = QTableWidgetItem(str(table[row][col]))
                elif isinstance(table[row][col], datetime.date):
                    self.text_item = QTableWidgetItem(table[row][col].strftime("%Y-%m-%d"))
                else:
                    self.text_item = QTableWidgetItem(table[row][col])
                self.text_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.text_item.setFont(QFont('', 12))
                self.tableWideget.setItem(row, col, self.text_item)

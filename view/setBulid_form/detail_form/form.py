import sys
# from util.ComboCheckBox import QComboCheckBox
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import numpy as np


class detailView(QDialog):
    def __init__(self, parent=None, typeNum_str=None, set_name=None, data_source=None, Ref=None,
                 train_ration=None, test_ration=None, ruler=None, Reverse=None, sample_length=None, down_value=None
                 , select_channel=None, setDetail=None):
        super(detailView, self).__init__(parent)
        self.typeNum_str = typeNum_str
        self.set_name = set_name
        self.data_source = data_source
        self.Ref = Ref
        self.train_ration = train_ration
        self.test_ration = test_ration
        self.ruler = ruler
        self.Reverse = Reverse
        self.setDetail = setDetail
        self.sample_length = sample_length
        self.down_value = down_value
        self.select_channel = select_channel
        self.total_num = 0
        self.positiveNum = 0
        self.reverse_num = 0
        self.init_view()
        self.init_scroArea()

    def init_view(self):
        self.setWindowTitle("详细信息")
        self.resize(1280, 720)
        font = QFont()
        font.setPointSize(12)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)

        self.scroLayout = QVBoxLayout()
        inner_widget = QWidget()
        inner_widget.setLayout(self.scroLayout)
        scrollArea.setWidget(inner_widget)

        label_0 = QLabel('数据集名称: {}'.format(self.set_name))
        label_1 = QLabel('数据来源: {}'.format(' '.join(data_source for data_source in self.data_source)))

        self.label_6 = QLabel("(正例数量: {}   反例数量: {})".format(self.positiveNum, self.reverse_num))
        label_2 = QLabel('训练集比率: {}%'.format(self.train_ration))
        label_3 = QLabel('测试集比率: {}%'.format(self.test_ration))
        label_4 = QLabel('延拓规则: {}'.format(self.ruler))
        self.label_5 = QLabel('样本数量: {}'.format(self.total_num))

        label_7 = QLabel('参考方案：{}  '.format(self.Ref))
        if self.select_channel is not None:
            channel_s = ''
            channel_s += ' '.join((channel for channel in self.select_channel[0:3]))
            if len(self.select_channel) > 3:
                label_9 = QLabel('导联挑选：{}...(移动至此有提示)'.format(channel_s))
                label_9.setToolTip("已添加：\n\t" + "\n\t".join((item for item in self.select_channel)))
            else:
                label_9 = QLabel('导联挑选：{}'.format(channel_s))
            label_9.setFont(font)
        items = self.Reverse.split(' ')
        item = items[0]
        result = item.split('-')
        ratio = result[1]
        label_8 = QLabel(' 正反比例：{}'.format(ratio))
        label_10 = QLabel('样本长度：{}秒(s)'.format(self.sample_length))
        label_11 = QLabel('下沿阈值：{}秒(s)'.format(self.down_value))

        label_0.setFont(font)
        label_1.setFont(font)
        label_2.setFont(font)
        label_3.setFont(font)
        label_4.setFont(font)
        self.label_5.setFont(font)
        label_7.setFont(font)
        label_8.setFont(font)
        label_10.setFont(font)
        label_11.setFont(font)

        font1 = QFont()
        font1.setPointSize(9)
        self.label_6.setFont(font1)

        widget_1 = QWidget()
        verticalLayout_1 = QVBoxLayout()
        widget_1.setLayout(verticalLayout_1)

        verticalLayout = QtWidgets.QVBoxLayout(self)
        verticalLayout.setObjectName("verticalLayout")
        horizontalLayout_0 = QtWidgets.QHBoxLayout()
        horizontalLayout_1 = QtWidgets.QHBoxLayout()
        horizontalLayout_2 = QtWidgets.QHBoxLayout()
        horizontalLayout_3 = QtWidgets.QHBoxLayout()
        horizontalLayout_4 = QtWidgets.QHBoxLayout()
        horizontalLayout_5 = QtWidgets.QHBoxLayout()
        horizontalLayout_6 = QtWidgets.QHBoxLayout()

        spaceItem_0 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spaceItem_1 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spaceItem_2 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spaceItem_3 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spaceItem_4 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spaceItem_5 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spaceItem_6 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spaceItem_7 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spaceItem_8 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        line3 = QFrame()
        line3.setFrameShape(QFrame.HLine)
        line3.setFrameShadow(QFrame.Sunken)
        line4 = QFrame()
        line4.setFrameShape(QFrame.HLine)
        line4.setFrameShadow(QFrame.Sunken)
        line5 = QFrame()
        line5.setFrameShape(QFrame.HLine)
        line5.setFrameShadow(QFrame.Sunken)
        line6 = QFrame()
        line6.setFrameShape(QFrame.HLine)
        line6.setFrameShadow(QFrame.Sunken)
        line7 = QFrame()
        line7.setFrameShape(QFrame.HLine)
        line7.setFrameShadow(QFrame.Sunken)

        horizontalLayout_0.addWidget(label_0)
        horizontalLayout_0.addItem(spaceItem_0)
        horizontalLayout_0.addWidget(self.label_5)
        horizontalLayout_0.addWidget(self.label_6)
        horizontalLayout_0.addItem(spaceItem_5)
        horizontalLayout_0.setStretch(4, 9)

        horizontalLayout_1.addWidget(label_1)
        horizontalLayout_1.addItem(spaceItem_1)
        horizontalLayout_1.setStretch(1, 9)

        horizontalLayout_2.addWidget(label_2)
        horizontalLayout_2.addItem(spaceItem_2)
        horizontalLayout_2.addWidget(label_3)
        horizontalLayout_2.addItem(spaceItem_3)
        horizontalLayout_2.setStretch(3, 9)

        horizontalLayout_3.addWidget(label_4)
        horizontalLayout_3.addItem(spaceItem_4)
        horizontalLayout_3.setStretch(1, 9)

        horizontalLayout_4.addWidget(label_7)
        if self.select_channel is not None:
            horizontalLayout_4.addWidget(label_9)
        horizontalLayout_4.addItem(spaceItem_7)
        if self.select_channel is not None:
            horizontalLayout_4.setStretch(1, 9)
        else:
            horizontalLayout_4.setStretch(2, 9)

        horizontalLayout_6.addWidget(label_10)
        horizontalLayout_6.addWidget(label_11)
        horizontalLayout_6.addWidget(label_8)
        horizontalLayout_6.addItem(spaceItem_8)
        horizontalLayout_6.setStretch(3, 9)

        verticalLayout.addLayout(horizontalLayout_0)
        verticalLayout.addWidget(line1)
        verticalLayout.addLayout(horizontalLayout_1)
        verticalLayout.addWidget(line4)
        verticalLayout.addLayout(horizontalLayout_4)
        verticalLayout.addWidget(line7)
        verticalLayout.addLayout(horizontalLayout_6)
        verticalLayout.addWidget(line2)
        verticalLayout.addLayout(horizontalLayout_2)
        verticalLayout.addWidget(line3)
        verticalLayout.addLayout(horizontalLayout_3)

        verticalLayout.addWidget(scrollArea)
        verticalLayout.setStretch(13, 9)

        self.spaceItemWidth1 = 33
        self.spaceItemWidth2 = 65
        self.spaceItemWidth3 = 105
        self.spaceItemWidth4 = 138
        self.font = QFont()
        self.font.setPointSize(12)

    def init_scroArea(self):
        # i = 0
        typeLengthNum = self.typeNum_str.split(' ')
        typeLengthNum_dict = dict()
        for item in typeLengthNum:
            result = item.split('-')
            typeLengthNum_dict[result[0] + '-' + result[1]] = result[2]

        labelType = set()
        for item in self.setDetail:
            labelType.add(item[0])
        labelGroup = []
        for item in labelType:
            temp = []
            for i in self.setDetail:
                if i[0] == item:
                    temp.append(i)
            labelGroup.append(temp)
        # print(labelGroup)
        n = 0
        for i in labelGroup:
            verticalLayout = QtWidgets.QVBoxLayout()
            self.scroLayout.addLayout(verticalLayout)

            type_name = i[0][0]
            type_length = i[0][1]
            type_model = i[0][2]
            evaluate = i[0][3]
            type_user = i[0][4]
            patient = i[0][5]
            typeNum = 0
            for key, value in typeLengthNum_dict.items():
                result = key.split('-')
                typeName = result[0]
                if typeName == type_name:
                    typeNum += int(value)

            self.positiveNum += typeNum
            label_0 = QLabel('标注名称: {}'.format(type_name))
            num_label = QLabel('标注数量：{}'.format(typeNum))

            if type_model != ' ':
                label_2 = QLabel('标注模型: {}'.format(type_model))
                label_2.setFont(self.font)
            if evaluate != ' ':
                label_3 = QLabel('评估结果: {}'.format(evaluate))
                label_3.setFont(self.font)

            label_4 = QLabel('标注用户: {}'.format(type_user))
            if patient == '全选':
                label_5 = QLabel('病   人 : 全选')
                label_5.setFont(self.font)

            label_0.setFont(self.font)
            num_label.setFont(self.font)

            label_4.setFont(self.font)

            horizontalLayout_0 = QtWidgets.QHBoxLayout()
            horizontalLayout_1 = QtWidgets.QHBoxLayout()
            horizontalLayout_2 = QtWidgets.QHBoxLayout()
            horizontalLayout_3 = QtWidgets.QHBoxLayout()
            horizontalLayout_4 = QtWidgets.QHBoxLayout()
            horizontalLayout_5 = QtWidgets.QHBoxLayout()

            spaceItem1 = QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            spaceItem1_0 = QSpacerItem(120, 5, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)

            spaceItem2 = QSpacerItem(self.spaceItemWidth1, 5, QSizePolicy.Fixed, QSizePolicy.Fixed)
            spaceItem3 = QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            spaceItem4 = QSpacerItem(self.spaceItemWidth1, 5, QSizePolicy.Fixed, QSizePolicy.Fixed)
            spaceItem5 = QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            spaceItem6 = QSpacerItem(self.spaceItemWidth1, 5, QSizePolicy.Fixed, QSizePolicy.Fixed)
            spaceItem7 = QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            spaceItem8 = QSpacerItem(self.spaceItemWidth1, 5, QSizePolicy.Fixed, QSizePolicy.Fixed)
            spaceItem9 = QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            # spaceItem = QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

            if patient == '全选':
                spaceItem10 = QSpacerItem(self.spaceItemWidth1, 5, QSizePolicy.Fixed, QSizePolicy.Fixed)

            spaceItem11 = QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

            horizontalLayout_0.addWidget(label_0)
            horizontalLayout_0.addItem(spaceItem1_0)
            horizontalLayout_0.addWidget(num_label)
            horizontalLayout_0.addItem(spaceItem1)

            horizontalLayout_0.setStretch(3, 9)
            type_length = type_length.split(' ')

            for length in type_length:
                spaceItem = QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                line = QFrame()
                line.setFrameShape(QFrame.VLine)
                line.setFrameShadow(QFrame.Sunken)
                typeLength = float(length) * 1000
                label_1 = QLabel('标注长度: {} (单位:秒)'.format(length))
                typeLengthNum = 0
                for key, value in typeLengthNum_dict.items():
                    result = key.split('-')
                    if result[0] == type_name and typeLength == float(result[1]):
                        typeLengthNum = int(value)

                typeLengthNumLabel = QLabel('数量: {}'.format(typeLengthNum))
                label_1.setFont(self.font)
                typeLengthNumLabel.setFont(self.font)
                horizontalLayout_1.addWidget(label_1)
                horizontalLayout_1.addItem(spaceItem)
                horizontalLayout_1.addWidget(typeLengthNumLabel)
                horizontalLayout_1.addWidget(line)

            horizontalLayout_1.addItem(spaceItem3)
            horizontalLayout_1.setStretch(horizontalLayout_1.count() - 1, 9)

            if type_model != ' ':
                horizontalLayout_2.addItem(spaceItem4)
                horizontalLayout_2.addWidget(label_2)
                horizontalLayout_2.addItem(spaceItem5)
                horizontalLayout_2.setStretch(2, 9)

            if evaluate != ' ':
                horizontalLayout_3.addItem(spaceItem6)
                horizontalLayout_3.addWidget(label_3)
                horizontalLayout_3.addItem(spaceItem7)
                horizontalLayout_3.setStretch(2, 9)

            horizontalLayout_4.addItem(spaceItem8)
            horizontalLayout_4.addWidget(label_4)
            horizontalLayout_4.addItem(spaceItem9)
            horizontalLayout_4.setStretch(2, 9)

            if patient == '全选':
                horizontalLayout_5.addItem(spaceItem10)
                horizontalLayout_5.addWidget(label_5)
                horizontalLayout_5.addItem(spaceItem11)
                horizontalLayout_5.setStretch(2, 9)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)

            verticalLayout.addLayout(horizontalLayout_0)
            verticalLayout.addLayout(horizontalLayout_1)
            verticalLayout.addLayout(horizontalLayout_2)
            verticalLayout.addLayout(horizontalLayout_3)
            verticalLayout.addLayout(horizontalLayout_4)
            if patient == '全选':
                verticalLayout.addLayout(horizontalLayout_5)

            if patient != '全选':
                temp_set = set()
                for j in i:
                    temp_set.add(j[5])
                pn_list = []
                for item in temp_set:
                    temp_list = []
                    for j in i:
                        if j[5] == item:
                            temp_list.append(j)
                    pn_list.append(temp_list)
                # print(pn_list)
                for item in pn_list:
                    label_5 = QLabel('病   人： {}'.format(item[0][5]))
                    label_5.setFont(self.font)
                    spaceItem10 = QSpacerItem(self.spaceItemWidth2, 5, QSizePolicy.Fixed, QSizePolicy.Fixed)
                    spaceItem11 = QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                    horizontalLayout_5 = QHBoxLayout()
                    horizontalLayout_5.addItem(spaceItem10)
                    horizontalLayout_5.addWidget(label_5)
                    horizontalLayout_5.addItem(spaceItem11)
                    horizontalLayout_5.setStretch(2, 9)
                    verticalLayout.addLayout(horizontalLayout_5)

                    for n in item:
                        label_6 = QLabel('测量日期： {}'.format(n[6]))
                        label_6.setFont(self.font)
                        spaceItem12 = QSpacerItem(self.spaceItemWidth3, 5, QSizePolicy.Fixed, QSizePolicy.Fixed)
                        spaceItem13 = QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                        horizontalLayout_6 = QHBoxLayout()
                        horizontalLayout_6.addItem(spaceItem12)
                        horizontalLayout_6.addWidget(label_6)
                        horizontalLayout_6.addItem(spaceItem13)
                        horizontalLayout_6.setStretch(2, 9)
                        verticalLayout.addLayout(horizontalLayout_6)

                        if n[6] != '全选':
                            label_7 = QLabel('文件名称： {}'.format(n[7]))
                            label_7.setFont(self.font)
                            spaceItem13 = QSpacerItem(self.spaceItemWidth4, 5, QSizePolicy.Fixed, QSizePolicy.Fixed)
                            spaceItem14 = QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding,
                                                      QtWidgets.QSizePolicy.Minimum)
                            horizontalLayout_7 = QHBoxLayout()
                            horizontalLayout_7.addItem(spaceItem13)
                            horizontalLayout_7.addWidget(label_7)
                            horizontalLayout_7.addItem(spaceItem14)
                            horizontalLayout_7.setStretch(2, 9)
                            verticalLayout.addLayout(horizontalLayout_7)

            verticalLayout.addWidget(line)

        if self.Reverse != ' ':
            Reverse = self.Reverse.split(' ')
        if self.Reverse != ' ':
            for item in Reverse:
                temp = item.split('-')
                reverseLength = temp[0]
                ratio = temp[1]
                positive_ratio = int(ratio.split('/')[0])
                counter_ratio = int(ratio.split('/')[1])
                for key, value in typeLengthNum_dict.items():
                    result = key.split('-')
                    typeLengthNum = int(value)
                    if float(reverseLength) * 1000 == float(result[1]):
                        self.reverse_num += int(typeLengthNum * (counter_ratio / positive_ratio))
        self.total_num = self.positiveNum + self.reverse_num
        self.label_5.setText('样本数量: {}'.format(self.total_num))
        self.label_6.setText("(正例数量: {}   反例数量: {})".format(self.positiveNum, self.reverse_num))
        spacerItem = QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.scroLayout.addItem(spacerItem)
        count = self.scroLayout.count()
        self.scroLayout.setStretch(count - 1, 1)

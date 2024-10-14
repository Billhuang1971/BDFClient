#!/usr/bin/python
# author bluenor
from PyQt5.QtCore import Qt, QRegExp

from util.clientAppUtil import clientAppUtil
from view.basicConfig import BasicConfigView
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from functools import partial
import sys
import numpy as np


class basicConfigController(QWidget):
    update_done_signal = QtCore.pyqtSignal(list)

    def __init__(self, client, cAppUtil):
        super().__init__()
        self.client = client
        self.cAppUtil = cAppUtil
        self.view = BasicConfigView()

        self.client.getConfigDataResSig.connect(self.getConfigRes)
        self.client.addBasicConfigResSig.connect(self.addBasicConfigRes)
        self.client.updBasicConfigResSig.connect(self.updateBasicConfigRes)
        self.client.delBasicConfigResSig.connect(self.delBasicConfigRes)
        self.client.getConfigData()

        self.view.ui.pushButton.clicked.connect(self.on_clicked_basic_config_add)

        self.tableWidget = self.view.ui.tableWidget
        # 存放当前用户信息的列表
        self.configInfo = []
        # 数据库用户表的列名
        self.col_name = ['config_name', 'sampling_rate', 'notch', 'low_pass', 'high_pass', 'default']
        self.col_num = len(self.col_name)

    # 处理“向服务端发送获取配置数据的请求”的结果
    def getConfigRes(self, configInfo):
        print(f'configInfo: {configInfo}')
        self.configInfo = configInfo
        # 表格初始化
        self.view.refresh(self.configInfo, self.updateBasicConfig, self.editCancel, self.delBasicConfig)

    # 回调，self.view.basicConfigAddSig信号处理新增基本配置的逻辑
    def addBasicConfig(self):
        try:
            config = []
            row_num = len(self.configInfo)
            print(f'addBasicConfig row_num: {row_num}')
            for j in range(1, 6):
                config.append(self.tableWidget.item(row_num, j).text())

            if config[0] == '':
                QMessageBox.information(self, "提示", '方案名称不完善', QMessageBox.Yes)
                return
            elif config[1] == '':
                QMessageBox.information(self, "提示", '系统采样率不完善', QMessageBox.Yes)
                return
            elif config[2] == '':
                QMessageBox.information(self, "提示", '陷波滤波不完善', QMessageBox.Yes)
                return
            elif config[3] == '':
                QMessageBox.information(self, "提示", '低通滤波不完善', QMessageBox.Yes)
                return
            elif config[4] == '':
                QMessageBox.information(self, "提示", '高通滤波不完善', QMessageBox.Yes)
                return

            for config_t in self.configInfo:
                if config[0] == config_t[1]:
                    QMessageBox.information(self, "提示", '方案名已存在', QMessageBox.Yes)
                    return

            regex = QRegExp("^[0-9]+$")
            for i in range(1, 5):
                if not regex.exactMatch(config[i]):
                    QMessageBox.information(self, "提示", '采样率或滤波需要为大于零的整数', QMessageBox.Yes)
                    return

            if int(config[3]) <= int(config[4]):
                QMessageBox.information(self, "提示", '高通滤波不能高于低通滤波', QMessageBox.Yes)
                return

            checkbox = self.tableWidget.cellWidget(row_num, 6)
            if checkbox.isChecked():
                config.append(1)
            else:
                config.append(0)
            print(f"config: {config}")
            REQmsg = config
            self.client.addBasicConfig(REQmsg)
        except Exception as e:
            print('addBasicConfig', e)

    # 负责“处理新增基本配置的逻辑”结果
    def addBasicConfigRes(self, config):
        print(f'addBasicConfigRes: {config}')
        for id, c in enumerate(self.configInfo):
            if config[6] == 1 and c[6] == 1:
                c_t = list(c)
                self.configInfo.remove(c)
                c_t[6] = 0
                self.configInfo.insert(id, tuple(c_t))
        self.configInfo.append(config)
        self.view.refresh(self.configInfo, self.updateBasicConfig, self.editCancel, self.delBasicConfig)

    # basicConfigUpdSig信号处理修改基本配置的逻辑
    def updateBasicConfig(self, row):
        try:
            config = []
            config.append(self.configInfo[row][0])
            for j in range(1, 6):
                config.append(self.tableWidget.item(row, j).text())


            print(f'config: {config}')
            regex = QRegExp("^[0-9]+$")
            for i in range(2, 6):
                if not regex.exactMatch(config[i]):
                    QMessageBox.information(self, "提示", '采样率或滤波需要为大于零的整数', QMessageBox.Yes)
                    return

            if int(config[4]) <= int(config[5]):
                QMessageBox.information(self, "提示", '高通滤波不能高于低通滤波', QMessageBox.Yes)
                return

            checkbox = self.tableWidget.cellWidget(row, 6)
            if checkbox.isChecked():
                config.append(1)
            else:
                config.append(0)
            self.client.updateBasicConfig(config)
        except Exception as e:
            print('updateBasicConfig', e)

    # 处理client传回来结果的后续
    def updateBasicConfigRes(self, data):
        print(f'config: {data}')
        if data[0] != '1':
            QMessageBox.information(self, "提示", str(data[1]), QMessageBox.Yes)
            self.view.refresh(self.configInfo, self.updateBasicConfig, self.editCancel, self.delBasicConfig)
            return
        try:
            self.getConfigRes(data[1])
        except Exception as e:
            print('updateBasicConfig', e)
        # 基本配置删除
        # 处理删除基本配置信息方法

    def delBasicConfig(self, i):
        try:
            if len(self.configInfo) == 1:
                QMessageBox.information(self, "提示", "至少保留一个基本配置信息", QMessageBox.Yes)
                return
            reply = QMessageBox.question(self, "基本配置删除", "是否删除此项基本配置", QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                REQmsg = [self.configInfo[i]]
                # 调用客户端删除用户信息方法
                self.client.delBasicConfig(REQmsg)
        except Exception as e:
            print('on_clicked_user_del', e)

    # 处理client传回来结果的后续
    def delBasicConfigRes(self, data):
        print(f'delBasicConfigRes: {data}')
        if data[0] != '1':
            QMessageBox.information(self, "提示", data[1], QMessageBox.Yes)
            return
        self.client.getConfigData()
        # self.view.refresh(self.configInfo, self.updateBasicConfig, self.editCancel, self.delBasicConfig)

    def editCancel(self):
        try:
            reply = QMessageBox.information(self, "提示", '是否取消编辑', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                self.view.refresh(self.configInfo, self.updateBasicConfig, self.editCancel, self.delBasicConfig)
        except Exception as e:
            print('editCancel', e)

    # 取消添加用户信息方法
    def addCancel(self):
        reply = QMessageBox.information(self, "提示", '是否取消添加', QMessageBox.Yes | QMessageBox.No)
        if reply == 16384:
            self.tableWidget.setRowCount(self.tableWidget.rowCount() - 1)

    # 添加基本配置方法
    def on_clicked_basic_config_add(self):
        try:
            row_num = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row_num + 1)
            self.tableWidget.setRowHeight(row_num, 55)
            self.tableWidget.setEditTriggers(QAbstractItemView.DoubleClicked)
            # self.tableWidget.setInputMethodHints(self, Qt.ImhHiddenText)
            # 为新一行添加文本item
            for i in range(0, 5):
                self.tableWidget.setItem(row_num, i + 1, QTableWidgetItem())
                self.tableWidget.item(row_num, i + 1).setTextAlignment(Qt.AlignCenter)
                font = self.tableWidget.item(row_num, i + 1).font()
                font.setPointSize(12)

            # 为每一行的头部添加复选框
            self.tableWidget.setCellWidget(row_num, 0, QCheckBox())
            checkBox = self.tableWidget.cellWidget(row_num, 0)
            checkBox.setCheckState(QtCore.Qt.Unchecked)
            checkBox.setCheckable(True)
            checkBox.setStyleSheet('margin:10px')

            self.tableWidget.setCellWidget(row_num, 6, QCheckBox())
            checkBox2 = self.tableWidget.cellWidget(row_num, 6)
            checkBox2.setCheckState(QtCore.Qt.Unchecked)
            checkBox2.setChecked(False)
            checkBox2.setStyleSheet('margin:10px')

            # 添加最后一列
            self.tableWidget.setCellWidget(row_num, 7, QWidget())
            confirmBtn = QPushButton('确认')
            cancelBtn = QPushButton('取消')
            confirmBtn.clicked.connect(self.addBasicConfig)
            cancelBtn.clicked.connect(self.addCancel)
            confirmBtn.setStyleSheet('margin:5px;height : 50px;width:60px;font : 18px')
            cancelBtn.setStyleSheet('margin:5px;height : 50px;width:60px;font : 18px')
            layout = QHBoxLayout()
            layout.addWidget(confirmBtn)
            layout.addWidget(cancelBtn)
            spaceItem_3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            layout.addItem(spaceItem_3)
            layout.setStretch(0, 2)
            layout.setStretch(1, 2)
            layout.setStretch(2, 4)
            self.tableWidget.cellWidget(row_num, 7).setLayout(layout)
        except Exception as e:
            print('config_add', e)

    def exit(self):
        self.client.getConfigDataResSig.disconnect()
        self.client.addBasicConfigResSig.disconnect()
        self.client.updBasicConfigResSig.disconnect()
        self.client.delBasicConfigResSig.disconnect()

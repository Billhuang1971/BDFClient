import os
import mne
import math
import numpy as np
import time,datetime
import bisect
import threading
import inspect
import ctypes
import pypinyin
from PyQt5 import QtCore

from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5 import QtCore
from pyqt5_plugins.examplebutton import QtWidgets

from view.assessLabel import AssessLabelView
from view.assessLabel import SettingView
from view.assessLabel import PrentryView
from view.manual_form.combo_check_box2 import CheckableComboBox


class assessLabelController(QWidget):
    is_reload_controller = QtCore.pyqtSignal(str)
    switchToEEG = pyqtSignal(list)

    def __init__(self, appUtil=None, Widget=None, client=None, mainMenubar=None):
        super().__init__()
        self.view = QWidget()

        self.client = client
        self.appUtil = appUtil
        self.User = client.tUser
        self.curPageIndex = 1
        self.pageRows = 12
        self.curPageMax = 1
        self.classifier_key_word = None
        self.classifier_key_value = None
        self.isSearch = False
        self.searchPage = 1
        self.searchPageMax = 1
        self.search_init_info = []
        self.init_info = []
        self.file_info = []
        # self.pre_info = []

        self.client.getAssessInfoResSig.connect(self.getAssessInfoRes)
        self.client.getModelIdNameResSig.connect(self.getModelIdNameRes)
        self.client.assessClassifierInfoPagingResSig.connect(self.assessClassifierInfoPagingRes)
        self.client.getAssessFileInfoResSig.connect(self.getAssessFileInfoRes)
        self.client.getAssessInfo([self.User[0], self.User[2]])

    def getAssessInfoRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提取类型、用户信息不成功", REPData[2], QMessageBox.Yes)
                return False
            self.type_info = REPData[1]
            self.user_info = REPData[2]
            self.montages = REPData[3]
            self.type_filter = [x[1] for x in self.type_info]
            self.type_name_dic = {}
            for i in self.type_info:
                self.type_name_dic[i[0]] = i[1]
            self.user_filter = [x[3] for x in self.user_info]
            # self.set_canvas()
            # self.set_contextmenu()
            self.init_prentryView()
        except Exception as e:
            print('getAssessInfoRes', e)

    # 初始化信息选择界面（选择分类器-文件）
    def init_prentryView(self):
        try:
            self.model_id = None
            self.file_name = None

            self.prentryView = PrentryView()
            self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
            self.prentryView.setWindowTitle("信息选择")
            self.prentryView.setWindowModality(Qt.ApplicationModal)
            # self.prentryView.show()
            # self.prentryView.ui.btnConfirm.setEnabled(False)
            # self.prentryView.ui.btnReturn.setEnabled(False)
            self.prentryView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.prentryView.ui.tableWidget.resizeRowsToContents()
            self.prentryView.ui.tableWidget.resizeColumnsToContents()
            self.prentryView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.prentryView.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)
            self.prentryView.ui.btnConfirm.clicked.connect(self.on_btnConfirm_clicked)
            self.prentryView.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)
            self.page = ['model_name']
            self.client.getModelIdName([self.curPageIndex, self.pageRows, False])
            # self.init_tableWidget()
        except Exception as e:
            print('init_prentryView', e)

    def getModelIdNameRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.init_info.clear()
                self.init_info = REPData[2]
                self.curPageMax = REPData[3]
                if self.curPageMax <= 0:
                    self.curPageMax = 1
                reset = REPData[4]
                itemName = ['分类器名称']
                if reset:
                    self.isSearch = False
                    self.search_init_info.clear()
                    self.prentryView.ui.lineEdit_2.clear()
                    self.init_tableWidget(self.search_init_info, itemName)
                    self.prentryView.ui.label_2.setText("共" + str(self.searchPageMax) + "页")
                    self.prentryView.ui.label.setText(str(self.searchPage))
                    QMessageBox.information(self, '提示', '刷新页面成功', QMessageBox.Ok)
                else:
                    self.init_tableWidget(self.init_info, itemName)
                    self.prentryView.ui.label_2.setText("共" + str(self.curPageMax) + "页")
                    self.prentryView.ui.label.setText(str(self.curPageIndex))
                    self.prentryView.page_control_signal.connect(self.page_controller)
                    self.prentryView.ui.btnConfirm.setVisible(False)
                    self.prentryView.ui.btnReturn.setVisible(False)
                    self.prentryView.show()
            else:
                QMessageBox.information(self, '提示', '获取评估标注界面信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getClearLabelInfoRes', e)

    def page_controller(self, signal):
        try:
            if "home" == signal[0]:
                if self.isSearch == False:
                    if self.curPageIndex == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.curPageIndex = 1
                    self.view.ui.label.setText(str(self.curPageIndex))
                else:
                    if self.searchPage == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.searchPage = 1
                    self.view.ui.label.setText(str(self.searchPage))
            elif "pre" == signal[0]:
                if self.isSearch == False:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.curPageIndex <= 1:
                        return
                    self.curPageIndex = self.curPageIndex - 1
                    self.view.ui.label.setText(str(self.curPageIndex))
                else:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.searchPage <= 1:
                        return
                    self.searchPage = self.searchPage - 1
                    self.view.ui.label.setText(str(self.searchPage))
            elif "next" == signal[0]:
                if self.isSearch == False:
                    if self.curPageMax == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.curPageIndex = self.curPageIndex + 1
                    self.view.ui.label.setText(str(self.curPageIndex))
                else:
                    if self.searchPageMax == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.searchPage = self.searchPage + 1
                    self.view.ui.label.setText(str(self.searchPage))
            elif "final" == signal[0]:
                if self.isSearch == False:
                    if self.curPageIndex == self.curPageMax:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.curPageIndex = self.curPageMax
                    self.view.ui.label.setText(str(self.curPageMax))
                else:
                    if self.searchPage == self.searchPageMax:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.searchPage = self.searchPageMax
                    self.view.ui.label.setText(str(self.searchPageMax))
            elif "confirm" == signal[0]:
                if self.isSearch == False:
                    if self.curPageIndex == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.curPageMax < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.curPageIndex = int(signal[1])
                    self.view.ui.label.setText(signal[1])
                else:
                    if self.searchPage == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.searchPageMax < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.searchPage = int(signal[1])
                    self.view.ui.label.setText(signal[1])
            if self.isSearch == False:
                msg = [self.curPageIndex, self.pageRows, signal[0], self.isSearch]
            else:
                msg = [self.searchPage, self.pageRows, signal[0], self.isSearch, self.key_word, self.key_value]
            self.client.assessClassifierInfoPaging(msg)
        except Exception as e:
            print('page_controller', e)

    def assessClassifierInfoPagingRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提示", "跳转页面失败", QMessageBox.Yes)
                return
            else:
                isSearch = REPData[3]
                itemName = ['分类器名称']
                if isSearch:
                    self.search_init_info.clear()
                    self.search_init_info = REPData[2]
                    self.init_tableWidget(self.search_init_info, itemName)
                    self.prentryView.ui.label_2.setText("共" + str(self.searchPageMax) + "页")
                    self.prentryView.ui.label.setText(str(self.searchPage))
                    QMessageBox.information(self, "提示", "跳转页面成功", QMessageBox.Yes)
                else:
                    self.init_info.clear()
                    self.init_info = REPData[2]
                    self.init_tableWidget(self.init_info, itemName)
                    self.prentryView.ui.label_2.setText("共" + str(self.curPageMax) + "页")
                    self.prentryView.ui.label.setText(str(self.curPageIndex))
                    QMessageBox.information(self, "提示", "跳转页面成功", QMessageBox.Yes)
        except Exception as e:
            print('assessClassifierInfoPagingRes', e)



    # 初始化prentryView中表格（模型/文件）
    def init_tableWidget(self, pre_info, itemName):
        try:
            col_num = len(itemName)
            self.prentryView.ui.tableWidget.setColumnCount(col_num)
            self.prentryView.ui.tableWidget.setHorizontalHeaderLabels(itemName)
            # for i in range(col_num):
            #     header_item = QTableWidgetItem(itemName[i])
            #     font = header_item.font()
            #     font.setPointSize(12)
            #     header_item.setFont(font)
            #     header_item.setForeground(QBrush(Qt.black))
            #     self.prentryView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
            self.prentryView.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.prentryView.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            row_num = len(pre_info)
            self.prentryView.ui.tableWidget.setRowCount(row_num)
            if itemName == ['分类器名称']:
                for r in range(row_num):
                    item = QTableWidgetItem(str(pre_info[r][1]))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.prentryView.ui.tableWidget.setItem(r, 0, item)
            else:
                for r in range(row_num):
                    for c in range(col_num):
                        if c == 0:
                            item = QTableWidgetItem(str(pre_info[r][1]))
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = item.font()
                            font.setPointSize(10)
                            item.setFont(font)
                        elif c == 1:
                            item = QTableWidgetItem(str(pre_info[r][3]))
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = item.font()
                            font.setPointSize(10)
                            item.setFont(font)
                        elif c == 2:
                            item = QTableWidgetItem(str(pre_info[r][2]))
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = item.font()
                            font.setPointSize(10)
                            item.setFont(font)
                        elif c == 3:
                            item = QTableWidgetItem(str(pre_info[r][0]))
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = item.font()
                            font.setPointSize(10)
                            item.setFont(font)
                        self.prentryView.ui.tableWidget.setItem(r, c, item)
            self.prentryView.ui.tableWidget.verticalHeader().setVisible(False)
        except Exception as e:
            print('init_tableWidget', e)

    # 响应prentryView单击表格事件，选择模型/文件名
    def on_tableWidget_itemClicked(self):
        try:
            row = self.prentryView.ui.tableWidget.currentRow()
            if self.model_id == None:
                self.model_id = self.init_info[row][0]
                self.model_name = self.init_info[row][1]
                self.client.getAssessFileInfo([self.model_id])
            else:
                self.check_id = self.file_info[row][1]
                self.file_id = self.file_info[row][2]
                self.patient_id = self.pre_info[row][4]
                self.measure_date = self.pre_info[row][2]
                self.prentryView.ui.btnConfirm.setEnabled(True)
        except Exception as e:
            print('on_tableWidget_itemClicked', e)

    def getAssessFileInfoRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提示", "获取标注文件列表失败", QMessageBox.Yes)
                return
            else:
                self.pre_info = REPData[2]
                self.file_info.clear()
                self.file_info = REPData[3]
                itemName = ['病人名称', '检查单号', '检查日期', '文件名称']
                self.init_tableWidget(self.pre_info, itemName)
                self.prentryView.ui.pushButton.setVisible(False)
                self.prentryView.ui.pushButton_2.setVisible(False)
                self.prentryView.ui.pushButton_3.setVisible(False)
                self.prentryView.ui.pushButton_4.setVisible(False)
                self.prentryView.ui.pushButton_5.setVisible(False)
                self.prentryView.ui.label_2.setVisible(False)
                self.prentryView.ui.label.setVisible(False)
                self.prentryView.ui.lineEdit.setVisible(False)
                self.prentryView.ui.lineEdit_2.setVisible(False)
                self.prentryView.ui.comboBox.setVisible(False)
                self.prentryView.ui.pushButton_6.setVisible(False)
                self.prentryView.ui.pushButton_7.setVisible(False)
                self.prentryView.ui.btnReturn.setVisible(True)
                self.prentryView.ui.btnConfirm.setVisible(True)
                self.prentryView.ui.btnConfirm.setEnabled(False)
        except Exception as e:
            print('getAssessFileInfoRes', e)

    def on_btnConfirm_clicked(self):
        try:
            self.prentryView.hide()
            self.switchToEEG.emit([self.file_id, self.file_name, self.check_id, self.patient_id, self.measure_date,
                                   ['assessLabelController', '', ],
                                   "label_info", self.User[0], False, False, self.model_id])
        except Exception as ee:
            QMessageBox.information(self, '提示', f'当前文件无效:{ee}')
            return



    # prentryView返回按钮
    def on_btnReturn_clicked(self):
        try:
            self.model_id = None
            self.file_id = None
            self.check_id = None
            itemName = ['分类器名称']
            self.init_tableWidget(self.init_info, itemName)
            self.prentryView.ui.pushButton.setVisible(True)
            self.prentryView.ui.pushButton_2.setVisible(True)
            self.prentryView.ui.pushButton_3.setVisible(True)
            self.prentryView.ui.pushButton_4.setVisible(True)
            self.prentryView.ui.pushButton_5.setVisible(True)
            self.prentryView.ui.label_2.setVisible(True)
            self.prentryView.ui.label.setVisible(True)
            self.prentryView.ui.lineEdit.setVisible(True)
            self.prentryView.ui.lineEdit_2.setVisible(True)
            self.prentryView.ui.comboBox.setVisible(True)
            self.prentryView.ui.pushButton_6.setVisible(True)
            self.prentryView.ui.pushButton_7.setVisible(True)
            self.prentryView.ui.btnReturn.setVisible(False)
            self.prentryView.ui.btnConfirm.setVisible(False)
        except Exception as e:
            print('on_btnReturn_clicked', e)

    def exit(self):
        try:
            self.client.getAssessInfoResSig.disconnect()
            self.client.getModelIdNameResSig.disconnect()
            self.client.assessClassifierInfoPagingResSig.disconnect()
            self.client.getAssessFileInfoResSig.disconnect()
        except Exception as e:
            print('exit', e)
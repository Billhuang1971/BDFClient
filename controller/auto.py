
import datetime
import mne
import math
import numpy as np
import time
import threading
import weakref
import sys
import ast

import pypinyin
import pickle

from PyQt5.Qt import *

from view.auto import AutoView
from view.auto import PrentryView
from view.progressBarView import ProgressBarView
from PyQt5.QtCore import *


def get_montage_name_by_fileinfo(file_info):
    return file_info[0]


# 用函数方法返回file_info中的文件名称，方便统一修改
def get_filename_by_fileinfo(file_info):
    return file_info[1][1]


# 用函数方法返回file_info中的通道列表，方便统一修改
def get_channelList_by_fileinfo(file_info):
    return file_info[2]


# 将通道的字符串数组转换为文本格式，使用特殊字符替换连字符
def channel_array_to_text(arr):
    text = ''
    for s in arr:
        text = text + s + '#'
    return text


# 将通道的文本格式转换为字符串数组，替换特殊字符
def channel_text_to_array(text):
    list = []
    for s in text.split('#'):
        if s == '':
            continue
        list.append(s)
    return list


# class CheckBoxHeader(QHeaderView):
#     """自定义表头类"""
#
#     # 自定义 复选框全选信号
#     select_all_clicked = pyqtSignal(bool)
#     # 这4个变量控制列头复选框的样式，位置以及大小
#     _x_offset = 0
#     _y_offset = 0
#     _width = 20
#     _height = 20
#
#     def __init__(self, orientation=Qt.Horizontal, parent=None):
#         super(CheckBoxHeader, self).__init__(orientation, parent)
#         self.isOn = False
#
#     def paintSection(self, painter, rect, logicalIndex):
#         painter.save()
#         super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
#         painter.restore()
#
#         self._y_offset = int((rect.height() - self._width) / 2.)
#
#         if logicalIndex == 0:
#             option = QStyleOptionButton()
#             option.rect = QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
#             option.state = QStyle.State_Enabled | QStyle.State_Active
#             if self.isOn:
#                 option.state |= QStyle.State_On
#             else:
#                 option.state |= QStyle.State_Off
#             self.style().drawControl(QStyle.CE_CheckBox, option, painter)
#
#     def mousePressEvent(self, event):
#         index = self.logicalIndexAt(event.pos())
#         if 0 == index:
#             x = self.sectionPosition(index)
#             if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width and self._y_offset < event.pos().y() < self._y_offset + self._height:
#                 if self.isOn:
#                     self.isOn = False
#                 else:
#                     self.isOn = True
#                     # 当用户点击了行表头复选框，发射 自定义信号 select_all_clicked()
#                 self.select_all_clicked.emit(self.isOn)
#
#                 self.updateSection(0)
#         super(CheckBoxHeader, self).mousePressEvent(event)

    # 自定义信号 select_all_clicked 的槽方法
    # def change_state(self, isOn):
    #     # 如果行表头复选框为勾选状态
    #     if isOn:
    #         # 将所有的复选框都设为勾选状态
    #         for i in self.all_header_combobox:
    #             i.setCheckState(Qt.Checked)
    #     else:
    #         for i in self.all_header_combobox:
    #             i.setCheckState(Qt.Unchecked)


class autoController(QWidget):
    # scan_next_signal = pyqtSignal(int)
    total_process_value = pyqtSignal(int)

    # 自动标注控制器初始化
    def __init__(self, client, cAppUtil):
        try:
            super().__init__()
            self.client = client
            self.cAppUtil = cAppUtil
            self.view = AutoView()
            # self.root_path = self.Util.root_path
            self.model = None
            # self.click_stop_button = False
            # file_info = [[montage_name, file_name, selected_channel_list],[montage_name, file_name, selected_channel_list]]
            self.patient_id = None
            self.check_id = None
            self.file_id = None
            self.file_name = None
            # 每列一个list，0：是否配置导联方案，1：文件信息：check_id,文件名,file_id, 2:通道信息
            self.file_info = []
            self.classifier_info = []
            # 当前被扫描文件信息要通过self.file_info[self.scan_sequence]获取
            # 以下信息仅表示当前表格中选中选项的信息，而不一定是当前被扫描文件的信息.
            self.classifier_name = None
            self.classifier_id = None
            self.patient_info = []
            self.patient_name = None
            # 以上信息仅表示当前表格中选中选项的信息，而不一定是当前被扫描文件的信息
            self.montage_list = None
            self.montage_name_list = None
            self.comobobox_time_stride_items = np.around(np.arange(1., 0., -0.1, dtype='f'), 1)
            # 标记用户是否在当前脑电文件配置方案上进行过修改
            self.file_montage_update = False
            self.scan_channels_info = []
            # self.all_header_combobox = []
            # 给定一个初始进度值，让用户有开始运行的感觉
            self.apv = 10
            self.alg_page = 1
            self.alg_page_max = 1
            self.alg_page_row = 8
            self.alg_search_page = 1
            self.alg_search_page_max = 1
            self.search_algorithm_info = []
            self.alg_key_word = None
            self.alg_key_value = None
            self.is_alg_search = False
            self.timer = QTimer(self)
            # self.view.ui.btnScan.clicked.connect(self.on_btnScan_clicked)
            # self.view.ui.btnScan.setEnabled(False)
            self.view.ui.btnScan.hide()
            self.view.ui.pushButton.clicked.connect(self.on_btnMatch_clicked)
            # self.view.ui.sleep_assessment_pushButton.clicked.connect(self.on_clicked_sleep_assessment_pushButton)
            self.view.ui.fileAddbtn.clicked.connect(self.init_prentryView)
            self.view.ui.fileDelbtn.clicked.connect(self.del_file)
            self.view.ui.tableWidgetClassifierScan.itemSelectionChanged.connect(
                self.itemSelectionChanged_tableWidgetClassifierScan)
            self.view.ui.tableWidgetFile.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.view.ui.tableWidgetFile.itemSelectionChanged.connect(self.itemSelectionChanged_tableWidgetFile)
            self.view.ui.tableWidgetFile.clicked.connect(self.on_clicked_tableWidgetFile)
            self.view.ui.tableWidgetClassifierScan.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.view.ui.tableWidgetFile.setSelectionMode(QAbstractItemView.SingleSelection)
            self.view.ui.tableWidgetClassifierScan.setSelectionMode(QAbstractItemView.SingleSelection)
            # self.view.ui.sleep_assessment_pushButton.setEnabled(False)
            self.view.signal_file_info_montage_setting_save.connect(self.on_clicked_save_file_montage_setting_pushButton)
            self.view.signal_file_montage_update.connect(self.signal_response_signal_file_montage_update)
            self.view.ui.pushButton_11.clicked.connect(self.on_query_classifier_info)
            self.view.ui.pushButton_12.clicked.connect(self.on_reset_classifier_info)
            self.view.ui.horizontalLayout.setStretch(0, 1)
            self.view.ui.horizontalLayout.setStretch(1, 1)
            self.scanOutput = weakref.proxy(self.view.ui.editScanOutput)
            self.sub_scanOutput = weakref.proxy(self.view.ui.sub_editScanOutput)
            # 发送信号扫描下一个脑电文件（如果有）
            # self.scan_next_signal.connect(self.next_scan_file)
            self.total_process_value.connect(self.process_barView_progressBar_value_set)
            self.client.getAutoInitDataResSig.connect(self.getAutoInitDataRes)
            self.client.getPatientMeasureDayResSig.connect(self.getPatientMeasureDayRes)
            self.client.getPatientFileResSig.connect(self.getPatientFileRes)
            self.client.getFileChannelsResSig.connect(self.getFileChannelsRes)
            self.client.autoClassifierInfoPagingResSig.connect(self.autoClassifierInfoPagingRes)
            self.client.autoInquiryClassifierInfoResSig.connect(self.autoInquiryClassifierInfoRes)
            self.client.matchClassifierFileResSig.connect(self.matchClassifierFileRes)
            self.client.runProcessForScanResSig.connect(self.runProcessForScanRes)
            self.client.getScanProgressResSig.connect(self.getScanProgressRes)
            self.client.getAutoInitData([self.alg_page, self.alg_page_row, False])
        except Exception as e:
            print('__init__', e)


    def getAutoInitDataRes(self, REPData):
        try:
            if REPData[0] == '1':
                reset = REPData[6]
                if not reset:
                    self.montage_list = REPData[2]
                    self.montage_name_list = [montage['name'] for montage in self.montage_list]
                    print(self.montage_name_list)
                    self.patient_info = REPData[4]
                    self.view.init_file_table(self.file_info)
                self.classifier_info = REPData[3]
                self.alg_page_max = REPData[5]
                if self.alg_page_max <= 0:
                    self.alg_page_max = 1
                if reset:
                    self.view.init_classifier_table(self.classifier_info)
                    self.view.ui.label_10.setText("共" + str(self.alg_page_max) + "页")
                    self.view.ui.label_9.setText(str(self.alg_page))
                    self.view.ui.lineEdit_3.clear()
                    self.classifier_id = None
                else:
                    self.view.init_classifier_table(self.classifier_info)
                    self.view.ui.label_10.setText("共" + str(self.alg_page_max) + "页")
                    self.view.ui.label_9.setText(str(self.alg_page))
                    self.view.page_control_signal.connect((self.page_controller))
                self.init_combobox_time_stride()
            else:
                QMessageBox.information(self, '提示', '获取脑电扫描信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getAutoInitDataRes', e)

    def on_reset_classifier_info(self):
        try:
            self.alg_page = 1
            self.is_alg_search = False
            self.alg_search_page = 1
            self.alg_search_page_max = 1
            self.client.getAutoInitData([self.alg_page, self.alg_page_row, True])
        except Exception as e:
            print('on_reset_classifier_info', e)

    def on_query_classifier_info(self):
        try:
            self.alg_key_word = self.view.ui.comboBox.currentText()
            self.alg_key_value = self.view.ui.lineEdit_3.text()
            self.search_algorithm_info.clear()
            self.alg_search_page = 1
            self.is_alg_search = False
            if self.alg_key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的分类器信息', QMessageBox.Ok)
                return
            if self.alg_key_word == '分类器名称':
                self.alg_key_word = 'classifier_name'
            REQmsg = [self.alg_key_word, self.alg_key_value, self.alg_search_page, self.alg_page_row]
            self.client.autoInquiryClassifierInfo(REQmsg)
        except Exception as e:
            print('on_query_alg_info', e)

    def autoClassifierInfoPagingRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提示", "跳转页面失败", QMessageBox.Yes)
                return
            else:
                isSearch = REPData[3]
                if isSearch:
                    self.search_algorithm_info.clear()
                    self.search_algorithm_info = REPData[2]
                    self.view.init_classifier_table(self.search_algorithm_info)
                    self.view.ui.label_10.setText("共" + str(self.alg_search_page_max) + "页")
                    self.view.ui.label_9.setText(str(self.alg_search_page))
                    QMessageBox.information(self, "提示", "跳转页面成功", QMessageBox.Yes)
                else:
                    self.classifier_info.clear()
                    self.classifier_info = REPData[2]
                    self.view.init_classifier_table(self.classifier_info)
                    self.view.ui.label_10.setText("共" + str(self.alg_page_max) + "页")
                    self.view.ui.label_9.setText(str(self.alg_page))
                    QMessageBox.information(self, "提示", "跳转页面成功", QMessageBox.Yes)
        except Exception as e:
            print('autoClassifierInfoPagingRes', e)

    def autoInquiryClassifierInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.is_alg_search = True
                self.alg_search_page_max = REPData[3]
                QMessageBox.information(self, '提示', '查询分类器信息成功', QMessageBox.Ok)
                self.search_algorithm_info.clear()
                self.search_algorithm_info = REPData[2]
                self.view.init_classifier_table(self.search_algorithm_info)
                self.view.ui.label_10.setText("共" + str(self.alg_search_page_max) + "页")
                self.view.ui.label_9.setText(str(self.alg_search_page))
            else:
                self.view.ui.lineEdit_3.clear()
                QMessageBox.information(self, '提示', '查询分类器信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('autoInquiryClassifierInfoRes', e)

    def page_controller(self, signal):
        try:
            if "home" == signal[0]:
                if self.is_alg_search == False:
                    if self.alg_page == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.alg_page = 1
                    self.view.ui.label_9.setText(str(self.alg_page))
                else:
                    if self.alg_search_page == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.alg_search_page = 1
                    self.view.ui.label_9.setText(str(self.alg_search_page))
            elif "pre" == signal[0]:
                if self.is_alg_search == False:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.alg_page <= 1:
                        return
                    self.alg_page = self.alg_page - 1
                    self.view.ui.label_9.setText(str(self.alg_page))
                else:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.alg_search_page <= 1:
                        return
                    self.alg_search_page = self.alg_search_page - 1
                    self.view.ui.label_9.setText(str(self.alg_search_page))
            elif "next" == signal[0]:
                if self.is_alg_search == False:
                    if self.alg_page_max == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.alg_page = self.alg_page + 1
                    self.view.ui.label_9.setText(str(self.alg_page))
                else:
                    if self.alg_search_page_max == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.alg_search_page = self.alg_search_page + 1
                    self.view.ui.label_9.setText(str(self.alg_search_page))
            elif "final" == signal[0]:
                if self.is_alg_search == False:
                    if self.alg_page == self.alg_page_max:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.alg_page = self.alg_page_max
                    self.view.ui.label_9.setText(str(self.alg_page_max))
                else:
                    if self.alg_search_page == self.alg_search_page_max:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.alg_search_page = self.alg_search_page_max
                    self.view.ui.label_9.setText(str(self.alg_search_page_max))
            elif "confirm" == signal[0]:
                if self.is_alg_search == False:
                    if self.alg_page == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.alg_page_max < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.alg_page = int(signal[1])
                    self.view.ui.label_9.setText(signal[1])
                else:
                    if self.alg_search_page == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.alg_search_page_max < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.alg_search_page = int(signal[1])
                    self.view.ui.label_9.setText(signal[1])
            if self.is_alg_search == False:
                msg = [self.alg_page, self.alg_page_row, signal[0], self.is_alg_search]
            else:
                msg = [self.alg_search_page, self.alg_page_row, signal[0], self.is_alg_search, self.alg_key_word, self.alg_key_value]
            self.client.autoClassifierInfoPaging(msg)
        except Exception as e:
            print('page_controller', e)


    # 初始化移动步长下拉列表
    def init_combobox_time_stride(self):
        self.comobobox_time_stride_items = [str(i) for i in self.comobobox_time_stride_items]
        self.view.ui.comboBox_time_stride.addItems(self.comobobox_time_stride_items)


    # 初始化信息选择界面（选择病人-测量日期-文件）
    def init_prentryView(self):
        try:
            if self.classifier_id == None:
                QMessageBox.information(self, "提示", "请先选择扫描的分类器", QMessageBox.Yes)
                return
            limit = self.view.ui.tableWidgetFile.rowCount()
            if limit >= 1:
                QMessageBox.information(self, "提示", "仅可以添加一个脑电文件", QMessageBox.Yes)
                return
            self.patient_id = None
            self.check_id = None
            self.file_name = None
            self.prentryView = PrentryView()
            self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
            self.prentryView.setWindowTitle("信息选择")
            self.prentryView.setWindowModality(Qt.ApplicationModal)
            self.prentryView.show()
            self.prentryView.ui.btnConfirm.setEnabled(False)
            # self.prentryView.ui.btnReturn.setEnabled(False)
            self.prentryView.ui.btnReturn.setText('关闭')
            self.prentryView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.prentryView.ui.tableWidget.resizeRowsToContents()
            self.prentryView.ui.tableWidget.resizeColumnsToContents()
            self.prentryView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.prentryView.ui.tableWidget.clicked.connect(self.on_prentryView_tableWidget_itemClicked)
            self.prentryView.ui.btnConfirm.clicked.connect(self.on_btnConfirm_clicked)
            self.prentryView.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)
            self.page = ['patient_name']
            self.init_tableWidget()
        except Exception as e:
            print('init_prentryView', e)

    # 从需要扫描的脑电集合中删除选中的脑电文件
    def del_file(self):
        try:
            row = self.view.ui.tableWidgetFile.currentIndex().row()
            self.view.ui.tableWidgetFile.selectRow(row)
            self.file_info.pop(row)
            self.view.init_file_table(self.file_info)
            self.view.init_del_montage_setting_view()
        except Exception as e:
            print('del_file', e)

    # 初始化表格（病人/测量日期/文件）
    def init_tableWidget(self):
        try:
            # 清空上一阶段表格遗留下来的信息
            self.prentryView.ui.tableWidget.clear()
            if self.page == ['patient_name']:
                itemName = ['选择病人']
                self.pre_info = self.patient_info
                self.init_table(self.pre_info, itemName)
                self.enable_controls()
            elif self.page == ['measure_date']:
                self.client.getPatientMeasureDay([self.patient_id])
            elif self.page == ['file_name']:
                # 初始化文件名称和大小数组
                self.client.getPatientFile([self.check_id])
                # self.pre_info_file_size = []
                # self.prentryView.ui.tableWidget.itemClicked.connect(self.file_clicked)
        except Exception as e:
            print('init_tableWidget', e)

    def getPatientFileRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.prentryView.ui.btnConfirm.setEnabled(True)
                self.prentryView.ui.tableWidget.itemClicked.connect(self.on_prentryView_tableWidget_itemClicked)
                self.pre_info = REPData[2]
                self.pre_info_file_size = REPData[3]
                itemName = ['文件大小', '文件名称']
                self.init_table(self.pre_info, itemName)
                self.enable_controls()
            else:
                QMessageBox.information(self, '提示', '获取对应病人文件信息失败, 请重试', QMessageBox.Ok)
        except Exception as e:
            print('getPatientMeasureDayRes', e)

    def getPatientMeasureDayRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.pre_info = REPData[2]
                itemName = ['检查单号', '选择测量日期']
                self.init_table(self.pre_info, itemName)
                self.enable_controls()
            else:
                QMessageBox.information(self, '提示', '获取对应病人文件测量日期失败, 请重试', QMessageBox.Ok)
        except Exception as e:
            print('getPatientMeasureDayRes', e)

    def init_table(self, pre_info, itemName):
        try:
            # 设置表头信息
            col_num = len(itemName)
            self.prentryView.ui.tableWidget.setColumnCount(col_num)
            # 选择脑电页面，设置表头名称和复选框
            # if self.page == ['file_name']:
            #     self.setTableHeaderField(itemName)
            # # 非选择脑电页面，只设置表头名称
            # else:
            for i in range(col_num):
                header_item = QTableWidgetItem(itemName[i])
                font = header_item.font()
                font.setPointSize(12)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                self.prentryView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
            self.prentryView.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            # self.prentryView.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.prentryView.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            self.prentryView.ui.tableWidget.setAlternatingRowColors(True)  # 交替行颜色
            self.prentryView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            # 设置文件选择页面中的每行信息
            row_num = len(pre_info)
            # self.all_header_combobox = []
            self.prentryView.ui.tableWidget.setRowCount(row_num)
            # 为表格中的每个单元格填上信息，当在脑电选择页面时为表格额外添加复选框
            for r in range(row_num):
                for c in range(col_num):
                    # if c == 0 and self.page == ['file_name']:
                    #     # #当在选择脑电文件页面时，为每行添加复选框
                    #     checkbox = QCheckBox()
                    #     # 将所有的复选框都添加到 全局变量 all_header_combobox 中
                    #     self.all_header_combobox.append(checkbox)
                    #     # 为每一行的第一列添加复选框
                    #     self.prentryView.ui.tableWidget.setCellWidget(r, c, checkbox)
                    # else:
                    if itemName[c] == '文件大小' and self.page == ['file_name']:
                        item = QTableWidgetItem(str(self.pre_info_file_size[r]))
                    elif itemName[c] == '检查单号' and self.page == ['measure_date']:
                        item = QTableWidgetItem(str(pre_info[r][0]))
                    elif itemName[c] == '文件名称' and self.page == ['file_name']:
                        item = QTableWidgetItem(str(pre_info[r][1]))
                    else:
                        item = QTableWidgetItem(str(pre_info[r][1]))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.prentryView.ui.tableWidget.setItem(r, c, item)
            self.prentryView.ui.tableWidget.verticalHeader().setVisible(False)
        except Exception as e:
            print('init_table:', e)

    # 选择脑电页面，设置行表头字段
    # def setTableHeaderField(self, header_field):
    #     self.prentryView.ui.tableWidget.clear()
    #     # header = CheckBoxHeader()  # 实例化自定义表头
    #     # self.prentryView.ui.tableWidget.setHorizontalHeader(header)  # 设置表头
    #     self.prentryView.ui.tableWidget.setHorizontalHeaderLabels(header_field)  # 设置行表头字段
    #     # self.prentryView.ui.tableWidget.setColumnWidth(0, 60)  # 设置第0列宽度
    #     # self.prentryView.ui.tableWidget.setColumnWidth(1, 300)  # 设置第1列宽度
    #     # header.select_all_clicked.connect(header.change_state)  # 行表头复选框单击信号与槽

    # # 点击全选按钮
    # def header_checkbox_clicked(self):
    #     if self.header_checkbox.isChecked():
    #         for cb in self.all_header_combobox:
    #             cb.setChecked(True)
    #     else:
    #         for cb in self.all_header_combobox:
    #             cb.setChecked(False)

    def disable_controls(self):
        self.prentryView.ui.tableWidget.setEnabled(False)
        self.prentryView.ui.btnReturn.setEnabled(False)

    def enable_controls(self):
        self.prentryView.ui.tableWidget.setEnabled(True)
        self.prentryView.ui.btnReturn.setEnabled(True)

    # 响应单击表格事件，选择病人/测量日期/文件名
    def on_prentryView_tableWidget_itemClicked(self):
        try:
            row = self.prentryView.ui.tableWidget.currentRow()
            if self.patient_id == None:
                self.disable_controls()
                self.patient_id = self.pre_info[row][0]
                self.patient_name = self.pre_info[row][1]
                self.page = ['measure_date']
                self.init_tableWidget()
                self.prentryView.ui.btnReturn.setEnabled(True)
            elif self.check_id == None:
                self.disable_controls()
                self.check_id = self.pre_info[row][2]
                self.page = ['file_name']
                self.init_tableWidget()
            else:
                self.file_name = self.pre_info[row][1]
                self.file_id = self.pre_info[row][2]
                # row = self.prentryView.ui.tableWidget.currentIndex().row()
                # self.prentryView.ui.tableWidget.selectRow(row)
                self.prentryView.ui.btnConfirm.setEnabled(True)
        except Exception as e:
            print('on_prentryView_tableWidget_itemClicked', e)

    # 在脑电选择页面点击脑电选项，直接选中该行对应的复选框
    def file_clicked(self):
        if self.page == ['file_name']:
            row = self.prentryView.ui.tableWidget.currentIndex().row()
            self.prentryView.ui.tableWidget.selectRow(row)
            # if self.all_header_combobox[row].isChecked():
            #     self.all_header_combobox[row].setChecked(False)
            # else:
            #     self.all_header_combobox[row].setChecked(True)

    # 选择脑电界面，点击返回按钮
    def on_btnReturn_clicked(self):
        self.prentryView.close()

    # 选择脑电界面，点击确认按钮
    def on_btnConfirm_clicked(self):
        try:
            select_file_row = self.prentryView.ui.tableWidget.currentRow()
            if select_file_row == -1:
                QMessageBox.information(self, 'prompt', '未选择脑电文件')
                return
            # 遍历每行的checkbox，判断其是否被选中
            # for i in range(len(self.all_header_combobox)):
            #     if self.all_header_combobox[i].isChecked():
            if self.pre_info_file_size[select_file_row] == "not exists":
                QMessageBox.information(self.prentryView, "提示", "目标文件无效", QMessageBox.Yes)
                return
            # select_file_row.append(i)
            # for i in select_file_row:
                # montage_name, file_name, channel_list
            self.file_info.append(['未配置导联方案', self.pre_info[select_file_row], []])
            # self.file_info = sorted(self.file_info, key=(lambda x: get_filename_by_fileinfo(x)))
            self.view.init_file_table(self.file_info)
            self.prentryView.close()
        except Exception as e:
            print('on_btnConfirm_clicked', e)

    # 检测即将进行扫描的脑电文件信息是否符合规范
    # 主要检查相同脑电文件是否存在同样的参考方案，如果存在，则显示异常，并让用户删除出现重复参考方案的脑电文件表格中的选项
    # 是否存在还没有进行参考方案配置的脑电文件
    def if_leagel_file_info_list(self):
        if self.file_montage_update:
            QMessageBox.critical(self, 'Alert',
                                 '检测到参考方案配置进行过修改，但未保存')
            return
        # legal = False
        for i in range(len(self.file_info)):
            montage_name = self.file_info[i][0]
            name = get_filename_by_fileinfo(self.file_info[i])
            if montage_name == '未配置导联方案':
                QMessageBox.critical(self, 'Alert',
                                     '脑电文件{}还未完成导联方案配置'.format(name))
                return
        # if len(self.file_info) == 1:
        #     return True
        # # file_info中的数组是按照脑电文件名称进行排序的
        # for i in range(len(self.file_info)):
        #     montage_name = self.file_info[i][0]
        #     name = get_filename_by_fileinfo(self.file_info[i])
        #     for j in range(i + 1, len(self.file_info)):
        #         if name == get_filename_by_fileinfo(self.file_info[j]) and montage_name == self.file_info[j][0]:
        #             QMessageBox.critical(self, 'Alert',
        #                                  '脑电文件{}及参考方案{}重复，请删除重复项'.format(name, montage_name))
        #             return legal
        legal = True
        return legal

    # 自动标注页面点击扫描按钮
    def on_btnScan_clicked(self):
        try:
            self.client.runProcessForScan([self.classifier_id])
        except Exception as e:
            print('on_btnScan_clicked', e)


    def runProcessForScanRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self.view, '提示', '开启扫描进程失败, 请重试')
            else:
                self.scanOutput.clear()
                self.sub_scanOutput.clear()
                self.sub_scanOutput.appendPlainText(
                    "开始扫描:脑电文件{}".format(get_filename_by_fileinfo(self.file_info[0])))
                self.sub_scanOutput.appendPlainText(
                    "参考方案名称：{}".format(
                        self.file_info[0][0]))
                self.sub_scanOutput.appendPlainText(
                    "扫描通道：{}".format(
                        get_channelList_by_fileinfo(self.file_info[0])))
                self.lock_btn()
                # 扫描进程总进度
                self.pv = 0
                self.progressBar = ProgressBarView(window_title="扫描中", maximum=100, hasStopBtn=False)
                # self.init_process_barView()
                # self.process_barView_progressBar_value_set(self.pv)
                # # 使自动扫描窗口进入模态
                # self.process_barView._set_window_title(title="扫描中")
                # self.process_barView_progressBar_value_set(self.apv)
                # self.process_barView.setWindowModality(Qt.ApplicationModal)
                # 每3秒查询一次
                self.timer.start(3000)
                self.timer.timeout.connect(self.getScanProgress)
                self.progressBar.exec_()
                # self.process_barView.exec_()
        except Exception as e:
            print('runProcessForScanRes', e)

    def lock_btn(self):
        # self.view.ui.btnScan.setText('扫描中')
        # self.view.ui.btnScan.setEnabled(False)
        self.view.ui.tableWidgetFile.setEnabled(False)
        self.view.ui.tableWidgetClassifierScan.setEnabled(False)
        self.view.ui.pushButton.setEnabled(False)
        self.view.ui.pushButton_6.setEnabled(False)
        self.view.ui.pushButton_7.setEnabled(False)
        self.view.ui.pushButton_8.setEnabled(False)
        self.view.ui.pushButton_9.setEnabled(False)
        self.view.ui.pushButton_10.setEnabled(False)
        self.view.ui.pushButton_11.setEnabled(False)
        self.view.ui.pushButton_12.setEnabled(False)
        self.view.ui.addchannel_pushButton.setEnabled(False)
        self.view.ui.allAddchannel_pushButton.setEnabled(False)
        self.view.ui.fileAddbtn.setEnabled(False)
        self.view.ui.delchannel_pushButton.setEnabled(False)
        self.view.ui.moveup_pushButton.setEnabled(False)
        self.view.ui.movedown_pushButton.setEnabled(False)
        self.view.ui.save_file_montage_setting_pushButton.setEnabled(False)

    def getScanProgress(self):
        self.client.getScanProgress([self.client.tUser[0]])

    # def init_process_barView(self):
    #     # 总进度条视图
    #     self.process_barView = ProcessBarView()
    #     self.process_barView.ui.stop_pushButton.hide()
    #     self.process_barView.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
    #     self.total_process_value.connect(self.process_barView_progressBar_value_set)
    #     # self.process_barView.ui.stop_pushButton.clicked.connect(self.on_clicked_stop_pushButton)

    # def on_clicked_stop_pushButton(self):
    #     self.click_stop_button = True
    #     self.p.close()

    def process_bar_view_pv_update(self, scan_num, total_scan_num):
        # 查看当前扫描进度并更新进度条
        if total_scan_num != 0:
            self.pv = (scan_num / total_scan_num) * 100
            # 进度条超过初始值在更新self.pv的值
            self.pv = max(self.pv, self.apv)
            self.total_process_value.emit(self.pv)

    # 输出信息到页面
    def output_info(self, msg):
        self.scanOutput.appendPlainText(str(msg))
        self.view.ui.editScanOutput.moveCursor(self.view.ui.editScanOutput.textCursor().End)
        QApplication.processEvents()

    def scan_finished(self):
        self.view.ui.tableWidgetFile.setEnabled(True)
        self.view.ui.tableWidgetClassifierScan.setEnabled(True)
        # if self.if_sleep_scan:
        #     self.sub_scanOutput.appendPlainText("睡眠诊断结束")
        #     # self.view.ui.sleep_assessment_pushButton.setText("睡眠评估")
        #     # self.view.ui.sleep_assessment_pushButton.setEnabled(True)
        # else:
        #     self.sub_scanOutput.appendPlainText("扫描结束")
        self.view.ui.pushButton.setEnabled(True)
        self.view.ui.pushButton_6.setEnabled(True)
        self.view.ui.pushButton_7.setEnabled(True)
        self.view.ui.pushButton_8.setEnabled(True)
        self.view.ui.pushButton_9.setEnabled(True)
        self.view.ui.pushButton_10.setEnabled(True)
        self.view.ui.pushButton_11.setEnabled(True)
        self.view.ui.pushButton_12.setEnabled(True)
        self.view.ui.addchannel_pushButton.setEnabled(True)
        self.view.ui.allAddchannel_pushButton.setEnabled(True)
        self.view.ui.fileAddbtn.setEnabled(True)
        self.view.ui.delchannel_pushButton.setEnabled(True)
        self.view.ui.moveup_pushButton.setEnabled(True)
        self.view.ui.movedown_pushButton.setEnabled(True)
        self.view.ui.save_file_montage_setting_pushButton.setEnabled(True)
        # self.progressBar.updateProgressBar(100)
        # self.progressBar.close()
        # self.view.ui.btnScan.setText("扫描")
        # self.view.ui.btnScan.setEnabled(True)
        # self.pv = 100
        # self.total_process_value.emit(self.pv)
        # time.sleep(0.3)
        # self.process_barView.close()


    # 保存睡眠扫描的结果,用于给睡眠诊断模块提供数据来源
    # def save_sleep_scan_result(self):
    #     # 包含了当前脑电文件所有的标注和标注的时间起点终点下标
    #     # sleep_scan_result = {'scan_labels':self.scan_label,'start_end_timepoints':self.start_end_timepoints, 'scan_channels':self.scan_file_channel_list, 'duration_in_seconds': duration_in_seconds}
    #     sleep_scan_result = self.read_pickle(self.sleep_scan_result_path)
    #     os.remove(self.sleep_scan_result_path)
    #     montage_name = get_montage_name_by_fileinfo(self.file_info[self.scan_sequence])
    #     channel_list = get_channelList_by_fileinfo(self.file_info[self.scan_sequence])
    #     channel_list = channel_array_to_text(channel_list)
    #     file_name = get_filename_by_fileinfo(self.file_info[self.scan_sequence])
    #     patient_id, measure_date = self.get_patient_id_measeuredate_by_file_name(file_name)
    #     try:
    #         sleep_id = self.DbUtil.get_sleep_maxId() + 1
    #         self.DbUtil.add_sleep_info(sleep_id=sleep_id, file_name=file_name, classifier_id=self.classifier_id,
    #                                    montage_name=montage_name,
    #                                    channel_list=channel_list, patient_id=patient_id, measure_date=measure_date)
    #         sleep_report_name = file_name.split('.')[0] + str(sleep_id)
    #         sleep_report_name = sleep_report_name + '_{}'.format(sleep_id)
    #         self.DbUtil.update_sleep_info(set_name='report_name', set_value=sleep_report_name, where_name='sleep_id',
    #                                       where_value=sleep_id)
    #         sleep_report_path = os.path.join(self.sleep_report_path, sleep_report_name + '.pkl')
    #         self.save_file_in_pickle(sleep_scan_result, sleep_report_path)
    #     except Exception as s_result:
    #         self.output_info("睡眠诊断信息添加失败,失败原因: %s" % s_result)

    # 扫描下一个脑电文件，如果所有脑电文件都已扫描完毕则在UI页面中提示用户扫描结束
    # def next_scan_file(self, msg):
    #     # 扫描下一个文件
    #     self.scan_sequence += 1
    #     self.pv = 100 // len(self.file_info) * (self.scan_sequence)
    #     if self.scan_sequence < len(self.file_info):
    #         # 还有没扫描的脑电文件，继续扫描下一个
    #         self.scan_file_on_QProcess(self.scan_sequence, self.file_info)

    # 响应函数，点击分类器表格
    def itemSelectionChanged_tableWidgetClassifierScan(self, item=None):
        try:
            row = self.view.ui.tableWidgetClassifierScan.currentRow()
            self.status = self.classifier_info[row][14]
            self.view.ui.container.setEnabled(self.status == "waveform")
            if not self.is_alg_search:
                self.classifier_name = self.classifier_info[row][1]
                self.classifier_file_name = self.classifier_info[row][4]
                self.classifier_id = self.classifier_info[row][0]
                # self.channel_info = self.classifier_info[row][9]
                self.scan_len = self.classifier_info[row][10]
                self.config_id = self.classifier_info[row][11]
                self.current_selected_classifier_info = self.classifier_info[row]
                self.current_selected_classifier_set_id = self.current_selected_classifier_info[3]
            else:
                self.classifier_name = self.search_algorithm_info[row][1]
                self.classifier_file_name = self.search_algorithm_info[row][4]
                self.classifier_id = self.search_algorithm_info[row][0]
                # self.channel_info = self.classifier_info[row][9]
                self.scan_len = self.search_algorithm_info[row][10]
                self.config_id = self.search_algorithm_info[row][11]
                self.current_selected_classifier_info = self.search_algorithm_info[row]
                self.current_selected_classifier_set_id = self.current_selected_classifier_info[3]
            # self.if_import_model = False
            # if self.current_selected_classifier_set_id == None:
            #     self.if_import_model = True
            self.scanOutput.clear()
            self.view.ui.label_classifiername.setText('当前已选择分类器:{}'.format(self.classifier_name))
        except Exception as e:
            print('itemSelectionChanged_tableWidgetClassifierScan', e)

    # 响应函数，点击脑电文件表格项目
    def itemSelectionChanged_tableWidgetFile(self):
        try:
            row = self.view.ui.tableWidgetFile.currentRow()
            # 保存当前选择并进行编辑的脑电文件的行下表，currentRow拿到的可能是错误的，所以需要在此进行保存一次下标
            self.file_current_selected_row = row
            # 删除脑电文件造成的触发, 或正在更新脑电配置
            if row == -1 or self.file_montage_update:
                return
            # 读取已选脑电文件的参考方案，以及通道列表
            montage_name = self.file_info[row][0]
            file_name = get_filename_by_fileinfo(self.file_info[row])
            selected_file_info = self.file_info[row]
            channel_list = get_channelList_by_fileinfo(self.file_info[row])
            self.client.getFileChannels(REQmsg=[self.check_id, file_name, selected_file_info])
            # self.view.set_selected_filename(file_name)
            # # if montage_name not in self.montage_name_list:
            # self.view.init_file_montage_setting_view(self.montage_name_list, self.montage_list, include_channels_in_file,
            #                                          selected_file_info)
        except Exception as e:
            print('itemSelectionChanged_tableWidgetFile', e)

    def getFileChannelsRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提示", "获取脑电文件通道信息失败, 请重新尝试", QMessageBox.Yes)
                return
            else:
                include_channels_in_file = REPData[2]
                file_name = REPData[3]
                selected_file_info = REPData[5]
                EEG = REPData[6]
                self.view.set_selected_filename(file_name)
                if EEG == "EEG":
                    self.view.init_file_montage_setting_view(self.montage_name_list, self.montage_list,
                                                         include_channels_in_file,
                                                         selected_file_info)
                else:
                    monopole = []
                    bipolar = []
                    self.dgroup = self.bdfMontage(include_channels_in_file)
                    dgroupKeys = list(self.dgroup.keys())
                    glen = len(dgroupKeys)
                    for i in range(glen):
                        chs = self.dgroup.get(dgroupKeys[i])
                        for j in range(len(chs) - 1):
                            chs[j] = chs[j].split('-')[0]
                            chs[j + 1] = chs[j + 1].split('-')[0]
                            ch1 = "-".join([chs[j], chs[j + 1]])  # 单极
                            monopole.append(ch1)
                            if j < len(chs) - 2:
                                chs[j + 2] = chs[j + 2].split('-')[0]
                                ch2 = "-".join([chs[j], chs[j + 2]])
                                bipolar.append(ch2)
                    self.view.init_file_montage_setting_view(["Default", "单极", "双极"], [{"channels": include_channels_in_file, "name": "Default"}, {"channels": monopole, "name": "单极"}, {"channels": bipolar, "name": "双极"}], include_channels_in_file, selected_file_info)
        except Exception as e:
            print('getFileChannelsRes', e)

    def bdfMontage(self, channels):
        dgroup = {}
        for channel in channels:
            ch = channel.split('-')[0]
            idx = len(ch) - 1
            while idx >= 0:
                if not ch[idx].isdigit():
                    break
                idx -= 1
            key = ch[:idx + 1]
            if key in dgroup.keys():
                dgroup[key].append(channel)
            else:
                dgroup[key] = [channel]
        return dgroup

    def on_clicked_tableWidgetFile(self):
        try:
            if self.file_montage_update:
                QMessageBox.information(self.view, "提示", "请先完成方案保存，在尝试重新选择脑电文件", QMessageBox.Yes)
                return
        except Exception as e:
            print('on_clicked_tableWidgetFile', e)

    def on_clicked_save_file_montage_setting_pushButton(self, items):
        self.file_info[self.file_current_selected_row] = items
        self.scan_channels_info = items[2]
        self.view.init_file_table(self.file_info)

    # def get_file_channels(self, file_name):
    #     raw = self.load_file_raw(file_name)
    #     channel_info = raw.info['ch_names']
    #     channel_list = []
    #     for item in channel_info:
    #         item = item.split(' ')
    #         channel_list.append(item[-1])
    #     return channel_list

    def signal_response_signal_file_montage_update(self, signal):
        self.file_montage_update = signal
        if self.file_montage_update:
            # 设置编辑触发器模式为 NoEditTriggers，锁死表格
            self.view.ui.tableWidgetFile.setSelectionMode(QAbstractItemView.NoSelection)
        else:
            self.view.ui.tableWidgetFile.setSelectionMode(QAbstractItemView.SingleSelection)

    # # 加载脑电文件
    # def load_file_raw(self, file_name):
    #     try:
    #         path = self.get_filepath_by_name(file_name)
    #         raw = mne.io.read_raw_edf(path)
    #         return raw
    #     except:
    #         QMessageBox.information(self, '提示', '当前文件无效')
    #         return
    #
    # # 通过脑电名称，获取脑电文件存储路径
    # def get_filepath_by_name(self, file_name):
    #     temp = file_name.split('_')
    #     patiend_id = int(temp[0])
    #     patient_name = self.DbUtil.get_patientInfo('patient_id', patiend_id)[0][1]
    #     patient_name = ''.join(pypinyin.lazy_pinyin(patient_name, pypinyin.Style.NORMAL))
    #     subfile_name = temp[0] + '_' + patient_name
    #     file_path = os.path.join(self.root_path, 'data', 'formated_data', subfile_name, file_name)
    #     return file_path

    # # 通过脑电文件名称，返回该文件对应的病人id和测量日期
    # def get_patient_id_measeuredate_by_file_name(self, file_name):
    #     s = file_name.split('_')
    #     id = int(s[0])
    #     measuredate = s[1].split('.')[0]
    #     return id, measuredate

    # 自动扫描总进度条，值设置
    def process_barView_progressBar_value_set(self, process_value):
        pv = int(process_value)
        self.progressBar.ui.progressBar.setValue(process_value)

    # 判断当前使用模型是否为睡眠标注模型
    # def if_sleep_annotation_algorithm(self):
    #     parameters = self.predict_algorithm_parameters
    #     para = parameters.split(' ')
    #     for p in para:
    #         name, attribute = p.split('-')
    #         if name == 'sleepAnnotationAlgorithm':
    #             if attribute == 'True':
    #                 self.if_sleep_scan = True
    #                 return True
    #             else:
    #                 self.if_sleep_scan = False
    #                 return False
    #     raise ValueError("parameters 中缺少对sleepAnnotationAlgorithm的描述")

    def on_btnMatch_clicked(self):
        try:
            self.view.ui.pushButton.setEnabled(False)
            if not self.file_info:
                QMessageBox.critical(self, 'Alert', '未选择脑电文件')
                self.view.ui.pushButton.setEnabled(True)
                return
            if self.classifier_id == None:
                QMessageBox.critical(self, 'Alert', '未选择分类器')
                self.view.ui.pushButton.setEnabled(True)
                return
            if self.status == "waveform" and not self.if_leagel_file_info_list():
                self.view.ui.pushButton.setEnabled(True)
                return
            row = self.view.ui.tableWidgetClassifierScan.currentRow()
            if self.is_alg_search:
                alg_id = self.search_algorithm_info[row][2]
            else:
                alg_id = self.classifier_info[row][2]
            self.client.matchClassifierFile([self.classifier_id, self.check_id, self.file_id, self.scan_channels_info,
                                             self.comobobox_time_stride_items[self.view.ui.comboBox_time_stride.currentIndex()], alg_id])
        except Exception as e:
            print('on_btnMatch_clicked', e)

    def matchClassifierFileRes(self, REPData):
        try:
            if REPData[0] == '0':
                self.view.ui.pushButton.setEnabled(True)
                if REPData[1] == "当前服务器存在正在执行的训练、测试或扫描任务":
                    QMessageBox.information(self.view, '提示', '当前服务器存在正在执行的训练、测试或扫描任务',
                                            QMessageBox.Yes)
                elif REPData[1] == "当前分类器未上传预测文件":
                    QMessageBox.information(self.view, '提示', '当前分类器未上传预测算法文件',
                                            QMessageBox.Yes)
                else:
                    QMessageBox.information(self.view, '提示', '分类器脑电文件匹配失败', QMessageBox.Yes)
            else:
                self.custom_msg_box = CustomMessageBox()
                self.timer_2 = QTimer()
                self.timer_2.start(20000)
                self.timer_2.timeout.connect(self.scan_cancel)
                result = self.custom_msg_box.exec_()
                if result == QMessageBox.AcceptRole:
                    self.on_btnScan_clicked()
                else:
                    self.scan_cancel()
        except Exception as e:
            print('matchClassifierFileRes', e)

    def refresh_scan_btn(self):
        self.view.ui.btnScan.setEnabled(True)

    def scan_cancel(self):
        print('start')
        self.custom_msg_box.close()
        self.view.ui.pushButton.setEnabled(True)
        self.timer_2.stop()
        self.client.scan_cancel([self.client.tUser[0]])

    def getScanProgressRes(self, REPData):
        try:
            if REPData[0] == '0':
                self.scan_finished()
                self.timer.stop()
                QMessageBox.information(self.view, '提示', '读取进度信息失败', QMessageBox.Yes)
            else:
                if REPData[3]:
                    for i in REPData[3]:
                        temp = str(i)
                        # temp += "\n"
                        self.output_info(temp)
                if REPData[2] == False:
                    self.timer.stop()
                    if REPData[5] == False:
                        self.sub_scanOutput.appendPlainText("扫描结束")
                        self.sub_scanOutput.appendPlainText('算法运行失败')
                        QMessageBox.information(self.view, '提示', '算法运行失败', QMessageBox.Yes)
                    else:
                        self.sub_scanOutput.appendPlainText("扫描结束")
                        self.sub_scanOutput.appendPlainText('算法运行成功')
                        QMessageBox.information(self.view, '提示', '算法运行成功', QMessageBox.Yes)
                    # self.progressBar.updateProgressBar(100)
                    self.progressBar.close()
                    self.scan_finished()
                else:
                    scan_num = REPData[4]
                    total_scan_num = REPData[5]
                    self.process_bar_view_pv_update(scan_num, total_scan_num)
                    # if total_scan_num != 0:
                    #     self.pv += (scan_num / total_scan_num) * 100
                    #     # 进度条超过初始值在更新self.pv的值
                    #     self.pv = max(self.pv, self.apv)
                    #     self.progressBar.updateProgressBar(self.pv)
        except Exception as e:
            print('getScanProgressRes', e)

    def exit(self):
        try:
            self.client.getAutoInitDataResSig.disconnect()
            self.client.getPatientMeasureDayResSig.disconnect()
            self.client.getPatientFileResSig.disconnect()
            self.client.getFileChannelsResSig.disconnect()
            self.client.autoClassifierInfoPagingResSig.disconnect()
            self.client.autoInquiryClassifierInfoResSig.disconnect()
            self.client.matchClassifierFileResSig.disconnect()
            self.client.runProcessForScanResSig.disconnect()
            self.client.getScanProgressResSig.disconnect()
        except Exception as e:
            print('exit', e)
class CustomMessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("提示")
        self.setText("分类器与脑电文件匹配成功,是否开始扫描。")

        # 创建自定义按钮并设置名称
        button1 = QPushButton("扫描")
        button2 = QPushButton("不扫描")

        # 将按钮添加到消息框中
        self.addButton(button1, QMessageBox.AcceptRole)
        self.addButton(button2, QMessageBox.RejectRole)
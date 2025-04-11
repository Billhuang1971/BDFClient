import mne
import os
import datetime
import time

from PyQt5.Qt import *
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor
from view.clearLabel import clearLabelView
import re

class clearLabelController(QWidget):
    is_reload_controller = pyqtSignal(str)

    def __init__(self, client, cAppUtil):
        try:
            super().__init__()
            self.client = client
            self.cAppUtil = cAppUtil
            self.view = clearLabelView()
            self.view.ui.btnSelect.clicked.connect(self.on_btnSelect_clicked_classifier)
            self.view.ui.btnReset.clicked.connect(self.on_btnRest_classifier_clicked)
            self.view.ui.btnDel.clicked.connect(self.on_btnDel_clicked)
            self.view.ui.btnDelAll.clicked.connect(self.on_btnDelAll_clicked)
            self.view.ui.btnAssess.clicked.connect(self.on_btnAssesse_clicked)
            self.view.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)
            self.view.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.view.ui.tableWidget.resizeRowsToContents()
            self.view.ui.tableWidget.resizeColumnsToContents()
            self.view.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.view.ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
            self.view.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)
            self.view.ui.btnReturn.setEnabled(False)
            self.view.ui.btnDel.setVisible(False)
            self.view.ui.btnDelAll.setVisible(False)
            # self.view.ui.btnReset.setVisible(False)
            self.view.ui.btnAssess.setVisible(False)
            # self.view.ui.btnSelect.setVisible(False)
            # self.view.ui.lineValue.setVisible(False)
            # self.view.ui.comboCond.setVisible(False)
            self.view.ui.label.setVisible(False)
            self.curPageIndex = 1
            self.pageRows = 24
            self.curPageMax = 1
            self.classifier_key_word = None
            self.classifier_key_value = None
            self.isSearch = False
            self.searchPage = 1
            self.searchPageMax = 1
            self.search_init_info = []
            self.sampling_rate = None
            self.count = 0
            self.model_id = None
            self.file_name = None
            self.check_id = None
            self.file_id = None
            self.init_info = []
            self.patient_info = []
            self.header = ['通道', '起始(h:m:s)', '结束(h:m:s)', '模型标注', '用户', '用户标注']
            self.field = ['channel', 'begin', 'end', 'mtype_id', 'uid', 'utype_id']
            self.item = ['分类器名称']
            self.file_1 = ['classifier_name']
            self.scan_info = []
            self.model_name = None
            self.is_scan_file = False
            # self.page = ['model_name']
            self.client.getClearLabelInfo([self.curPageIndex, self.pageRows, False, self.client.tUser[12]])
            self.client.getClearLabelInfoResSig.connect(self.getClearLabelInfoRes)
            self.client.inquiryScanClassifierInfoResSig.connect(self.inquiryScanClassifierInfoRes)
            self.client.scanClassifierInfoPagingResSig.connect(self.scanClassifierInfoPagingRes)
            self.client.getScanInfoResSig.connect(self.getScanInfoRes)
            self.client.getCurClearLabelInfoResSig.connect(self.getCurClearLabelInfoRes)
            self.client.getScanFileInfoResSig.connect(self.getScanFileInfoRes)
            self.client.delLabelListInfoResSig.connect(self.delLabelListInfoRes)
            self.client.delLabelByModelFileResSig.connect(self.delLabelByModelFileRes)
            self.client.getSearchScanFileInfoResSig.connect(self.getSearchScanFileInfoRes)
            self.client.getLabelInfoByAssessResSig.connect(self.getLabelInfoByAssessRes)
        except Exception as e:
            print('__init__', e)

    def getClearLabelInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.init_info.clear()
                self.init_info = REPData[2]
                self.curPageMax = REPData[3]
                if self.curPageMax <= 0:
                    self.curPageMax = 1
                reset = REPData[4]
                itemName = ['分类器名称', '标注文件数', '标注数量', '已评估', '未评估']
                if reset:
                    self.isSearch = False
                    self.search_init_info.clear()
                    self.view.ui.lineValue.clear()
                    self.view.initView(self.init_info, itemName)
                    self.view.ui.label_3.setText("共" + str(self.searchPageMax) + "页")
                    self.view.ui.label_2.setText(str(self.searchPage))
                    QMessageBox.information(self, '提示', '刷新页面成功', QMessageBox.Ok)
                else:
                    self.view.initView(self.init_info, itemName)
                    self.view.ui.label_3.setText("共" + str(self.curPageMax) + "页")
                    self.view.ui.label_2.setText(str(self.curPageIndex))
                    self.view.page_control_signal.connect(self.page_controller)
                    self.init_comboCond(self.file_1, self.item)
                    self.sampling_rate = REPData[5]
            else:
                QMessageBox.information(self, '提示', '获取清理标注界面信息失败,请重试', QMessageBox.Ok)
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
                    self.view.ui.label_2.setText(str(self.curPageIndex))
                else:
                    if self.searchPage == 1:
                        QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                        return
                    self.searchPage = 1
                    self.view.ui.label_2.setText(str(self.searchPage))
            elif "pre" == signal[0]:
                if self.isSearch == False:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.curPageIndex <= 1:
                        return
                    self.curPageIndex = self.curPageIndex - 1
                    self.view.ui.label_2.setText(str(self.curPageIndex))
                else:
                    if 1 == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                        return
                    if self.searchPage <= 1:
                        return
                    self.searchPage = self.searchPage - 1
                    self.view.ui.label_2.setText(str(self.searchPage))
            elif "next" == signal[0]:
                if self.isSearch == False:
                    if self.curPageMax == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.curPageIndex = self.curPageIndex + 1
                    self.view.ui.label_2.setText(str(self.curPageIndex))
                else:
                    if self.searchPageMax == int(signal[1]):
                        QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                        return
                    self.searchPage = self.searchPage + 1
                    self.view.ui.label_2.setText(str(self.searchPage))
            elif "final" == signal[0]:
                if self.isSearch == False:
                    if self.curPageIndex == self.curPageMax:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.curPageIndex = self.curPageMax
                    self.view.ui.label_2.setText(str(self.curPageMax))
                else:
                    if self.searchPage == self.searchPageMax:
                        QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                        return
                    self.searchPage = self.searchPageMax
                    self.view.ui.label_2.setText(str(self.searchPageMax))
            elif "confirm" == signal[0]:
                if self.isSearch == False:
                    if self.curPageIndex == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.curPageMax < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.curPageIndex = int(signal[1])
                    self.view.ui.label_2.setText(signal[1])
                else:
                    if self.searchPage == int(signal[1]):
                        QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                        return
                    if self.searchPageMax < int(signal[1]) or int(signal[1]) < 0:
                        QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                        return
                    self.searchPage = int(signal[1])
                    self.view.ui.label_2.setText(signal[1])
            if self.isSearch == False:
                msg = [self.curPageIndex, self.pageRows, signal[0], self.isSearch]
            else:
                msg = [self.searchPage, self.pageRows, signal[0], self.isSearch, self.key_word, self.key_value]
            self.client.scanClassifierInfoPaging(msg)
        except Exception as e:
            print('page_controller', e)

    def scanClassifierInfoPagingRes(self, REPData):
        try:
            if REPData[0] == '0':
                QMessageBox.information(self, "提示", "跳转页面失败", QMessageBox.Yes)
                return
            else:
                isSearch = REPData[3]
                itemName = ['分类器名称', '标注文件数', '标注数量', '已评估', '未评估']
                if isSearch:
                    self.search_init_info.clear()
                    self.search_init_info = REPData[2]
                    self.view.initView(self.search_init_info, itemName)
                    self.view.ui.label_3.setText("共" + str(self.searchPageMax) + "页")
                    self.view.ui.label_2.setText(str(self.searchPage))
                    QMessageBox.information(self, "提示", "跳转页面成功", QMessageBox.Yes)
                else:
                    self.init_info.clear()
                    self.init_info = REPData[2]
                    self.view.initView(self.init_info, itemName)
                    self.view.ui.label_3.setText("共" + str(self.curPageMax) + "页")
                    self.view.ui.label_2.setText(str(self.curPageIndex))
                    QMessageBox.information(self, "提示", "跳转页面成功", QMessageBox.Yes)
        except Exception as e:
            print('autoClassifierInfoPagingRes', e)

    def init_comboCond(self, file_1, item):
        self.view.ui.comboCond.clear()
        for i in range(len(file_1)):
            self.view.ui.comboCond.addItem(item[i], file_1[i])
        self.view.ui.comboCond.setSizeAdjustPolicy(QComboBox.AdjustToContents)

    # 初始化 模型列表/模型标注的文件列表
    # def init_tableWidget(self):
    #     try:
    #         self.view.ui.tableWidget.clear()
    #         # if self.page == ['model_name']:
    #         itemName = ['模型名称', '标注文件数', '标注数量', '已评估', '未评估']
    #         #     self.pre_info = self.DbUtil.get_modelIdName()
    #         # elif self.page == ['file_name']:
    #         #     itemName = ['文件名', '病人','标注数量','已评估','未评估']
    #         #     self.pre_info = self.DbUtil.get_fileNameByModel('mid', self.model_id)
    #
    #         col_num = 5
    #         self.view.ui.tableWidget.setColumnCount(col_num)
    #         for i in range(col_num):
    #             header_item = QTableWidgetItem(itemName[i])
    #             font = header_item.font()
    #             font.setPointSize(12)
    #             header_item.setFont(font)
    #             header_item.setForeground(QBrush(Qt.black))
    #             self.view.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
    #         self.view.ui.tableWidget.horizontalHeader().setHighlightSections(False)
    #         self.view.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    #
    #         row_num = len(self.pre_info)
    #         self.view.ui.tableWidget.setRowCount(row_num)
    #         for c in range(col_num):
    #             for r in range(row_num):
    #                 if self.page == ['model_name']:
    #                     if c == 1:
    #                         item = QTableWidgetItem(str(len(self.DbUtil.get_fileNameByModel('mid', self.pre_info[r][0]))))
    #                     elif c == 2:
    #                         item = QTableWidgetItem(str(len(self.DbUtil.get_labelInfoByModel(self.pre_info[r][0]))))
    #                     elif c == 3:
    #                         item = QTableWidgetItem(str(len(self.DbUtil.get_labelInfoByAssess(self.pre_info[r][0], 1))))
    #                     elif c == 4:
    #                         item = QTableWidgetItem(str(len(self.DbUtil.get_labelInfoByAssess(self.pre_info[r][0], 0))))
    #                     else:
    #                         item = QTableWidgetItem(str(self.pre_info[r][1]))
    #                 elif self.page == ['file_name']:
    #                     if c == 1:
    #                         item = QTableWidgetItem(str(self.DbUtil.get_patientInfo('patient_id', int(self.pre_info[r][1].split('_')[0]))[0][1]))
    #                     elif c == 2:
    #                         item = QTableWidgetItem(str(len(self.DbUtil.get_labelInfoByModel(self.model_id, self.pre_info[r][1]))))
    #                     elif c == 3:
    #                         item = QTableWidgetItem(str(len(self.DbUtil.get_labelInfoByAssess(self.model_id, 1, self.pre_info[r][1]))))
    #                     elif c == 4:
    #                         item = QTableWidgetItem(str(len(self.DbUtil.get_labelInfoByAssess(self.model_id, 0, self.pre_info[r][1]))))
    #                     else:
    #                         item = QTableWidgetItem(str(self.pre_info[r][1]))
    #                 item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #                 font = item.font()
    #                 font.setPointSize(10)
    #                 item.setFont(font)
    #                 self.view.ui.tableWidget.setItem(r, c, item)
    #         # self.view.ui.tableWidget.verticalHeader().setVisible(False)
    #     except Exception as e:
    #         print('init_tableWidget', e)

    def on_tableWidget_itemClicked(self):
        try:
            row = self.view.ui.tableWidget.currentRow()
            if self.model_name == None:
                self.model_name = self.init_info[row][0]
                self.page = ['file_name']
                self.client.getScanInfo([self.model_name, False])
            elif self.check_id == None:
                self.model_id = self.patient_info[row][0]
                self.check_id = self.patient_info[row][1]
                self.file_id = self.patient_info[row][2]
                self.page = ['label_list']
                self.client.getScanFileInfo([self.model_id, self.check_id, self.file_id, False])
        except Exception as e:
            print('on_tableWidget_itemClicked', e)

    def getScanFileInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                reset = REPData[3]
                self.label_info = REPData[2]
                if reset == True:
                    self.is_scan_file = False
                    self.view.ui.lineValue.clear()
                    self.init_table(self.label_info)
                    return
                self.file_name = "{:>03}.bdf".format(self.file_id)
                self.view.ui.btnDel.setVisible(True)
                self.view.ui.btnDelAll.setVisible(True)
                self.view.ui.btnReset.setVisible(True)
                self.view.ui.btnReset.clicked.disconnect(self.on_btnRest_classifier_clicked)
                self.view.ui.btnReset.clicked.connect(self.on_btnRest_scanFileInfo_clicked)
                self.view.ui.btnAssess.setVisible(True)
                self.view.ui.btnSelect.setVisible(True)
                self.view.ui.btnSelect.clicked.disconnect(self.on_btnSelect_clicked_classifier)
                self.view.ui.btnSelect.clicked.connect(self.on_btnSelect_clicked_scanFileInfo)
                self.view.ui.lineValue.setVisible(True)
                self.view.ui.comboCond.setVisible(True)
                self.view.ui.label.setVisible(True)
                self.view.ui.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
                self.init_table(self.label_info)
        except Exception as e:
            print('getScanFileInfoRes', e)

    def on_btnRest_scanFileInfo_clicked(self):
        try:
            self.client.getScanFileInfo([self.model_id, self.check_id, self.file_id, True])
        except Exception as e:
            print('on_btnRest_scanFileInfo_clicked', e)

    def on_btnSelect_clicked_scanFileInfo(self):
        try:
            self.is_scan_file = True
            index = self.view.ui.comboCond.currentIndex()
            cond = self.view.ui.comboCond.itemData(index)
            value = self.view.ui.lineValue.text()
            if value:
                self.client.getSearchScanFileInfo([cond, value, self.model_id, self.check_id, self.file_id, index])
            else:
                QMessageBox.information(self, "提示", "请输入查询信息", QMessageBox.Yes)
                return
        except Exception as e:
            print('on_btnSelect_clicked_scanFileInfo', e)

    def getSearchScanFileInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                print('start')
                index = REPData[3]
                self.search_label_info = REPData[2]
                self.file_name = "{:>03}.bdf".format(self.file_id)
                self.view.ui.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)
                self.init_table(self.search_label_info)
                self.view.ui.comboCond.setCurrentIndex(index)
            else:
                QMessageBox.information(self, "提示", "查询失败", QMessageBox.Yes)
                return
        except Exception as e:
            print('getSearchScanFileInfo', e)

    def getScanInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.scan_info.clear()
                self.scan_info = REPData[2]
                self.patient_info.clear()
                self.patient_info = REPData[3]
                itemName = ['文件名', '病人', '标注数量', '已评估', '未评估']
                self.view.initView(self.scan_info, itemName)
                self.view.ui.btnDel.setVisible(False)
                self.view.ui.btnDelAll.setVisible(False)
                self.view.ui.btnReset.setVisible(False)
                self.view.ui.btnAssess.setVisible(False)
                self.view.ui.btnSelect.setVisible(False)
                self.view.ui.lineValue.setVisible(False)
                self.view.ui.comboCond.setVisible(False)
                self.view.ui.label.setVisible(False)
                self.view.ui.pushButton.setVisible(False)
                self.view.ui.pushButton_2.setVisible(False)
                self.view.ui.pushButton_3.setVisible(False)
                self.view.ui.pushButton_4.setVisible(False)
                self.view.ui.pushButton_5.setVisible(False)
                self.view.ui.label_2.setVisible(False)
                self.view.ui.label_3.setVisible(False)
                self.view.ui.label_4.setVisible(False)
                self.view.ui.lineEdit.setVisible(False)
                self.view.ui.btnReturn.setEnabled(True)
                back = REPData[4]
                if back:
                    self.model_id = None
                    self.check_id = None
                    self.file_id = None
                    self.page = ['file_name']
                    self.view.ui.btnSelect.clicked.disconnect(self.on_btnSelect_clicked_scanFileInfo)
                    self.view.ui.btnSelect.clicked.connect(self.on_btnSelect_clicked_classifier)
                    self.view.ui.btnReset.clicked.disconnect(self.on_btnRest_scanFileInfo_clicked)
                    self.view.ui.btnReset.clicked.connect(self.on_btnRest_classifier_clicked)
            else:
                QMessageBox.information(self, '提示', '获取清理标注界面信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('getScanInfoRes', e)

    def on_btnReturn_clicked(self):
        if self.page == ['label_list']:
            self.client.getScanInfo([self.model_name, True])
            # self.check_id = None
            # self.file_id = None
            # self.page = ['file_name']
        elif self.page == ['file_name']:
            self.client.getCurClearLabelInfo([self.curPageIndex, self.pageRows])
            # self.view.ui.btnReturn.setEnabled(False)

    def getCurClearLabelInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.init_info.clear()
                self.init_info = REPData[2]
                self.curPageMax = REPData[3]
                if self.curPageMax <= 0:
                    self.curPageMax = 1
                itemName = ['分类器名称', '标注文件数', '标注数量', '已评估', '未评估']
                self.view.initView(self.init_info, itemName)
                self.view.ui.label_3.setText("共" + str(self.curPageMax) + "页")
                self.view.ui.label_2.setText(str(self.curPageIndex))
                self.init_comboCond(self.file_1, self.item)
                self.view.ui.btnDel.setVisible(False)
                self.view.ui.btnDelAll.setVisible(False)
                self.view.ui.btnReset.setVisible(True)
                self.view.ui.btnAssess.setVisible(False)
                self.view.ui.btnSelect.setVisible(True)
                self.view.ui.lineValue.setVisible(True)
                self.view.ui.comboCond.setVisible(True)
                self.view.ui.label.setVisible(False)
                self.view.ui.pushButton.setVisible(True)
                self.view.ui.pushButton_2.setVisible(True)
                self.view.ui.pushButton_3.setVisible(True)
                self.view.ui.pushButton_4.setVisible(True)
                self.view.ui.pushButton_5.setVisible(True)
                self.view.ui.label_2.setVisible(True)
                self.view.ui.label_3.setVisible(True)
                self.view.ui.label_4.setVisible(True)
                self.view.ui.lineEdit.setVisible(True)
                self.model_id = None
                self.model_name = None
                self.file_name = None
                self.page = ['model_name']
                self.view.ui.btnReturn.setEnabled(False)
            else:
                QMessageBox.information(self, '提示', '返回上一级页面失败, 请重试', QMessageBox.Ok)
        except Exception as e:
            print('getClearLabelInfoRes', e)

    # 显示标注
    def init_table(self, data):
        try:
            self.view.ui.tableWidget.clear()
            col_num = len(self.header)
            row_num = len(data)
            self.view.ui.tableWidget.setColumnCount(col_num)
            self.view.ui.tableWidget.setRowCount(row_num)
            for i in range(col_num):
                header_item = QTableWidgetItem(self.header[i])
                font = header_item.font()
                font.setPointSize(16)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                header_item.setData(Qt.UserRole, self.field[i])
                self.view.ui.tableWidget.setHorizontalHeaderItem(i, header_item)

            for r in range(row_num):
                for c in range(col_num):
                    if c == 1 or c ==2:
                        be_t = data[r][c] / self.sampling_rate
                        ms = int(be_t * 1000) % 1000
                        be_t = time.strftime('%H:%M:%S.{:03}'.format(ms), time.gmtime(be_t))
                        item = QTableWidgetItem(str(be_t))
                    else:
                        item = QTableWidgetItem(str(data[r][c]))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.view.ui.tableWidget.setItem(r, c, item)
            self.init_comboCond(self.field, self.header)
            self.view.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.view.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.view.ui.label.setText('模型:' + self.model_name + '   文件名:' + self.file_name + '   当前页面记录数:'+str(len(data)))
        except Exception as e:
            print('init_table', e)

    # 初始化筛选条件下拉框
    # def init_comboCond(self):
    #     self.view.ui.comboCond.clear()
    #     for i in range(len(self.field)):
    #         self.view.ui.comboCond.addItem(self.header[i], self.field[i])

    # 删除单行或多行标注
    def on_btnDel_clicked(self):
        try:
            row_num = -1
            for i in self.view.ui.tableWidget.selectionModel().selection().indexes():
                row_num = i.row()
            answer = QMessageBox.warning(
                self.view, '确认删除！', '您将进行删除操作！',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if answer == QMessageBox.Yes:
                if row_num == -1:
                    QMessageBox.information(self.view, ' ', '请至少选中一行')
                    return
                del_info = []
                for i in self.view.ui.tableWidget.selectionModel().selectedRows():
                    row = i.row()
                    sample = self.label_info[row]
                    channel = sample[0]
                    begin = sample[1]
                    temp = []
                    temp.append(self.model_id)
                    temp.append(self.check_id)
                    temp.append(self.file_id)
                    temp.append(begin)
                    temp.append(channel)
                    del_info.append(temp)
                self.client.delLabelListInfo(del_info)
        except Exception as e:
            print('on_btnDel_clicked', e)

    def delLabelListInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                QMessageBox.information(self, "提示", "删除标注信息成功")
                self.is_reload_controller.emit("assessLabelController")
                self.label_info = REPData[2]
                self.init_table(self.label_info)
                return
            else:
                self.label_info = REPData[2]
                self.init_table(self.label_info)
                QMessageBox.information(self, "提示", "删除标注信息失败")
        except Exception as e:
            print('delLabelListInfoRes', e)

    # 删除全部按钮，删除当前页全部标注
    def on_btnDelAll_clicked(self):
        try:
            if not self.label_info:
                QMessageBox.information(self.view, ' ', '当前页为空')
                return
            answer = QMessageBox.warning(
                self.view, '确认删除！', '您将进行删除操作！',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if answer == QMessageBox.Yes:
                self.client.delLabelByModelFile([self.model_id, self.check_id, self.file_id])
        except Exception as e:
            print('on_btnDelAll_clicked', e)

    def delLabelByModelFileRes(self, REPData):
        try:
            if REPData[0] == '1':
                QMessageBox.information(self, "提示", "删除全部标注信息成功")
                self.view.ui.tableWidget.clear()
                self.init_table([])
                return
            else:
                QMessageBox.information(self, "提示", "删除全部标注信息失败")
        except Exception as e:
            print('delLabelByModelFileRes', e)

    # 查询筛选当前页标注
    def on_btnSelect_clicked_classifier(self):
        try:
            self.classifier_key_word = self.view.ui.comboCond.currentText()
            self.classifier_key_value = self.view.ui.lineValue.text()
            self.search_init_info.clear()
            self.isSearch = False
            self.searchPage = 1
            if self.classifier_key_value == '':
                QMessageBox.information(self, '提示', '请输入要搜索的分类器信息', QMessageBox.Ok)
                return
            if self.classifier_key_word == '分类器名称':
                self.classifier_key_word = 'classifier_name'
            REQmsg = [self.classifier_key_word, self.classifier_key_value, self.searchPage, self.pageRows]
            self.client.inquiryScanClassifierInfo(REQmsg)
        except Exception as e:
            print('on_btnSelect_clicked_classifier', e)

    def inquiryScanClassifierInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.isSearch = True
                self.searchPageMax = REPData[3]
                QMessageBox.information(self, '提示', '查询信息成功', QMessageBox.Ok)
                self.search_init_info.clear()
                self.search_init_info = REPData[2]
                itemName = ['分类器名称', '标注文件数', '标注数量', '已评估', '未评估']
                self.view.initView(self.search_init_info, itemName)
                self.view.ui.label_3.setText("共" + str(self.searchPageMax) + "页")
                self.view.ui.label_2.setText(str(self.searchPage))
            else:
                self.view.ui.lineValue.clear()
                QMessageBox.information(self, '提示', '查询算法信息失败,请重试', QMessageBox.Ok)
        except Exception as e:
            print('inquiryScanClassifierInfoRes', e)

    # 重置，显示所有标注
    def on_btnRest_classifier_clicked(self):
        try:
            self.curPageIndex = 1
            self.isSearch = False
            self.searchPage = 1
            self.searchPageMax = 1
            self.client.getClearLabelInfo([self.curPageIndex, self.pageRows, True])
        except Exception as e:
            print('reset', e)

    # 点击显示未评估/已评估的标注
    def on_btnAssesse_clicked(self):
        try:
            if self.count % 2 == 0:
                self.client.getLabelInfoByAssess([self.model_id, self.check_id, self.file_id, 0])
            else:
                self.client.getLabelInfoByAssess([self.model_id, self.check_id, self.file_id, 1])
        except Exception as e:
            print('on_btnAssesse_clicked', e)

    def getLabelInfoByAssessRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.label_info = REPData[2]
                self.init_table(self.label_info)
                self.count += 1
                flag = REPData[3]
                if flag == 1:
                    self.view.ui.btnAssess.setText('已评估')
                else:
                    self.view.ui.btnAssess.setText('未评估')
                QMessageBox.information(self, '提示', '查询信息成功', QMessageBox.Ok)
            else:
                QMessageBox.information(self, '提示', '查询信息失败', QMessageBox.Ok)
        except Exception as e:
            print('getLabelInfoByAssessRes', e)


    def exit(self):
        try:
            self.client.getClearLabelInfoResSig.disconnect()
            self.client.inquiryScanClassifierInfoResSig.disconnect()
            self.client.scanClassifierInfoPagingResSig.disconnect()
            self.client.getScanInfoResSig.disconnect()
            self.client.getCurClearLabelInfoResSig.disconnect()
            self.client.getScanFileInfoResSig.disconnect()
            self.client. delLabelListInfoResSig.disconnect()
            self.client.delLabelByModelFileResSig.disconnect()
            self.client.getLabelInfoByAssessResSig.disconnect()
            self.client.getSearchScanFileInfoResSig.disconnect()
        except Exception as e:
            print('exit', e)

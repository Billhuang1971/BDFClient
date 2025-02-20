import datetime
import json
import math
import numpy as np
import time

import threading
import inspect
import ctypes

from PyQt5 import QtWidgets, QtCore
from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.Qt import *

from view.manualQuery import ManualView
from view.manualQuery import PrentryView
from view.manualQuery import sign_InfoView

from view.manual_form.combo_check_box2 import CheckableComboBox

class manualQueryController(QWidget):
    switchToEEG = pyqtSignal(list)
    def __init__(self, appUtil=None, client=None, page_number=None):
        super().__init__()
        self.appUtil = appUtil
        self.view = ManualView()
        self.client = client
        self.User = self.client.tUser
        if page_number==None:
            self.curPageIndex = 1
        else:
            self.curPageIndex=page_number
        self.pageRows = 12
        self.curPageMax = 1
        self.check_id = None
        self.measure_date = None
        self.file_name = None
        self.file_id = None
        self.page = ['file_name']
        msg = [self.client.tUser[0], self.curPageIndex, self.pageRows]
        self.client.mq_get_diags_Diagnosed(msg)
        self.view.page_control_signal.connect(self.mq_paging)
        self.client.mq_pagingResSig.connect(self.mq_pagingRes)
        self.client.mq_get_diags_DiagnosedResSig.connect(self.mq_get_diags_DiagnosedRes)
        # self.client.mq_get_type_infoResSig.connect(self.mq_get_type_infoRes)
        self.client.mq_get_fileNameByIdDateResSig.connect(self.mq_get_fileNameByIdDateRes)
        # self.client.mq_openEEGFileResSig.connect(self.mq_openEEGFileRes)
        # self.client.mq_load_dataDynamicalResSig.connect(self.mq_load_dataDynamicalRes)
        # self.client.mq_init_SampleListResSig.connect(self.mq_init_SampleListRes)
        # self.client.mq_get_diagResSig.connect(self.mq_get_diagRes)


    def mq_get_diags_DiagnosedRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "提取未诊断信息不成功", REPData[2], QMessageBox.Yes)
            return False
        self.diags_viewInfo = REPData[2]
        self.userNamesDict = {}
        self.paitentNamesDict = {}
        if REPData[3] is not None:
          for u in REPData[3]:
            self.userNamesDict.setdefault(u[0], u[1])
        if REPData[4] is not None:
          for p in REPData[4]:
            self.paitentNamesDict.setdefault(p[0], p[1])

        self.curPageIndex = REPData[5]
        self.curPageMax = REPData[6]

        self.view.show()
        self.view.init_table(self.diags_viewInfo, self.client.tUser, self.userNamesDict, self.paitentNamesDict,
                              self.on_clicked_manual_query, self.on_clicked_diag_query, self.curPageIndex, self.curPageMax)


    # 槽对象中的槽函数
    def exit(self):
        # self.stopRolling()
        self.client.mq_get_diags_DiagnosedResSig.disconnect()
        # self.client.mq_get_type_infoResSig.disconnect()
        self.client.mq_get_fileNameByIdDateResSig.disconnect()
        self.client.mq_pagingResSig.disconnect()
        # self.client.mq_openEEGFileResSig.disconnect()
        # self.client.mq_load_dataDynamicalResSig.disconnect()
        # self.client.mq_init_SampleListResSig.disconnect()
        # self.client.mq_get_diagResSig.disconnect()
        # self.client.mq_pagingResSig.disconnect()


    def mq_paging(self,page_to):
        if page_to[0] == "home":
            self.curPageIndex = 1
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "pre":
            if self.curPageIndex <= 1:
                return
            self.curPageIndex = self.curPageIndex - 1
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "next":
            self.curPageIndex = self.curPageIndex + 1
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "final":
            self.curPageIndex = self.curPageMax
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "confirm":
            pp = self.diagListView.ui.skipPage.text()
            if int(pp) > self.curPageMax or int(pp) <= 0:
                QMessageBox.information(self, "查询", f'页数：1 至 {self.curPageMax}', QMessageBox.Yes)
                self.view.ui.skipPage.setText(str(self.curPageMax))
                return False
            self.curPageIndex = int(pp)
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "query":
            self.curPageIndex = 1
            self.view.ui.curPage.setText(str(self.curPageIndex))
        pname = self.view.ui.comboBox.currentText()
        pvalue = self.view.ui.lineEdit.text()
        if pname == '测量日期':
            r, pvalue = self.chkdate(pvalue)
            if r == '0':
                return
        mdate1 = self.view.ui.lineEditDate1.text()
        r, mdate1 = self.chkdate(mdate1)
        if r == '0':
            return
        mdate2 = self.view.ui.lineEditDate2.text()
        r, mdate2 = self.chkdate(mdate2)
        if r == '0':
            return
        self.view.setDisabled(True)
        msg = [self.client.tUser[0], self.curPageIndex, self.pageRows, page_to[0], pname, pvalue, mdate1, mdate2]
        self.client.mq_paging(msg)

    def chkdate(self, date_str):
        try:
            if date_str is None or date_str == '':
                return '1', ''
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return '1', date_str
        except:
            QMessageBox.information(self, "输入数据校验", f"输入{date_str}不正确,日期格式,如2024-9-18", QMessageBox.Yes)
            return '0', date_str
    def mq_pagingRes(self, REPData):
        self.view.setEnabled(True)
        if REPData[0] == '0':
            QMessageBox.information(self, "查询", REPData[2], QMessageBox.Yes)
            return False
        self.diags_viewInfo = REPData[2]
        self.userNamesDict = {}
        self.paitentNamesDict = {}
        if REPData[3] is not None:
          for u in REPData[3]:
            self.userNamesDict.setdefault(u[0], u[1])
        if REPData[4] is not None:
          for p in REPData[4]:
            self.paitentNamesDict.setdefault(p[0], p[1])

        self.curPageIndex = REPData[5]
        self.curPageMax = REPData[6]

        # self.view.show()
        self.view.init_table(self.diags_viewInfo, self.client.tUser, self.userNamesDict, self.paitentNamesDict,
                                     self.on_clicked_manual_query, self.on_clicked_diag_query, self.curPageIndex,
                                     self.curPageMax)
    def on_btnNextFile_clicked(self):
      self.stopRolling()
      # self.view.ui.nextFileBtn.setDisabled(True)
      # self.view.ui.nextPatientBtn.setDisabled(True)
      # self.view.ui.btnSignInfo.setDisabled(True)
      self.view.hide()

      # self.file_id = None
      # self.measure_date = None
      # self.file_name = None
      # self.page = ['file_name']
      self.returnTo = 1
      msg = [self.check_id]
      self.client.mq_get_fileNameByIdDate(msg)


    def on_btnNextPatient_clicked(self):
      self.stopRolling()
      self.view.ui.nextFileBtn.setDisabled(True)
      self.view.ui.nextPatientBtn.setDisabled(True)
      self.view.ui.btnSignInfo.setDisabled(True)
      self.view.hide()
      #self.prentryView.hide()
      while self.mainLayout.count() > 1:
          witem = self.mainLayout.itemAt(self.mainLayout.count() - 1)
          witem.widget().hide()
          self.mainLayout.removeItem(witem)
      self.mainLayout.addWidget(self.diagListView)
      self.diagListView.show()
      self.returnTo = 0

    # 获取提取取诊断信息
    # 向客户端发送提取取诊断信息的请求
    def mq_get_diags_Diagnosed(self):
        self.check_id = None
        self.measure_date = None
        self.file_name = None
        self.file_id = None
        self.page = ['file_name']
        msg=[self.client.tUser[0],self.curPageIndex,self.pageRows]
        self.client.mq_get_diags_Diagnosed(msg)

    # 处理客户端传回的提取取诊断信息

    def on_clicked_manual_query(self, diags_viewInfo, patient_name):
        self.check_id = diags_viewInfo[-4]
        self.patient_id = diags_viewInfo[0]
        self.measure_date = diags_viewInfo[1]
        self.patient_name = patient_name
        self.uid = diags_viewInfo[2]

        self.file_name = None
        self.file_id = None
        self.page = ['file_name']

        msg = [self.check_id]
        self.client.mq_get_fileNameByIdDate(msg)
        self.returnTo = 0
        self.view.hide()

    def on_clicked_diag_query(self, diags_viewInfo, patient_name):

        msg = f"病人：{patient_name}, 测量时间:{diags_viewInfo[1]}, 诊断医生：{self.userNamesDict.get(diags_viewInfo[2])},\n诊断时间：{str(diags_viewInfo[4])[0:10]}\n"

        msg += f"alpha波活动: {diags_viewInfo[5]}\n"
        msg += f"慢波活动: {diags_viewInfo[6]}\n"
        msg += f"快波活动: {diags_viewInfo[7]}\n"
        msg += f"波幅特点: {diags_viewInfo[8]}\n"
        msg += f"睁闭眼: {diags_viewInfo[9]}\n"
        msg += f"过度换气: {diags_viewInfo[10]}\n"
        msg += f"睡眠: {diags_viewInfo[11]}\n"
        msg += f"异常脑波: {diags_viewInfo[12]}\n"
        msg += f"发作期: {diags_viewInfo[13]}\n"
        msg += f"诊断总结: {diags_viewInfo[14]}\n"

        QMessageBox.information(self, "诊断信息", msg, QMessageBox.Yes)


    def mq_get_fileNameByIdDateRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "选择脑电数据文件", REPData[2], QMessageBox.Yes)
            return False
        else:
            self.pre_info = REPData[1]
            col_num = 1

            self.prentryView = PrentryView()
            self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
            self.prentryView.setWindowTitle("标注诊断[选择脑电数据文件]")
            self.prentryView.setWindowModality(Qt.ApplicationModal)
            # self.prentryView.show()
            self.prentryView.ui.btnConfirm.setEnabled(False)
            # self.prentryView.ui.btnReturn.setEnabled(False)
            self.prentryView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.prentryView.ui.tableWidget.resizeRowsToContents()
            self.prentryView.ui.tableWidget.resizeColumnsToContents()
            self.prentryView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.prentryView.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)
            self.prentryView.ui.btnConfirm.clicked.connect(self.on_btnConfirm_clicked)
            self.prentryView.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)

            self.prentryView.ui.tableWidget.setColumnCount(col_num)
            itemName = ['脑电数据文件列表']
            row_num = len(self.pre_info)
            if row_num <= 0:
                itemName = ['脑电数据文件列表[无相关文件]']
            for i in range(col_num):
                header_item = QTableWidgetItem(itemName[i])
                font = header_item.font()
                font.setPointSize(10)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                self.prentryView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
            self.prentryView.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.prentryView.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            self.prentryView.ui.tableWidget.setRowCount(row_num)
            for r in range(row_num):
                fn='{:>03}.bdf'.format(self.pre_info[r][1])
                item = QTableWidgetItem(fn)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(10)
                item.setFont(font)
                self.prentryView.ui.tableWidget.setItem(r, 0, item)
            self.prentryView.ui.tableWidget.verticalHeader().setVisible(False)

        self.prentryView.show()

    # 响应prentryView单击表格事件，选择病人/测量日期/文件名
    def on_tableWidget_itemClicked(self):
        row = self.prentryView.ui.tableWidget.currentRow()
        strRow = str(row)
        # QMessageBox.information(self, "on_tableWidget_itemClicked", strRow, QMessageBox.Yes)
        if row < 0:
            return
        self.file_id = self.pre_info[row][1]
        self.file_name = '{:>03}.bdf'.format(self.file_id)
        self.prentryView.ui.btnConfirm.setEnabled(True)

    # prentryView选择文件后，点击确认按钮载入数据显示图像
    def on_btnConfirm_clicked(self):
        self.prentryView.close()
        self.switchToEEG.emit([self.file_id, self.file_name, self.check_id, self.patient_id, self.measure_date, ['manualQueryController', self.curPageIndex], "sample_info", self.client.tUser[0], False, False, None])


    # prentryView返回按钮
    def on_btnReturn_clicked(self):
        self.prentryView.close()
        # if self.returnTo == 1:
        self.view.show()
        # self.diagListView.hide()
        # else:
        #   # self.diagListView.show()
        #   self.view.hide()
        return
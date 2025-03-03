import math

from view.createCons import createConsView, PrentryView
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import sys, re, shutil
import numpy as np
from functools import partial
from datetime import date


class createConsController(QWidget):
    is_reload_controller = QtCore.pyqtSignal(str)

    def __init__(self, client, cAppUtil):
        try:
            super().__init__()
            self.client = client
            self.cAppUtil = cAppUtil
            self.view = createConsView()

            # 存放病人ID的列表
            self.patientId_list = []
            # 存放医生信息的列表
            self.doctorInfo = []
            self.doctorSelect = []

            # 存放所有会诊数据的列表
            self.allConsInfo = []

            # 存放历史会诊记录
            self.historyConsData = []
            # 完成脑电检查信息
            self.cpltCheckInfo = []
            # 是否正在编辑模式，默认否
            self.isEdit = False
            # 是否正在添加模式，默认否
            # self.isAdd = False
            # 被选择的行
            self.select_row = None
            # 病人信息表的列数
            self.col_num = 3

            # 一页显示多少行
            self.pageRows = 12
            self.curPageIndex = 1
            self.totalPage = 1

            self.pageDocRows = 9
            self.curDocPageIndex = 1
            self.totalDocPage = 1

            self.isSearch = False
            self.isSearch_doctor = False

            self.view.initView(self.on_clicked_add, self.resetData, self.createCons, self.set_selectRow,
                               self.on_clicked_diag_select, lambda: self.inqConsInfo(pageIndex=1))
            self.view.initTable(self.allConsInfo)
            self.view.initDoctorTable(self.doctorSelect)
            self.client.getAllConsInfo([1, self.pageRows, 'home'])

            self.client.getDoctorInfoResSig.connect(self.getDoctorInfoRes)
            self.client.getCpltCheckInfoResSig.connect(self.getCpltCheckInfoRes)
            self.client.inqConsInfoSig.connect(self.inqConsInfoRes)
            self.client.createConsResSig.connect(self.createConsRes)
            self.client.getAllConsInfoSig.connect(self.getAllConsInfoRes)
            self.client.getSearchDoctorInfoSig.connect(self.getDocInfoRes)
            self.view.ui.resetSearch.clicked.connect(self.reset)
            self.view.create_cons_page_control_signal.connect(self.rg_paging)
            # self.client.getCpltCheckInfoResSig.connect(self.inqConsInfoSig)
            self.view.ui.tableWidget2.setContextMenuPolicy(Qt.CustomContextMenu)
            self.view.ui.tableWidget2.customContextMenuRequested.connect(self.menuSelect)
        except Exception as e:
            print('createConsController', e)

    def initPretry(self, width=700):
        self.prentryView = PrentryView()
        self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
        self.prentryView.setWindowTitle("创建会诊")
        self.prentryView.setWindowModality(Qt.ApplicationModal)
        self.prentryView.resize(width, 600)
        self.prentryView.show()
        self.prentryView.ui.btnConfirm.setEnabled(False)
        self.prentryView.ui.btnReturn.setEnabled(False)
        self.prentryView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.prentryView.ui.tableWidget.resizeRowsToContents()
        self.prentryView.ui.tableWidget.resizeColumnsToContents()
        self.prentryView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.prentryView.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)
        self.prentryView.ui.btnConfirm.clicked.connect(self.on_btnConfirm_clicked)
        self.prentryView.ui.searchDoc.clicked.connect(self.getDocSearchInfo)
        self.prentryView.ui.resetSearch.clicked.connect(self.resetDocSearch)
        self.prentryView.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)
        self.prentryView.prentry_page_control_signal.connect(self.rg_paging2)


    # 设置表格右键可呼出菜单
    def menuSelect(self, pos):
        row_num = -1
        for i in self.view.ui.tableWidget2.selectionModel().selection().indexes():
            row_num = i.row()
        if row_num == -1:
            return
        menu = QMenu()
        item1 = menu.addAction(u"删除医生")
        action = menu.exec_(self.view.ui.tableWidget2.mapToGlobal(pos))
        if action == item1:
            self.delDoc(row_num)

    def delDoc(self, row_num):
        print(f'row_num: {row_num}, doctorSelect: {self.doctorSelect}')
        del self.doctorSelect[row_num]
        self.view.initDoctorTable(self.doctorSelect)


    def resetDocSearch(self):#选择医生的重置
        print(f'resetDocSearch')
        self.isSearch_doctor = False
        self.curDocPageIndex=1
        self.prentryView.ui.curPage.setText(str(self.curDocPageIndex))
        self.client.getDoctorInfo([self.curDocPageIndex, self.pageDocRows, 'home'])


    def inqConsInfo(self, pageIndex):
        self.curPageIndex = pageIndex
        key_word = self.view.ui.comboBox.currentText()
        key_value = self.view.ui.lineEdit.text()

        date1 = self.view.ui.lineEditDate1.text()
        date2 = self.view.ui.lineEditDate2.text()

        if (date1 == '' and date2 !='') or (date1 != '' and date2 == ''):
            QMessageBox.information(self, '提示', '请输入起始日期和结束日期', QMessageBox.Yes)
            return

        if date1 != '' or date2 != '':
            try:
                dt1 = datetime.strptime(date1, '%Y-%m-%d')
                dt2 = datetime.strptime(date2, '%Y-%m-%d')

                if dt2 < dt1:
                    QMessageBox.information(self, '提示', '日期范围不对，不能早于起始日期', QMessageBox.Yes)
                    return
            except ValueError:
                QMessageBox.information(self, '提示', '日期格式错误', QMessageBox.Yes)
                return

        if key_value == '' and (date1 == '' and date2 ==''):
            QMessageBox.information(self, '提示', '请输入要搜索的信息', QMessageBox.Yes)
            return
        if key_word == '检查单号':
            key_word = 'check_number'
        elif key_word == '病人名称':
            key_word = 'name'

        REQmsg = [key_word, key_value, [date1, date2], pageIndex, self.pageRows]
        print(f'inqConsInfo: {REQmsg}')
        self.client.inqConsInfo(REQmsg)

    def getDocSearchInfo(self):
        self.curDocPageIndex = 1
        key_word = self.prentryView.ui.comboBox.currentText()
        key_value = self.prentryView.ui.lineEdit.text()

        if key_value == '' :
            QMessageBox.information(self, '提示', '请输入要搜索的信息', QMessageBox.Yes)
            return
        if key_word == '医生账号':
            key_word = 'account'
        elif key_word == '会诊医生':
            key_word = 'name'
        REQmsg = [self.curDocPageIndex, self.pageDocRows, 'home', key_word, key_value]
        self.prentryView.ui.curPage.setText(str(self.curDocPageIndex))
        print(f'inqConsInfo: {REQmsg}')
        self.client.getSearchDoctorInfo(REQmsg)

    def getDocInfoRes(self, REPData): #搜索的返回
        try:
            print(f'getDocInfoRes: {REPData}')
            self.isSearch_doctor = True
            self.getDoctorInfoRes(REPData)
        except Exception as e:
            print('getDocInfoRes', e)


    def inqConsInfoRes(self, REPData):
        try:
            self.isSearch=True
            print(f'inqConsInfoRes: {REPData}')
            self.curPageIndex = REPData[2]
            self.allConsInfo = REPData[1]
            self.totalPage = math.ceil(REPData[0] / self.pageRows)
            self.view.ui.totalPage.setText(f'共{str(self.totalPage)}页')
            self.view.ui.curPage.setText(str(self.curPageIndex))
            self.view.initTable(self.allConsInfo)
        except Exception as e:
            print('inqConsInfoRes', e)

    # 搜索重置
    def reset(self):
        print(f'reset')
        self.view.ui.lineEdit.clear()
        self.view.ui.lineEditDate1.clear()
        self.view.ui.lineEditDate2.clear()
        self.isSearch=False
        self.curPageIndex = 1
        self.view.ui.curPage.setText(str(self.curPageIndex))
        msg = [self.curPageIndex, self.pageRows, 'home']
        self.client.getAllConsInfo(msg)

    def rg_paging(self, page_to):
        print(page_to)
        if page_to[0] == "home":
            self.curPageIndex = 1
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "pre":
            if self.curPageIndex <= 1:
                return
            self.curPageIndex = self.curPageIndex - 1
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "next":
            if self.curPageIndex + 1 > self.totalPage:
                QMessageBox.information(self, "查询", f'最大页数：{self.totalPage}', QMessageBox.Yes)
                return False
            self.curPageIndex = self.curPageIndex + 1
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "final":
            self.curPageIndex = self.totalPage
            self.view.ui.curPage.setText(str(self.curPageIndex))
        elif page_to[0] == "confirm":
            pp = self.view.ui.skipPage.text()
            if pp != '':
                if int(pp) > self.totalPage:
                    QMessageBox.information(self, "查询", f'最大页数：{self.totalPage}', QMessageBox.Yes)
                    return False
                self.curPageIndex = int(pp)
                self.view.ui.curPage.setText(str(self.curPageIndex))
            else:
                QMessageBox.information(self, '提示', '请输入要跳转的页数', QMessageBox.Yes)
        if self.isSearch:
            key_word = self.view.ui.comboBox.currentText()
            key_value = self.view.ui.lineEdit.text()
            date1 = self.view.ui.lineEditDate1.text()
            date2 = self.view.ui.lineEditDate2.text()
            if key_word == '检查单号':
                key_word = 'check_number'
            elif key_word == '病人名称':
                key_word = 'name'
            msg = [key_word, key_value, [date1, date2], self.curPageIndex, self.pageRows]
            self.client.inqConsInfo(msg)
        else:
            msg = [self.curPageIndex, self.pageRows, page_to[0]]
            self.client.getAllConsInfo(msg)

    def rg_paging2(self, page_to):
        print(page_to)
        if page_to[0] == "home":
            self.curDocPageIndex = 1
            self.prentryView.ui.curPage.setText(str(self.curDocPageIndex))
        elif page_to[0] == "pre":
            if self.curDocPageIndex <= 1:
                return
            self.curDocPageIndex = self.curDocPageIndex - 1
            self.prentryView.ui.curPage.setText(str(self.curDocPageIndex))
        elif page_to[0] == "next":
            if self.curDocPageIndex + 1 > self.totalDocPage:
                QMessageBox.information(self, "查询", f'最大页数：{self.totalDocPage}', QMessageBox.Yes)
                return False
            self.curDocPageIndex = self.curDocPageIndex + 1
            self.prentryView.ui.curPage.setText(str(self.curDocPageIndex))
        elif page_to[0] == "final":
            self.curDocPageIndex = self.totalDocPage
            self.prentryView.ui.curPage.setText(str(self.curDocPageIndex))
        elif page_to[0] == "confirm":
            pp = self.prentryView.ui.skipPage.text()
            if pp != '':
                if int(pp) > self.totalDocPage:
                    QMessageBox.information(self, "查询", f'最大页数：{self.totalDocPage}', QMessageBox.Yes)
                    return False
                self.curDocPageIndex = int(pp)
                self.prentryView.ui.curPage.setText(str(self.curDocPageIndex))
            else:
                QMessageBox.information(self, '提示', '请输入要跳转的页数', QMessageBox.Yes)
        if self.isSearch_doctor:
            key_word = self.prentryView.ui.comboBox.currentText()
            key_value = self.prentryView.ui.lineEdit.text()
            if key_word == '医生账号':
                key_word = 'account'
            elif key_word == '会诊医生':
                key_word = 'name'
            msg = [self.curDocPageIndex, self.pageDocRows, 'home', key_word, key_value]
            self.client.getSearchDoctorInfo(msg)
        else:
            msg = [self.curDocPageIndex, self.pageDocRows, page_to[0]]
            self.client.getDoctorInfo(msg)


    def getAllConsInfoRes(self, data):
        print(f'getAllConsInfoRes data: {data}')
        self.allConsInfo = data[1]
        self.totalPage = math.ceil(data[0] / self.pageRows)
        self.view.ui.totalPage.setText(f'共{str(self.totalPage)}页')
        self.view.initTable(self.allConsInfo)


    def on_clicked_add(self):
        self.curDocPageIndex = 1
        self.initPretry()
        self.client.getDoctorInfo([1, self.pageDocRows, 'home'])

    def on_clicked_diag_select(self):
        try:
            # self.initPretry('diag', width=1000)
            # self.client.getCpltCheckInfo()
            row = self.select_row
            self.checkId = int(self.allConsInfo[row][9])
            text = f'病人名称：{self.allConsInfo[row][1]}\n' \
                   f'检查单号：{self.allConsInfo[row][0]}\n' \
                   f'测量日期：{self.allConsInfo[row][2].strftime("%Y-%m-%d %H:%M:%S")}\n' \
                   f'开单医生：{self.allConsInfo[row][3]}\n' \
                   f'上传医生：{self.allConsInfo[row][4]}\n' \
                   f'描述：{self.allConsInfo[row][8]}'
            self.view.ui.label_2.setText(text)
        except Exception as e:
            print('on_clicked_history_select', e)

    def getDoctorInfoRes(self, doctorInfo):
        print(f'getDoctorInfoRes: {doctorInfo}')
        self.doctorInfo = doctorInfo[1]

        self.totalDocPage = math.ceil(doctorInfo[0] / self.pageDocRows)
        self.prentryView.ui.totalPage.setText(f'共{str(self.totalDocPage)}页')

        col_num = 2
        columnName = ['医生账号', '会诊医生']
        self.prentryView.ui.tableWidget.setColumnCount(col_num)
        for i in range(col_num):
            header_item = QTableWidgetItem(columnName[i])
            font = header_item.font()
            font.setPointSize(15)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            self.prentryView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
        self.prentryView.ui.tableWidget.horizontalHeader().setHighlightSections(False)
        self.prentryView.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        row_num = len(self.doctorInfo)
        self.prentryView.ui.tableWidget.setRowCount(row_num)
        tempIndex = [4, 0]
        for r in range(row_num):
            for i in range(col_num):
                self.prentryView.ui.tableWidget.setRowHeight(r, 40)
                text = f'{self.doctorInfo[r][tempIndex[i]]}'
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(11)
                item.setFont(font)
                self.prentryView.ui.tableWidget.setItem(r, i, item)
        self.prentryView.ui.tableWidget.verticalHeader().setVisible(False)

    def on_btnConfirm_clicked(self):
        try:
            row = self.prentryView.ui.tableWidget.currentRow()
            print(f'on_btnConfirm_clicked Row: {row}')
            if self.doctorInfo[row] not in self.doctorSelect:
                self.doctorSelect.append(self.doctorInfo[row])
                print(f'self.doctorSelect: {self.doctorSelect}')
                self.view.initDoctorTable(self.doctorSelect)
                self.prentryView.close()
            else:
                QMessageBox.information(self, '提示', '医生已在列表中')
        except Exception as e:
            print('on_btnConfirm_clicked', e)





    def on_tableWidget_itemClicked(self):
        self.prentryView.ui.btnConfirm.setEnabled(True)

    def on_btnReturn_clicked(self):
        self.prentryView.close()

    # 病人删除
    def resetData(self):
        try:
            print(f'resetData')
            self.doctorSelect.clear()
            self.view.initDoctorTable(self.doctorSelect)
            self.view.ui.textEdit.clear()
            self.view.ui.label_2.setText('请选择会诊数据')
        except Exception as e:
            print('resetData', e)

    def getCpltCheckInfoRes(self, cpltCheckInfo):
        try:
            print(f'cpltCheckInfo； {cpltCheckInfo}')
            self.cpltCheckInfo = cpltCheckInfo
            col_num = 5
            columnName = ['病人名称', '检查单号', '测量日期', '开单医生', '上传医生']
            self.prentryView.ui.tableWidget.setColumnCount(col_num)
            for i in range(col_num):
                header_item = QTableWidgetItem(columnName[i])
                font = header_item.font()
                font.setPointSize(10)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                self.prentryView.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
            self.prentryView.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.prentryView.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            row_num = len(self.cpltCheckInfo)
            self.prentryView.ui.tableWidget.setRowCount(row_num)
            index_list = [8, 1, 5, 9, 10]
            for r in range(row_num):
                for i in range(col_num):
                    self.prentryView.ui.tableWidget.setRowHeight(r, 30)
                    if i == 2:
                        item = QTableWidgetItem(self.cpltCheckInfo[r][index_list[i]].strftime("%Y-%m-%d"))
                    else:
                        item = QTableWidgetItem(self.cpltCheckInfo[r][index_list[i]])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(11)
                    item.setFont(font)
                    self.prentryView.ui.tableWidget.setItem(r, i, item)
            self.prentryView.ui.tableWidget.verticalHeader().setVisible(False)
        except Exception as e:
            print('getCpltCheckInfoRes', e)

    def createCons(self):
        try:
            if len(self.doctorSelect) == 0:
                QMessageBox.information(self, '提示', '会诊医生数量为0')
                return

            if self.view.ui.label_2.text() == '请选择会诊数据':
                QMessageBox.information(self, '提示', '没有选择会诊数据')
                return

            message = self.view.ui.textEdit.toPlainText()
            if message == '':
                QMessageBox.information(self, '提示', '会诊信息为空')
                return

            # 获取当前时间
            current_datetime = QDateTime.currentDateTime()
            print(f'current_datetime: {current_datetime}')

            self.client.createCons(
                [self.checkId, message, current_datetime.toString("yyyy-MM-dd hh:mm:ss"), self.doctorSelect])
            self.view.ui.verifyButton.setEnabled(False)

            # 清空数据
            self.doctorSelect.clear()
            self.view.initDoctorTable(self.doctorSelect)
            self.view.ui.textEdit.clear()
            self.view.ui.label_2.setText("请选择会诊数据")
        except Exception as e:
            print('createCons', e)

    def createConsRes(self, msg):
        print(f'createConsRes: {msg}')
        self.view.ui.verifyButton.setEnabled(True)
        if msg[0] == '1':
            self.client.getAllConsInfo([1, self.pageRows, 'home'])
        QMessageBox.information(self, '提示', msg[1])


    def set_selectRow(self, item):
        self.select_row = item.row()

    def exit(self):
        try:
            self.client.getDoctorInfoResSig.disconnect()
            self.client.getCpltCheckInfoResSig.disconnect()
            # self.client.getHistoryConsResSig.disconnect()
            self.client.createConsResSig.disconnect()
            self.client.getAllConsInfoSig.disconnect()
            self.view.create_cons_page_control_signal.disconnect()

        except Exception as e:
            print('exit', e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = createConsController()
    controller.client.getPatientInfo()
    sys.exit(app.exec_())

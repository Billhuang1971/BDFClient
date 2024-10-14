from view.patientManager import patientManagerView, TableWidget
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import sys, re, shutil
import numpy as np


class patientManagerController(QWidget):
    is_reload_controller = QtCore.pyqtSignal(str)

    def __init__(self, client, cAppUtil):
        try:
            super().__init__()
            self.client = client
            self.cAppUtil = cAppUtil
            self.view = patientManagerView()

            # 存放病人ID的列表
            self.patientId_list = []
            self.searchID = []
            # 存放病人信息的列表
            self.patientInfo = []
            self.searchInfo = []

            # 是否正在编辑模式，默认否
            self.isEdit = False
            self.isAdd = False
            # 是否正在添加模式，默认否
            # self.isAdd = False
            # 被选择的行
            self.select_row = None
            # 病人信息表的列数
            self.col_num = 7
            self.tableWidget = None
            self.isSearch = False
            self.curPageIndex = 1
            self.pageRows = 12
            self.curPageMax = 1
            self.temptPageMax=1
            self.client.getPatientInfoResSig.connect(self.getPatientInfoRes)
            self.client.addPatientInfoResSig.connect(self.addPatientInfoRes)
            self.client.delPatientInfoResSig.connect(self.delPatientInfoRes)
            self.client.updatePatientInfoResSig.connect(self.updatePatientInfoRes)
            self.client.inqPatientInfoResSig.connect(self.inqPatientInfoRes)
            self.client.patientPagingResSig.connect(self.patientPagingRes)
            self.view.ui.pushButton.clicked.connect(lambda: self.inqPatientInfo(pageIndex=1))
            self.view.ui.pushButton_2.clicked.connect(self.reset)
            self.client.getPatientInfo([self.curPageIndex, self.pageRows])
        except Exception as e:
            print('patientInfo', e)


    def inqPatientInfo(self, pageIndex):
        if self.isEdit:
            QMessageBox.information(self, '提示', '请先完成编辑')
            return
        if self.isAdd:
            QMessageBox.information(self, '提示', '请先完成添加')
            return
        self.curPageIndex = pageIndex
        key_word = self.view.ui.comboBox.currentText()
        key_value = self.view.ui.lineEdit.text()
        self.searchInfo.clear()
        self.searchID.clear()
        # print(self.patientId_list)
        if key_value == '':
            QMessageBox.information(self, '提示', '请输入要搜索的病人信息', QMessageBox.Yes)
            return
        if key_word == '姓名':
            key_word = 'name'
        elif key_word == '医保卡号':
            key_word = 'card'
        elif key_word == '电话号码':
            key_word = 'tel'
        REQmsg = [key_word, key_value, pageIndex, self.pageRows]
        print(f'inqPatientInfo: {REQmsg}')
        self.client.inqPatientInfo(REQmsg)

        # 搜索重置
    def reset(self):
        if self.isEdit:
            QMessageBox.information(self, '提示', '请先完成编辑')
            return
        if self.isAdd:
            QMessageBox.information(self, '提示', '请先完成添加')
            return
        self.isSearch = False
        self.searchInfo.clear()
        self.searchID.clear()
        self.view.ui.lineEdit.clear()
        # self.tableWidget.init_table(self.patientInfo)
        self.curPageIndex = 1
        self.curPageMax=self.temptPageMax
        self.client.patientPaging([self.curPageIndex, self.pageRows, 'home'])

    def inqPatientInfoRes(self, REPData):
        try:
            self.isSearch = True
            if REPData[0] == '1':
                patientInfo_m = REPData[2][1]
                self.curPageMax=REPData[2][0]
                print(f'inqPatientInfoRes: {patientInfo_m}')
                for i in patientInfo_m:
                    tempList = list(i)
                    # self.searchInfo[tempList[0]] = tempList[1:]
                    self.searchInfo.append(tempList[1:])
                    self.searchID.append(tempList[0])
                # print(f'self.searchInfo.values(): {list(self.searchInfo.values())}')
                # self.tableWidget.init_table(self.searchInfo)
                self.clear_layout(self.view.ui.verticalLayout_2)
                self.tableWidget = TableWidget(self.searchInfo, self.curPageIndex)
                self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
                self.tableWidget.setPageController(REPData[2][0])  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.table.itemClicked.connect(self.set_selectRow)
            else:
                QMessageBox.information(self, '提示', '获取病人信息失败', QMessageBox.Ok)
        except Exception as e:
            print('inqPatientInfoRes', e)


    def getPatientInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.curPageMax = REPData[3]
                self.temptPageMax=self.curPageMax
                patientInfo_m = REPData[2]
                for i in patientInfo_m:
                    tempList = list(i)[1:]
                    self.patientId_list.append(i[0])
                    self.patientInfo.append(tempList)
                self.view.initView(self.on_clicked_patient_add, self.on_clicked_patient_del,
                                   self.on_clicked_patient_edit, self.client.tUser)
                self.tableWidget = TableWidget(self.patientInfo, self.curPageIndex)
                self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.table.itemClicked.connect(self.set_selectRow)
                self.view.ui.verticalLayout.setStretch(0, 1)
                self.view.ui.verticalLayout.setStretch(1, 9)
            elif REPData[0] == '2':
                QMessageBox.information(self, '提示', '无病人信息', QMessageBox.Ok)
                self.view.initView(self.on_clicked_patient_add, self.on_clicked_patient_del,
                                   self.on_clicked_patient_edit, self.client.tUser)
                self.tableWidget = TableWidget(self.patientInfo, self.curPageIndex)
                self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.table.itemClicked.connect(self.set_selectRow)
                self.view.ui.verticalLayout.setStretch(0, 1)
                self.view.ui.verticalLayout.setStretch(1, 9)
            else:
                QMessageBox.information(self, '提示', '获取病人信息失败', QMessageBox.Ok)
        except Exception as e:
            print('getPatientInfoRes', e)

    def page_controller(self, signal):
        if "home" == signal[0]:
            if self.curPageIndex == 1:
                QMessageBox.information(self, "提示", "已经是首页了", QMessageBox.Yes)
                return
            self.curPageIndex = 1
            self.tableWidget.curPage.setText(str(self.curPageIndex))
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            if self.curPageIndex <= 1:
                return
            self.curPageIndex = self.curPageIndex - 1
            self.tableWidget.curPage.setText(str(self.curPageIndex))
        elif "next" == signal[0]:
            if self.curPageMax == int(signal[1]):
                QMessageBox.information(self, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.curPageIndex = self.curPageIndex + 1
            self.tableWidget.curPage.setText(str(self.curPageIndex))
        elif "final" == signal[0]:
            if self.curPageIndex == self.curPageMax:
                QMessageBox.information(self, "提示", "已经是尾页了", QMessageBox.Yes)
                return
            self.curPageIndex = self.curPageMax
            self.tableWidget.curPage.setText(str(self.curPageMax))
        elif "confirm" == signal[0]:
            if signal[1]=='':
                QMessageBox.information(self, "提示", "请输入页码进行跳转", QMessageBox.Yes)
                return
            if self.curPageIndex == int(signal[1]):
                QMessageBox.information(self, "提示", "当前已显示该页面", QMessageBox.Yes)
                return
            if self.curPageMax < int(signal[1]) or int(signal[1]) < 0:
                QMessageBox.information(self, "提示", "跳转页码超出范围", QMessageBox.Yes)
                return
            self.curPageIndex = int(signal[1])
            self.tableWidget.curPage.setText(signal[1])
        msg = [self.curPageIndex, self.pageRows, signal[0]]
        if self.view.ui.lineEdit.text() != '':
            self.inqPatientInfo(pageIndex=self.curPageIndex)
        else:
            self.client.patientPaging(msg)

    def patientPagingRes(self, REPData):
        try:
            patientInfo_m = REPData[2]
            self.patientId_list = []
            self.patientInfo = []
            for i in patientInfo_m:
                tempList = list(i)[1:]
                self.patientId_list.append(i[0])
                self.patientInfo.append(tempList)
            self.clear_layout(self.view.ui.verticalLayout_2)
            self.tableWidget = TableWidget(self.patientInfo, self.curPageIndex)
            self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
            self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
            self.tableWidget.control_signal.connect(self.page_controller)
            self.tableWidget.table.itemClicked.connect(self.set_selectRow)
        except Exception as e:
            print('userPagingRes', e)

    def on_clicked_patient_add(self):
        try:
            if self.isEdit:
                QMessageBox.information(self, '提示', '请先完成编辑')
                return
            if self.isAdd:
                QMessageBox.information(self, '提示', '请先完成添加')
                return
            self.isAdd = True
            row_num = self.tableWidget.table.rowCount()
            # print('test')
            self.tableWidget.table.setRowCount(row_num + 1)
            self.tableWidget.table.setRowHeight(row_num, 55)
            # 为新一行添加文本item
            for i in range(0, self.col_num):
                textItem = QTableWidgetItem()
                # 设置文本对齐方式,水平垂直方向
                textItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                # 设置字体格式
                textItem.setFont(QFont('', 12))
                self.tableWidget.table.setItem(row_num, i, textItem)
            self.edit_widget(row_num)
            self.itemIsEditable(row_num)
            self.confirmBtn.clicked.connect(lambda: self.editConfirm(row_num))
            self.cancelBtn.clicked.connect(lambda: self.editCancel(row_num))
            # QMessageBox.information(self, "提示", '请先完成添加', QMessageBox.Yes)
        except Exception as e:
            print('on_clicked_patient_add', e)

    def addPatientInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.patientInfo.clear()
                self.patientId_list.clear()
                self.curPageMax = REPData[4]
                patientInfo_m = REPData[3]
                for i in patientInfo_m:
                    tempList = list(i)[1:]
                    self.patientId_list.append(i[0])
                    self.patientInfo.append(tempList)
                self.clear_layout(self.view.ui.verticalLayout_2)
                self.tableWidget = TableWidget(self.patientInfo, self.curPageIndex)
                self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.table.itemClicked.connect(self.set_selectRow)
                QMessageBox.information(self, '提示', '添加病人成功, 请翻转到尾页查看', QMessageBox.Ok)
            else:
                QMessageBox.information(self, '提示', '添加病人失败', QMessageBox.Ok)
                self.clear_layout(self.view.ui.verticalLayout_2)
                self.tableWidget = TableWidget(self.patientInfo, self.curPageIndex)
                self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.table.itemClicked.connect(self.set_selectRow)
            self.view.ui.lineEdit.clear()
            self.isAdd = False
        except Exception as e:
            print('addPatientInfoRes', e)


    # 设置表格item状态
    def itemIsEditable(self, row=-1):
        try:
            if row == -1:
                for i in range(0, self.tableWidget.table.rowCount()):
                    for j in range(0, self.col_num):
                        # 设置第i行第j+1列的单元格为可选择且启用状态
                        self.tableWidget.table.item(i, j).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            else:
                for i in range(0, self.tableWidget.table.rowCount()):
                    for j in range(0, self.col_num):
                        if i == row:
                            # 设置第row行第j+1列的单元格为可编辑且启用状态
                            self.tableWidget.table.item(i, j).setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
                        else:
                            # 设置第i行第j+1列的单元格不启用
                            self.tableWidget.table.item(i, j).setFlags(Qt.ItemIsEditable)
        except Exception as e:
            print('itemIsEditable', e)

    # 确定编辑
    def editConfirm(self, row):
        try:
            # 当前编辑的病人信息
            patient_info = []
            row_num = row
            birth = self.cWidget.dateTime().toString("yyyy-MM-dd")
            sex = self.check_box.currentText()

            for j in range(0, self.col_num):
                if j == self.col_num - 6:
                    patient_info.append(birth)
                elif j == self.col_num - 5:
                    patient_info.append(sex)
                else:
                    patient_info.append(self.tableWidget.table.item(row_num, j).text())
                    # print(j)
            print(patient_info)
            if patient_info[0] == '':
                QMessageBox.information(self, "提示", '病人姓名不完善', QMessageBox.Yes)
            else:
                # print(patient_info)
                self.clear(row)
                if self.isEdit:
                    self.isEdit = False
                    if self.isSearch:
                        self.client.updatePatientInfo(REQmsg=[patient_info, self.searchID[row], row])
                    else:
                        self.client.updatePatientInfo(REQmsg=[patient_info, self.patientId_list[row], row])
                else:
                    patient_info.append(self.curPageIndex)
                    self.client.addPatientInfo(REQmsg=patient_info)
        except Exception as e:
            print('editConfirm', e)

    # 取消编辑
    def editCancel(self, row):
        try:
            if not self.isEdit:
                reply = QMessageBox.information(self, "提示", '是否取消添加', QMessageBox.Yes | QMessageBox.No)
                if reply == 16384:
                    self.isAdd = False
                    self.tableWidget.table.setRowCount(self.tableWidget.table.rowCount() - 1)
                    self.clear(row)
                    self.itemIsEditable()
            elif self.isEdit:
                # print(self.isEdit)
                reply = QMessageBox.information(self, "提示", '是否取消修改', QMessageBox.Yes | QMessageBox.No)
                if reply == 16384:
                    self.isEdit = False
                    self.clear(row)
                    self.itemIsEditable()
                    # for i in range(0, self.col_num):
                    #     self.view.tableWidget.item(row, i + 1).setText(self.patient_info[row][i])
        except Exception as e:
            print('editCancel', e)

    def edit_widget(self, row, default_sex=None, default_date=None):
        # print(row)
        # 设置日期控件
        self.cWidget = QDateEdit()
        # 设置是否启用日历弹出显示模式
        self.cWidget.setCalendarPopup(True)
        if default_date is not None:
            self.cWidget.setDate(default_date)
        # 在给定行和列的单元格中显示给定小部件
        self.tableWidget.table.setCellWidget(row, self.col_num - 6, self.cWidget)

        # 添加性别选择
        self.check_box = QComboBox()
        self.check_box.addItem('男')
        self.check_box.addItem('女')
        if default_sex is not None:
            self.check_box.setCurrentText(default_sex)
        lineEdit = QLineEdit()
        lineEdit.setReadOnly(True)  # 设置只读
        lineEdit.setAlignment(Qt.AlignCenter)  # 设置文字居中
        self.check_box.setLineEdit(lineEdit)
        self.tableWidget.table.setCellWidget(row, self.col_num - 5, self.check_box)

        # 为新一行添加特定的操作按钮
        widget = QWidget()
        layout = QHBoxLayout()
        # if self.isAdd:
        #     self.confirmBtn = QPushButton('确认添加')
        #     self.cancelBtn = QPushButton('取消添加')
        if self.isEdit:
            self.confirmBtn = QPushButton('确认修改')
            self.cancelBtn = QPushButton('取消修改')
        else:
            self.confirmBtn = QPushButton('确认添加')
            self.cancelBtn = QPushButton('取消添加')
        layout.addWidget(self.confirmBtn)
        layout.addWidget(self.cancelBtn)
        layout.setStretch(0, 1)
        layout.setStretch(1, 1)
        self.cancelBtn.setStyleSheet('''width:80px;font : 18px''')
        self.confirmBtn.setStyleSheet('''width:80px;font : 18px''')
        widget.setLayout(layout)
        self.view.ui.horizontalLayout.addWidget(widget)

    def clear(self, row):
        # 清理日期控件
        self.tableWidget.table.removeCellWidget(row, self.col_num - 6)
        # 清理性别选择控件
        self.tableWidget.table.removeCellWidget(row, self.col_num - 5)
        # 清理确认和取消的按钮布局
        item_list_length = self.view.ui.horizontalLayout.count()
        item = self.view.ui.horizontalLayout.itemAt(item_list_length - 1)
        self.view.ui.horizontalLayout.removeItem(item)
        if item.widget():
            item.widget().deleteLater()

    # 病人删除
    def on_clicked_patient_del(self):
        try:
            if self.isEdit:
                QMessageBox.information(self, '提示', '请先完成编辑')
                return
            if self.isAdd:
                QMessageBox.information(self, '提示', '请先完成添加')
                return
            if self.select_row is None:
                QMessageBox.information(self, '提示', '请选择要删除的病人信息')
                return
            reply = QMessageBox.information(self, '提示', '是否删除选中的病人', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                if self.isSearch:
                    self.isSearch = False
                    self.view.ui.lineEdit.clear()
                    self.client.delPatientInfo(
                        REQmsg=[self.searchID[self.select_row], self.select_row, self.curPageIndex])
                    self.searchInfo.clear()
                    self.searchID.clear()
                else:
                    self.client.delPatientInfo(
                        REQmsg=[self.patientId_list[self.select_row], self.select_row, self.curPageIndex])
        except Exception as e:
            print('on_clicked_patient_del', e)

    def delPatientInfoRes(self, REPData):
        try:
            if REPData[0] == '1':
                self.curPageMax = REPData[4]
                self.curPageIndex = REPData[5]
                patientInfo_m = REPData[3]
                self.patientInfo.clear()
                self.patientId_list.clear()
                self.select_row = None
                for i in patientInfo_m:
                    tempList = list(i)[1:]
                    self.patientId_list.append(i[0])
                    self.patientInfo.append(tempList)
                QMessageBox.information(self, '提示', '删除病人信息成功', QMessageBox.Ok)
                self.clear_layout(self.view.ui.verticalLayout_2)
                self.tableWidget = TableWidget(self.patientInfo, self.curPageIndex)
                self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.table.itemClicked.connect(self.set_selectRow)
                self.view.ui.verticalLayout.setStretch(0, 1)
                self.view.ui.verticalLayout.setStretch(1, 9)
            elif REPData[0] == '2':
                QMessageBox.information(self, '提示', '删除病人信息成功', QMessageBox.Ok)
                self.patientInfo.clear()
                self.patientId_list.clear()
                self.clear_layout(self.view.ui.verticalLayout_2)
                self.tableWidget = TableWidget(self.patientInfo, self.curPageIndex)
                self.view.ui.verticalLayout_2.addWidget(self.tableWidget)
                self.tableWidget.setPageController(self.curPageMax)  # 表格设置页码控制
                self.tableWidget.control_signal.connect(self.page_controller)
                self.tableWidget.table.itemClicked.connect(self.set_selectRow)
                self.view.ui.verticalLayout.setStretch(0, 1)
                self.view.ui.verticalLayout.setStretch(1, 9)
                QMessageBox.information(self, '提示', '无病人信息', QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "错误", "请将与该病人关联的全部信息删除后,再进行操作")
        except Exception as e:
            print('delPatientInfoRes', e)

    def on_clicked_patient_edit(self):
        try:
            if self.isEdit == True:
                QMessageBox.information(self, '提示', '请先完成编辑')
                return
            if self.isAdd:
                QMessageBox.information(self, '提示', '请先完成添加')
                return
            row = self.select_row
            if row is None:
                QMessageBox.information(self, '提示', '请选择要修改的病人信息')
                return
            self.isEdit = True
            self.itemIsEditable(row)

            # 默认日期
            birth = self.tableWidget.table.item(row, self.col_num - 6).text()
            date = re.compile(r"[\d+]+").findall(birth)
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            # print(year, month, day)
            date = QDate(year, month, day)

            # 默认性别
            sex = self.tableWidget.table.item(row, self.col_num - 5).text()
            self.edit_widget(row, default_sex=sex, default_date=date)

            self.confirmBtn.clicked.connect(lambda: self.editConfirm(row))
            self.cancelBtn.clicked.connect(lambda: self.editCancel(row))
        except Exception as e:
            print('on_clicked_patient_edit', e)

    def updatePatientInfoRes(self, REPData):
        try:
            patient_info = REPData[2][0]
            row = REPData[2][2]
            self.isEdit = False
            if self.isSearch:
                for i, patient in enumerate(self.patientInfo):
                    if patient[0] == self.searchInfo[row][0]:
                        row = i
                        print(f'New row: {row}')
                        break
                self.isSearch = False
                self.searchInfo.clear()
                self.searchID.clear()
            if REPData[0] == '1':
                self.patientInfo[row] = patient_info
                for i in range(0, self.col_num):
                    self.tableWidget.table.item(row, i).setText(patient_info[i])
                    self.itemIsEditable()
                QMessageBox.information(self, '提示', '修改病人信息成功', QMessageBox.Ok)
            else:
                QMessageBox.information(self,'提示','修改病人信息失败',QMessageBox.Ok)
        except Exception as e:
            print('updatePatientInfoRes', e)

    def set_selectRow(self, item):
        print(f'set_selectRow: {item.row()}')
        self.select_row = item.row()

    def clear_layout(self, layout, num=0, count=-1):
        item_list = list(range(layout.count()))
        item_list.reverse()
        # print(item_list)
        j = 0
        for i in item_list:
            if num == 0 and count == -1:
                item = layout.itemAt(i)
                layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
            elif num != 0 and count == -1:
                item = layout.itemAt(i)
                layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
                j += 1
                if j == num:
                    return
            elif num == 0 and count != -1:
                if j == count:
                    item = layout.itemAt(i)
                    layout.removeItem(item)
                    if item.widget():
                        item.widget().deleteLater()
                    return
                j += 1

    def prev_page(self):
        pass

    def next_page(self):
        pass

    def exit(self):
        self.client.getPatientInfoResSig.disconnect()
        self.client.addPatientInfoResSig.disconnect()
        self.client.delPatientInfoResSig.disconnect()
        self.client.updatePatientInfoResSig.disconnect()
        self.client.inqPatientInfoResSig.disconnect()
        self.client.patientPagingResSig.disconnect()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = patientManagerController()
    controller.client.getPatientInfo()
    sys.exit(app.exec_())

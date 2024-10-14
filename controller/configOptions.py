from view.configOptions import configOptionsView, PrentryView
from view.configOptions_form.ComboCheckBox import QComboCheckBox
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class configOptionsController(QWidget):
    def __init__(self, client, cAppUtil):
        super().__init__()
        self.client = client
        self.cAppUtil = cAppUtil
        self.view = configOptionsView()
        # self.sampling_rate, self.low_pass, self.high_pass, self.notch, self.scheme_name = self.jsUtil.get_data()
        self.client.getCurConfigDataResSig.connect(self.getCurConfigDataRes)
        self.client.getAllConfigDataResSig.connect(self.getAllConfigDataRes)
        self.client.chgCurUserConfigResSig.connect(self.chgCurUserConfigRes)
        self.view.ui.pushButton.clicked.connect(self.on_clicked_change_config)
        self.client.getCurConfigData()
        self.curConfig = []

    def getCurConfigDataRes(self, data):
        print(f'getCurConfigDataRes Data: {data}')
        self.curConfig = data
        self.view.ui.label_2.setText("方案选择：{}".format(self.curConfig[1]))
        # self.view.ui.lineEdit_5.setText(str(self.sampling_rate))
        self.view.ui.label_26.setText("系统采样率(Hz)：{}".format(self.curConfig[2]))
        # self.view.ui.lineEdit_4.setText(str(self.high_pass))
        self.view.ui.label_3.setText(
            "滤波频段(Hz)：陷波频率：{}    低通滤波：{}     高通频率：{}".format(self.curConfig[3], self.curConfig[4],
                                                                             self.curConfig[5]))
        print(f'getCurConfigDataRes tUser1: {self.client.tUser}')
        self.client.tUser[12] = data[0]

    def getAllConfigDataRes(self, configInfo):
        print(f'chgCurUserConfigRes: {configInfo}')
        self.configInfo = configInfo
        col_num = 5
        columnName = ['方案名', '采样率', '陷波频率', '低通滤波', '高通滤波']
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

        row_num = len(self.configInfo)
        self.prentryView.ui.tableWidget.setRowCount(row_num)
        for r in range(row_num):
            for i in range(col_num):
                self.prentryView.ui.tableWidget.setRowHeight(r, 45)
                item = QTableWidgetItem(str(self.configInfo[r][i + 1]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = item.font()
                font.setPointSize(11)
                item.setFont(font)
                self.prentryView.ui.tableWidget.setItem(r, i, item)
        self.prentryView.ui.tableWidget.verticalHeader().setVisible(False)


    def chgCurUserConfigRes(self, data):
        print(f'chgCurUserConfigRes data: {data}')
        if data[0] != '1':
            QMessageBox.information(self, '提示', '修改配置信息错误')

    def on_clicked_change_config(self):
        self.prentryView = PrentryView()
        self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
        self.prentryView.setWindowTitle("配置信息选择")
        self.prentryView.setWindowModality(Qt.ApplicationModal)
        self.prentryView.show()
        self.prentryView.ui.btnConfirm.setEnabled(False)
        self.prentryView.ui.btnReturn.setEnabled(True)
        self.prentryView.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.prentryView.ui.tableWidget.resizeRowsToContents()
        self.prentryView.ui.tableWidget.resizeColumnsToContents()
        self.prentryView.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.prentryView.ui.tableWidget.clicked.connect(self.on_tableWidget_itemClicked)
        self.prentryView.ui.btnConfirm.clicked.connect(self.on_btnConfirm_clicked)
        self.prentryView.ui.btnReturn.clicked.connect(self.on_btnReturn_clicked)

        self.client.getAllConfigData()

    def on_btnConfirm_clicked(self):
        row = self.prentryView.ui.tableWidget.currentRow()
        self.getCurConfigDataRes(self.configInfo[row])
        self.prentryView.close()

        self.client.chgCurUserConfig([self.configInfo[row][0]])

    def on_tableWidget_itemClicked(self):
        self.prentryView.ui.btnConfirm.setEnabled(True)

    def on_btnReturn_clicked(self):
        self.prentryView.close()

    def exit(self):
        self.client.getCurConfigDataResSig.disconnect()
        self.client.chgCurUserConfigResSig.disconnect()
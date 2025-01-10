import inspect
import ctypes

from PyQt5 import QtCore

from PyQt5.Qt import *

from view.consulting import DiagListView, PrentryView


class consultingController(QWidget):
    switchToEEG = pyqtSignal(list)
    def __init__(self, appUtil=None, client=None,page=None):
        super().__init__()
        self.view = DiagListView()
        self.client = client
        self.appUtil = appUtil
        self.client.ct_get_diags_notDiagResSig.connect(self.get_diags_notDiagRes)
        self.client.ct_get_fileNameByIdDateResSig.connect(self.get_fileNameByIdDateRes)
        self.client.ct_get_diags_notDiag([self.client.tUser[0]])

        # 处理客户端传回的提取取诊断信息
    def get_diags_notDiagRes(self, REPData):
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
        self.check_id = None
        self.file_id = None
        self.measure_date = None
        self.file_name = None
        self.view.init_table(self.diags_viewInfo, self.client.tUser, self.userNamesDict, self.paitentNamesDict,
                             self.on_clicked_manual_query, self.on_clicked_diag_query, self.on_clicked_diag_refused)
        self.view.show()

    # 槽对象中的槽函数
    def exit(self):
        self.client.ct_get_diags_notDiagResSig.disconnect()
        self.client.ct_get_fileNameByIdDateResSig.disconnect()
        self.switchToEEG.disconnect()

    def on_clicked_manual_query(self, diags_viewInfo, patient_name):
        self.check_id = diags_viewInfo[-4]
        self.uid = diags_viewInfo[2]
        self.patient_id = diags_viewInfo[0]
        self.measure_date = diags_viewInfo[1]
        self.patient_name = patient_name

        self.file_id = None
        self.file_name = None
        self.returnTo = 0
        msg = [diags_viewInfo[-4]]
        self.client.ct_get_fileNameByIdDate(msg)
        self.view.hide()

    def get_fileNameByIdDateRes(self, REPData):
        if REPData[0] == '0':
            QMessageBox.information(self, "选择脑电数据文件", REPData[2], QMessageBox.Yes)
            return False
        else:
            self.pre_info = REPData[1]
            col_num = 1
            self.prentryView = PrentryView()
            self.prentryView.setAttribute(Qt.WA_DeleteOnClose)
            self.prentryView.setWindowTitle("[选择脑电数据文件]")
            self.prentryView.setWindowModality(Qt.ApplicationModal)
            self.prentryView.ui.btnConfirm.setEnabled(False)
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

    def on_tableWidget_itemClicked(self):
        row = self.prentryView.ui.tableWidget.currentRow()
        if row < 0:
            return
        self.file_id = self.pre_info[row][1]
        self.file_name = '{:>03}.bdf'.format(self.file_id)
        self.prentryView.ui.btnConfirm.setEnabled(True)

    def on_btnConfirm_clicked(self):
        self.prentryView.close()
        self.switchToEEG.emit([self.file_id, self.file_name, self.check_id, self.patient_id, self.measure_date,['consultingController','']])

    def on_btnReturn_clicked(self):
        self.prentryView.close()
        self.view.show()

    def on_clicked_diag_query(self, diags_viewInfo):
        pass

    def on_clicked_diag_refused(self, diags_viewInfo,patient_name):
        pass

import sys
from functools import partial

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont

from view.manual_form.diagList import Ui_diagList
from view.manual_form.manual import Ui_ManualForm
from view.manual_form.setting import Ui_Setting
from view.manual_form.prentry import Ui_Prentry
from view.manual_form.sign_info import Ui_diag_MainWindow

from PyQt5.QtWidgets import *
class DiagTrainingView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ManualForm()
        self.ui.setupUi(self)


    # 显示病人相关信息
    def show_patient_info(self, patient, file_name, measure_date, start_time, end_time):
        name = patient[0][1]
        birth = str(patient[0][2])
        sex = patient[0][3]
        self.ui.labelPatientName.setText(name)
        self.ui.labelPatientBirth.setText(birth)
        self.ui.labelPatientSex.setText(sex)
        self.ui.labelPatientMeasure.setText(str(measure_date))
        self.ui.labelFileName.setText(file_name)
        meas_time = str(start_time) + ' - ' + str(end_time)
        self.ui.labelMeasureTime.setText(meas_time)


    # 显示样本信息
    def show_sample_detail(self, type_name='', channel='', lent='', begin='', end='', amp='', user_name=''):
        self.ui.labelType.setText(type_name)
        self.ui.labelChannel.setText(channel)
        if lent != '':
            lent = str(round(float(lent), 3))
        self.ui.labelLength.setText(lent)
        self.ui.labelBegin.setText(begin)
        self.ui.labelEnd.setText(end)
        if amp != '':
            amp = str(round(float(amp), 3))
        self.ui.labelAmp.setText(amp)
        self.ui.labelRole.setText(user_name)

class SettingView(QWidget):
    def __init__(self, type_name, user_name, type_filter, user_filter,parent=None):
        super().__init__(parent)
        self.ui = Ui_Setting()
        self.ui.setupUi(self, type_name, user_name, type_filter, user_filter)

class PrentryView(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Prentry()
        self.ui.setupUi(self)

class sign_InfoView(QMainWindow,QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_diag_MainWindow()
        self.ui.setupUi(self)

class DiagListView(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_diagList()
        self.ui.setupUi(self)
        #self.setWindowTitle("[诊断学习]学习诊断信息列表")

    def init_table(self, diags_viewInfo, userNamesDict, studentDict, paitentNamesDict, on_clicked_manual_query, on_clicked_diag_query, on_clicked_learn_query=None):
        try:
            self.ui.tableWidget.clear()

            self.ui.tableWidget.setColumnCount(10)
            self.ui.tableWidget.setColumnWidth(0, 140)
            self.ui.tableWidget.setColumnWidth(1, 160)
            self.ui.tableWidget.setColumnWidth(2, 260)
            self.ui.tableWidget.setColumnWidth(3, 160)
            self.ui.tableWidget.setColumnWidth(4, 160)
            self.ui.tableWidget.setColumnWidth(5, 80)
            self.ui.tableWidget.setColumnWidth(6, 160)
            self.ui.tableWidget.setColumnWidth(7, 160)
            self.ui.tableWidget.setColumnWidth(8, 160)
            self.ui.tableWidget.setColumnWidth(9, 220)
            self.ui.tableWidget.setHorizontalHeaderLabels(
                ["班级", '状态', '学习说明', '起始时间', '截止时间', '时长','检查单号', '医生','文件号', '操作'])
            ltip = {'beforeStudy':'未开始', 'studying': '学习中', 'studied':'学习完成','testing':'测试中', 'tested':'测试完成'}

            self.ui.tableWidget.removeRow(0)
            self.row_num = len(diags_viewInfo)
            if self.row_num <=0:
                self.ui.tableWidget.setRowCount(1)
                self.ui.tableWidget.setItem(0, 0, QTableWidgetItem("[无]"))
                self.ui.tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(0, 0).setFlags(Qt.ItemIsEditable)
                font = self.ui.tableWidget.item(0, 0).font()
                font.setPointSize(12)
                return

            self.ui.tableWidget.setRowCount(self.row_num)
            col_num = 9
            # 设置表格高度
            for i in range(self.row_num):
                self.ui.tableWidget.setRowHeight(i, 50)
            iFont = QFont("", 14)
            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            cur_class_id = None
            for row in range(0, self.row_num):
               if cur_class_id is None or cur_class_id != diags_viewInfo[row][0]:
                  i = 0
                  self.ui.tableWidget.setItem(row, i, QTableWidgetItem(diags_viewInfo[row][1]))
                  self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                  self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                  self.ui.tableWidget.item(row, i).setFont(iFont)
                  i = 1
                  self.ui.tableWidget.setItem(row, i, QTableWidgetItem(ltip[studentDict.get(diags_viewInfo[row][0])]))
                  self.ui.tableWidget.item(row, i ).setTextAlignment(Qt.AlignCenter)
                  self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                  self.ui.tableWidget.item(row, i).setFont(iFont)
                  i=2
                  self.ui.tableWidget.setItem(row, i , QTableWidgetItem(str(diags_viewInfo[row][2])))
                  self.ui.tableWidget.item(row, i ).setTextAlignment(Qt.AlignCenter)
                  self.ui.tableWidget.item(row, i ).setFlags(Qt.ItemIsEditable)
                  self.ui.tableWidget.item(row, i).setFont(iFont)
                  i=3
                  self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][3])[:10]))
                  self.ui.tableWidget.item(row, i ).setTextAlignment(Qt.AlignCenter)
                  self.ui.tableWidget.item(row, i ).setFlags(Qt.ItemIsEditable)
                  self.ui.tableWidget.item(row, i).setFont(iFont)
                  i= 4
                  self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][4])[:10]))
                  self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                  self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                  self.ui.tableWidget.item(row, i).setFont(iFont)
                  i = 5
                  self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][5])))
                  self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                  self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                  self.ui.tableWidget.item(row, i).setFont(iFont)

               i = 6
               self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][7])))
               self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
               self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
               self.ui.tableWidget.item(row, i).setFont(iFont)
               i = 7
               self.ui.tableWidget.setItem(row, i, QTableWidgetItem(userNamesDict.get(diags_viewInfo[row][11])))
               self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
               self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
               self.ui.tableWidget.item(row, i).setFont(iFont)
               i = 8
               self.ui.tableWidget.setItem(row, i, QTableWidgetItem('{:>03}.bdf'.format(str(diags_viewInfo[row][10]))))
               self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
               self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
               self.ui.tableWidget.item(row, i).setFont(iFont)

               # 添加最后一列
               layout = QHBoxLayout()

               self.ui.tableWidget.setCellWidget(row, col_num , QWidget())
               layout.setAlignment(Qt.AlignLeft)

               manualBtn = QPushButton('脑电图及其标注')
               manualBtn.clicked.connect(partial(on_clicked_manual_query, diags_viewInfo[row],paitentNamesDict.get(diags_viewInfo[row][8])))
               manualBtn.setStyleSheet('height : 50px;width:140px;font : 18px;color:blue')
               manualBtn.setCursor(Qt.PointingHandCursor)
               manualBtn.setFont(iFont)
               manualBtn.setToolTip("诊断学习:脑电图及其标注")
               layout.addWidget(manualBtn)
               diagBtn = QPushButton('诊断信息')
               diagBtn.clicked.connect(partial(on_clicked_diag_query, diags_viewInfo[row],paitentNamesDict.get(diags_viewInfo[row][8])))
               diagBtn.setStyleSheet('height : 50px;width:80px;font : 18px;color:blue')
               diagBtn.setCursor(Qt.PointingHandCursor)
               diagBtn.setFont(iFont)
               layout.addWidget(diagBtn)
               if cur_class_id is None or cur_class_id != diags_viewInfo[row][0]:
                    learnInfoBtn = QPushButton('学习记录')
                    learnInfoBtn.clicked.connect(partial(on_clicked_learn_query, diags_viewInfo[row]))
                    learnInfoBtn.setStyleSheet('height : 50px;width:100px;font : 18px;color:blue')
                    learnInfoBtn.setCursor(Qt.PointingHandCursor)
                    learnInfoBtn.setFont(iFont)
                    layout.addWidget(learnInfoBtn)
                    cur_class_id = diags_viewInfo[row][0]

               self.ui.tableWidget.cellWidget(row, col_num ).setLayout(layout)

        except Exception as e:
            print('initTable', e)

    #def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
    #    reply = QMessageBox.information(self, '提示', '是否退出程序', QMessageBox.Yes | QMessageBox.No)
    #    self.hide()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = DiagListView()
    view.show()
    sys.exit(app.exec_())
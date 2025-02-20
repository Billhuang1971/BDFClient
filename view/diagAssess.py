
from functools import partial

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont

from view.manual_form.diagList import Ui_diagList
from view.manual_form.manual import Ui_ManualForm
from view.manual_form.setting import Ui_Setting
from view.manual_form.prentry import Ui_Prentry
from view.manual_form.sign_info import Ui_diag_MainWindow
from view.manual_form.sign_info1 import Ui_diag_MainWindow1

from PyQt5.QtWidgets import *

class DiagAssessView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ManualForm()
        self.ui.setupUi(self)
        self.initInfo()
    def initInfo(self):
        self.ui.gbPatientInfo.setTitle("学员及病人信息")
        self.ui.labelPatientNameInfo.setText("病人：")
        self.ui.labelPatientName.setText(" ")
        self.ui.labelPatientSexInfo.setText("性别：")
        self.ui.labelPatientSex.setText(" ")
        self.ui.labelPatientBirthInfo.setText("学员：")
        self.ui.labelPatientBirth.setText(" ")
        self.ui.labelPatientMeasureInfo.setText("当前题数：")
        self.ui.labelPatientMeasure.setText(" ")
        self.ui.labelMeasureTimeInfo.setText("当前比例：")
        self.ui.labelMeasureTime.setText(" ")
        self.ui.labelFileNameInfo.setText("课堂比例：")
        self.ui.labelFileName.setText(" ")

    # 显示病人相关信息
    def show_patient_info(self, patient, student, qsum, asum, grade):
        name = patient[0][1]
        sex = patient[0][3]
        self.ui.labelPatientName.setText(name)
        self.ui.labelPatientBirth.setText(student)
        self.ui.labelPatientSex.setText(sex)
        self.ui.labelPatientMeasure.setText(f'{qsum},   正确数：{asum}')
        if qsum>0 and asum>=0:
            ts=f'{(int(asum*100/qsum))}%'
        else:
            ts = f'{int(asum)}:{int(qsum)}'
        self.ui.labelMeasureTime.setText(ts)
        self.ui.labelFileName.setText(f'{grade}%')


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

class sign_InfoView1(QMainWindow,QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_diag_MainWindow1()
        self.ui.setupUi(self)

class DiagListView(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_diagList()
        self.ui.setupUi(self)
        self.setWindowTitle("[学习评估]课堂列表")

    def init_table(self, diags_viewInfo, on_clicked_manual_query,on_btnDelClass_clicked):
        try:

            self.ui.tableWidget.clear()

            self.ui.tableWidget.setColumnCount(6)
            self.ui.tableWidget.setColumnWidth(0, 140)
            self.ui.tableWidget.setColumnWidth(1, 260)
            self.ui.tableWidget.setColumnWidth(2, 160)
            self.ui.tableWidget.setColumnWidth(3, 160)
            self.ui.tableWidget.setColumnWidth(4, 80)
            self.ui.tableWidget.setColumnWidth(5, 220)
            self.ui.tableWidget.setHorizontalHeaderLabels(
                ["班级名称",'学习说明', '起始时间', '截止时间', '时长', '操作'])

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
            col_num = 5
            # 设置表格高度
            for i in range(self.row_num):
                self.ui.tableWidget.setRowHeight(i, 50)

            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            iFont = QFont("", 14)


            for row in range(0, self.row_num):
              i = 0
              self.ui.tableWidget.setItem(row, i, QTableWidgetItem(diags_viewInfo[row][3]))
              self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)
              i=1
              self.ui.tableWidget.setItem(row, i , QTableWidgetItem(str(diags_viewInfo[row][4])))
              self.ui.tableWidget.item(row, i ).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i ).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)
              i=2
              self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][5])[:10]))
              self.ui.tableWidget.item(row, i ).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i ).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)
              i = 3
              self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][6])[:10]))
              self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)

              i = 4
              self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][7])))
              self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)


              # 添加最后一列
              layout = QHBoxLayout()
              self.ui.tableWidget.setCellWidget(row, col_num , QWidget())

              manualBtn = QPushButton('查看学员')
              manualBtn.clicked.connect(partial(on_clicked_manual_query, diags_viewInfo[row],row))
              manualBtn.setStyleSheet('height : 50px;width:60px;font : 18px;color:blue')
              manualBtn.setCursor(Qt.PointingHandCursor)
              manualBtn.setToolTip("学习评估:查看学员")
              layout.addWidget(manualBtn)
              if on_btnDelClass_clicked is not None:
                delClassBtn = QPushButton('删除本课堂')
                delClassBtn.clicked.connect(
                     partial(on_btnDelClass_clicked, diags_viewInfo[row]))
                delClassBtn.setStyleSheet('height : 50px;width:60px;font : 18px;color:blue')
                delClassBtn.setCursor(Qt.PointingHandCursor)
                delClassBtn.setToolTip("删除本课堂:删除课堂内容、学员及其学习、测试记录。")
                layout.addWidget(delClassBtn)
              self.ui.tableWidget.cellWidget(row, col_num ).setLayout(layout)

        except Exception as e:
            print('initTable', e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = DiagAssessView()
    view.show()
    sys.exit(app.exec_())
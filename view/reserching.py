import sys
from functools import partial

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtGui import QFont

from view.reserching_from.form import Ui_Form
from view.manual_form.manual import Ui_ManualForm
from view.manual_form.setting import Ui_Setting

from PyQt5.QtWidgets import *
class ReserchingView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ManualForm()
        self.ui.setupUi(self)
        self.ui.gbPatientInfo.setTitle("任务信息")


    # 显示病人相关信息
    def show_patient_info(self, patient, file_name, measure_date, start_time, end_time,theme,check_num):
        self.ui.gbPatientInfo.setTitle(theme)
        name = patient[0][1]
        birth = str(patient[0][2])
        sex = patient[0][3]
        self.ui.labelPatientName.setText(name)
        self.ui.labelPatientBirthInfo.setText("检查单号：")
        self.ui.labelPatientBirth.setText(check_num)
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


class diagListView(QWidget):#首页ui
    page_control_signal = pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.homePage.clicked.connect(self.home_page)
        self.ui.prePage.clicked.connect(self.pre_page)
        self.ui.nextPage.clicked.connect(self.next_page)
        self.ui.finalPage.clicked.connect(self.final_page)
        self.ui.confirmSkip.clicked.connect(self.confirm_skip)
        self.ui.pushButton.clicked.connect(self.my_Query)
        self.ui.label1.hide()
        self.ui.comboBox.hide()
        self.ui.label2.hide()
        self.ui.comboBox2.hide()
        # self.setWindowTitle("[科研标注]标注信息列表")

    def init_table(self, diags_viewInfo, userNamesDict, paitentNamesDict, on_clicked_manual_query,on_clicked_submit,curPageIndex=1,maxPages=1):
        try:

            self.ui.tableWidget.clear()
            self.ui.curPage.setText(str(curPageIndex))
            self.ui.totalPage.setText(f"共{maxPages}页")

            self.ui.tableWidget.setColumnCount(9)
            self.ui.tableWidget.setColumnWidth(0, 260)
            self.ui.tableWidget.setColumnWidth(1, 120)
            self.ui.tableWidget.setColumnWidth(2, 400)
            self.ui.tableWidget.setColumnWidth(3, 160)
            self.ui.tableWidget.setColumnWidth(4, 100)
            self.ui.tableWidget.setColumnWidth(5, 160)
            self.ui.tableWidget.setColumnWidth(6, 200)
            self.ui.tableWidget.setColumnWidth(7, 100)
            self.ui.tableWidget.setColumnWidth(8, 200)
            self.ui.tableWidget.setHorizontalHeaderLabels(
                ["主题", '主题状态', '标注说明','检查单号','病人', '文件号', '任务状态', '标注员','操作'])

            ltip = {'notStarted': '未开始', 'labelling': '标注中', 'labelled': '标注完成', 'qualified': '合格',
                    'notqualified': '不合格'}
            self.ui.tableWidget.removeRow(0)
            self.row_num = len(diags_viewInfo)
            if self.row_num <= 0:
                self.ui.tableWidget.setRowCount(1)
                self.ui.tableWidget.setItem(0, 0, QTableWidgetItem("[无]"))
                self.ui.tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(0, 0).setFlags(Qt.ItemIsEditable)
                font = self.ui.tableWidget.item(0, 0).font()
                font.setPointSize(12)
                return

            self.ui.tableWidget.setRowCount(self.row_num)
            col_num = 8
            # 设置表格高度
            for i in range(self.row_num):
                self.ui.tableWidget.setRowHeight(i, 50)
            iFont = QFont("", 14)
            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            cur_theme_id = None
            for row in range(0, self.row_num):
                if cur_theme_id is  None or cur_theme_id!=diags_viewInfo[row][0]:
                    i = 0
                    self.ui.tableWidget.setItem(row, i, QTableWidgetItem(diags_viewInfo[row][1]))
                    self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                    self.ui.tableWidget.item(row, i).setFont(iFont)

                    i = 1
                    self.ui.tableWidget.setItem(row, i, QTableWidgetItem(diags_viewInfo[row][4]))
                    self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                    self.ui.tableWidget.item(row, i).setFont(iFont)

                    i = 2
                    self.ui.tableWidget.setItem(row, i, QTableWidgetItem(diags_viewInfo[row][2]))
                    self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                    self.ui.tableWidget.item(row, i).setFont(iFont)

                    cur_theme_id=diags_viewInfo[row][0]
                i = 3
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][8])))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                self.ui.tableWidget.item(row, i).setFont(iFont)

                i = 4
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(paitentNamesDict.get(diags_viewInfo[row][9])))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                self.ui.tableWidget.item(row, i).setFont(iFont)

                i = 5
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem('{:>03}.bdf'.format(str(diags_viewInfo[row][11]))))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                self.ui.tableWidget.item(row, i).setFont(iFont)

                i = 6
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(diags_viewInfo[row][3]))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                self.ui.tableWidget.item(row, i).setFont(iFont)
                i = 7
                self.ui.tableWidget.setItem(row, i, QTableWidgetItem(userNamesDict.get(diags_viewInfo[row][12])))
                self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                self.ui.tableWidget.item(row, i).setFont(iFont)

                # 添加最后一列
                layout = QHBoxLayout()
                self.ui.tableWidget.setCellWidget(row, col_num , QWidget())

                manualBtn = QPushButton('脑电数据标注')
                manualBtn.clicked.connect(partial(on_clicked_manual_query, diags_viewInfo[row],paitentNamesDict.get(diags_viewInfo[row][9])))
                manualBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                manualBtn.setCursor(Qt.PointingHandCursor)
                manualBtn.setToolTip("科研标注:脑电数据图标注")
                layout.addWidget(manualBtn)

                completeBtn = QPushButton('提交标注任务')
                completeBtn.clicked.connect(
                    partial(on_clicked_submit, diags_viewInfo[row], paitentNamesDict.get(diags_viewInfo[row][9])))
                completeBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                completeBtn.setCursor(Qt.PointingHandCursor)
                completeBtn.setToolTip("科研标注:提交标注任务")
                layout.addWidget(completeBtn)


                layout.setStretch(0, 1)
                layout.setStretch(1, 1)
                self.ui.tableWidget.cellWidget(row, col_num ).setLayout(layout)

        except Exception as e:
            print('initTable', e)

    def home_page(self):
        self.page_control_signal.emit(["home"])

    def pre_page(self):
        self.page_control_signal.emit(["pre"])

    def next_page(self):
        self.page_control_signal.emit(["next"])

    def final_page(self):
        self.page_control_signal.emit(["final"])

    def confirm_skip(self):
        self.page_control_signal.emit(["confirm"])


    def my_Query(self):
        self.page_control_signal.emit(["query"])
    #def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
    #    reply = QMessageBox.information(self, '提示', '是否退出程序', QMessageBox.Yes | QMessageBox.No)
    #    self.hide()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = ReserchingView()
    view.show()
    sys.exit(app.exec_())
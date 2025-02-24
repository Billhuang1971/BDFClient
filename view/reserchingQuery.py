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


class diagListView(QWidget):
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
        # self.setWindowTitle("[科研标注]标注信息列表")

        self.ui.comboBox.removeItem(1)
        self.ui.comboBox2.removeItem(1)
        self.ui.comboBox2.removeItem(1)

    def init_table(self, diags_viewInfo, userNamesDict, paitentNamesDict,  themeDict, on_clicked_manual_query,on_clicked_theme_commit, on_clicked_label_commit, curPageIndex=1,maxPages=1):
        try:

            self.ui.tableWidget.clear()
            self.ui.curPage.setText(str(curPageIndex))
            self.ui.totalPage.setText(f"共{maxPages}页")

            self.ui.tableWidget.setColumnCount(10)
            self.ui.tableWidget.setColumnWidth(0, 260)
            self.ui.tableWidget.setColumnWidth(1, 120)
            self.ui.tableWidget.setColumnWidth(2, 400)
            self.ui.tableWidget.setColumnWidth(3, 160)
            self.ui.tableWidget.setColumnWidth(4, 100)
            self.ui.tableWidget.setColumnWidth(5, 160)
            self.ui.tableWidget.setColumnWidth(6, 200)
            self.ui.tableWidget.setColumnWidth(7, 100)
            self.ui.tableWidget.setColumnWidth(8, 200)
            self.ui.tableWidget.setColumnWidth(9, 200)
            self.ui.tableWidget.setHorizontalHeaderLabels(
                ["主题", '主题状态', '标注说明','检查单号','病人', '文件号', '任务状态', '标注员', '打开文件', '评判'])

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
            theme_idValues = themeDict.keys()
            for row in range(0, self.row_num):
                if cur_theme_id is None or cur_theme_id != diags_viewInfo[row][0]:
                    i = 0
                    self.ui.tableWidget.setItem(row, i, QTableWidgetItem(diags_viewInfo[row][1]))
                    self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                    self.ui.tableWidget.item(row, i).setFont(iFont)

                    i = 1
                    if diags_viewInfo[row][0] not in theme_idValues or themeDict.get(diags_viewInfo[row][0]) <= 0:
                       layout5 = QHBoxLayout()
                       self.ui.tableWidget.setCellWidget(row, i, QWidget())
                       usableBtn = QPushButton('可用')
                       usableBtn.clicked.connect(partial(on_clicked_theme_commit, diags_viewInfo[row], 'usable'))
                       usableBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                       usableBtn.setCursor(Qt.PointingHandCursor)
                       usableBtn.setToolTip("执行查看:设置主题为可用")
                       layout5.addWidget(usableBtn)
                       notusableBtn = QPushButton('不可用')
                       notusableBtn.clicked.connect(
                                partial(on_clicked_theme_commit, diags_viewInfo[row], 'notUsable'))
                       notusableBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                       notusableBtn.setCursor(Qt.PointingHandCursor)
                       notusableBtn.setToolTip("执行查看:设置主题为不可用")
                       layout5.addWidget(notusableBtn)
                       layout5.setStretch(0, 1)
                       layout5.setStretch(1, 1)
                       self.ui.tableWidget.cellWidget(row, i).setLayout(layout5)
                    else:
                       self.ui.tableWidget.setItem(row, i, QTableWidgetItem(diags_viewInfo[row][4]))
                       self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                       self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                       self.ui.tableWidget.item(row, i).setFont(iFont)

                    i = 2
                    self.ui.tableWidget.setItem(row, i, QTableWidgetItem(diags_viewInfo[row][2]))
                    self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
                    self.ui.tableWidget.item(row, i).setFont(iFont)
                    cur_theme_id = diags_viewInfo[row][0]

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
                container1 = QWidget()

                manualBtn = QPushButton('查看标注')
                manualBtn.clicked.connect(partial(on_clicked_manual_query, diags_viewInfo[row],paitentNamesDict.get(diags_viewInfo[row][9])))
                manualBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                manualBtn.setCursor(Qt.PointingHandCursor)
                manualBtn.setToolTip("执行查看:脑电数据图标注")
                layout.addWidget(manualBtn)
                layout.setStretch(0, 1)
                layout.setStretch(1, 1)
                container1.setLayout(layout)

                self.ui.tableWidget.setCellWidget(row, 8, container1)

                layout1 = QHBoxLayout()
                container2 = QWidget()

                qualifiedBtn = QPushButton('合格')
                qualifiedBtn.clicked.connect(
                    partial(on_clicked_label_commit, diags_viewInfo[row], 'qualified'))
                qualifiedBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                qualifiedBtn.setCursor(Qt.PointingHandCursor)
                qualifiedBtn.setToolTip("合格")
                layout1.addWidget(qualifiedBtn)

                notQualifiedBtn = QPushButton('不合格')
                notQualifiedBtn.clicked.connect(
                    partial(on_clicked_label_commit, diags_viewInfo[row], 'notqualified'))
                notQualifiedBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                notQualifiedBtn.setCursor(Qt.PointingHandCursor)
                notQualifiedBtn.setToolTip("不合格")

                layout1.addWidget(notQualifiedBtn)
                layout1.setStretch(0, 1)
                layout1.setStretch(1, 1)
                container2.setLayout(layout1)
                self.ui.tableWidget.setCellWidget(row, 9, container2)
                if diags_viewInfo[row][3] != 'labelled':
                    notQualifiedBtn.setEnabled(False)
                    qualifiedBtn.setEnabled(False)
                    qualifiedBtn.setStyleSheet('height : 50px;font : 18px;color:black')
                    notQualifiedBtn.setStyleSheet('height : 50px;font : 18px;color:black')

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
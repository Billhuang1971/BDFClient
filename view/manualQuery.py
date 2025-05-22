import sys
import typing
from functools import partial

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from view.manualQuery_from.form import Ui_Form
from view.manual_form.manual import Ui_ManualForm
from view.manual_form.setting import Ui_Setting
from view.manual_form.prentry import Ui_Prentry
from view.manual_form.setBdf import Ui_SetBdf
from view.manual_form.sign_info import Ui_diag_MainWindow
from view.manual_form.diagList import Ui_diagList
from view.manual_form.prentry import Ui_Prentry

from PyQt5.QtWidgets import *

class PrentryView(QWidget):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Prentry()
        self.ui.setupUi(self)
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.hide()

class sign_InfoView(QMainWindow,QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_diag_MainWindow()
        self.ui.setupUi(self)

class ManualView(QWidget):
    page_control_signal = pyqtSignal(list)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.homePage.clicked.connect(self.home_page)
        self.ui.prePage.clicked.connect(self.pre_page)
        self.ui.nextPage.clicked.connect(self.next_page)
        self.ui.finalPage.clicked.connect(self.final_page)
        self.ui.confirmSkip.clicked.connect(self.confirm_skip)

        self.ui.pushButton.clicked.connect(self.my_Query)
        self.ui.pushButton_reset.clicked.connect(self.reset)
    # def mouseDoubleClickEvent(self, a0: typing.Optional[QtGui.QMouseEvent]):
    #     self.ui.date_lineEdit.clear()

    def init_table(self, diags_viewInfo,curUser,userNamesDict,paitentNamesDict,on_clicked_manual_query,
                   on_clicked_diag_query,curPageIndex,maxPages):
        try:
            self.ui.tableWidget.clear()
            self.ui.tableWidget.setHorizontalHeaderLabels(["检查单号", '病人', '测量日期', '医生', '状态','诊断时间','操作'])
            self.ui.tableWidget.removeRow(0)
            self.ui.curPage.setText(str(curPageIndex))
            self.ui.totalPage.setText(f"共{maxPages}页")

            self.row_num = len(diags_viewInfo)
            if self.row_num <= 0:
                self.ui.tableWidget.setRowCount(1)
                self.ui.tableWidget.setItem(0, 0, QTableWidgetItem("[无]"))
                self.ui.tableWidget.item(0, 0).setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget.item(0, 0).setFlags(Qt.ItemIsEditable)
                font = self.ui.tableWidget.item(0, 0).font()
                font.setPointSize(12)

                return
            col_num = 6
            if self.row_num>12:
                self.row_num=12

            self.ui.tableWidget.setRowCount(self.row_num)
            # 设置表格高度
            for i in range(self.row_num):
                self.ui.tableWidget.setRowHeight(i, 50)

            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            iFont=QFont("", 14)
            for row in range(0, self.row_num):
              i = 0
              self.ui.tableWidget.setItem(row, i, QTableWidgetItem(diags_viewInfo[row][-2]))
              self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)

              i = i + 1
              if paitentNamesDict.get(diags_viewInfo[row][0]) == None:
                  self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][0])))
              else:
                  self.ui.tableWidget.setItem(row, i, QTableWidgetItem(paitentNamesDict.get(diags_viewInfo[row][0])))
              self.ui.tableWidget.item(row, i ).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)

              i=i+1
              self.ui.tableWidget.setItem(row, i , QTableWidgetItem(str(diags_viewInfo[row][1])))
              self.ui.tableWidget.item(row, i ).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i ).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)
              i=i+1
              if userNamesDict.get(diags_viewInfo[row][2]) == None:
                  self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][2])))
              else:
                  self.ui.tableWidget.setItem(row, i, QTableWidgetItem(userNamesDict.get(diags_viewInfo[row][2])))
              self.ui.tableWidget.item(row, i ).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i ).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)

              i = i + 1
              self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][3])))
              self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)

              i = i + 1
              self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][4]).format("yyyy-MM-dd")))
              self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)

              # 添加最后一列
              layout = QHBoxLayout()
              self.ui.tableWidget.setCellWidget(row, col_num , QWidget())

              manualBtn = QPushButton('选择脑电数据文件...')
              manualBtn.clicked.connect(partial(on_clicked_manual_query, diags_viewInfo[row],paitentNamesDict.get(diags_viewInfo[row][0])))
              manualBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
              manualBtn.setCursor(Qt.PointingHandCursor)
              manualBtn.setToolTip("诊断查询:选择脑电数据文件")
              layout.addWidget(manualBtn)

              diagBtn = QPushButton('查看诊断信息')
              diagBtn.clicked.connect(partial(on_clicked_diag_query, diags_viewInfo[row],paitentNamesDict.get(diags_viewInfo[row][0])))
              diagBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
              diagBtn.setCursor(Qt.PointingHandCursor)
              layout.addWidget(diagBtn)

              layout.setStretch(0, 1)
              layout.setStretch(1, 1)
              #layout.setStretch(2, 1)
              #layout.setStretch(3, 8)
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

    def reset(self):
        self.page_control_signal.emit(["reset"])
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     view = ManualView()
#     view.show()
#     sys.exit(app.exec_())
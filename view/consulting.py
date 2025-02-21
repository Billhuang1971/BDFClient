import sys
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from view.manual_form.diagList import Ui_diagList
from view.manual_form.prentry import Ui_Prentry
from view.manual_form.sign_info import Ui_diag_MainWindow

from PyQt5.QtWidgets import *

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


    def init_table(self, diags_viewInfo,curUser,userNamesDict,paitentNamesDict,on_clicked_manual_query,on_clicked_diag_query,on_clicked_diag_refused=None):
        try:
            self.ui.tableWidget.setColumnCount(7)
            self.ui.tableWidget.setHorizontalHeaderLabels(
                ["检查单号", '病人', '测量日期', '医生', '状态', '诊断时间', '操作'])
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
            col_num = 6
            # 设置表格高度
            for i in range(self.row_num):
                self.ui.tableWidget.setRowHeight(i, 50)
            iFont = QFont("", 14)
            #self.ui.tableWidget.setStretchLastSection(True)
            self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
            cur_check_id=None
            for row in range(0, self.row_num):
              i = 0
              if cur_check_id is None or cur_check_id!=diags_viewInfo[row][-4]:
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
                cur_check_id=diags_viewInfo[row][-4]
              else:
                i+=2
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
              self.ui.tableWidget.setItem(row, i, QTableWidgetItem(str(diags_viewInfo[row][4])[:10]))
              self.ui.tableWidget.item(row, i).setTextAlignment(Qt.AlignCenter)
              self.ui.tableWidget.item(row, i).setFlags(Qt.ItemIsEditable)
              self.ui.tableWidget.item(row, i).setFont(iFont)

              # 添加最后一列
              layout = QHBoxLayout()
              layout.setAlignment(Qt.AlignLeft)

              self.ui.tableWidget.setCellWidget(row, col_num , QWidget())
              if on_clicked_diag_refused is not None and diags_viewInfo[row][3]=='notDiagnosed' and diags_viewInfo[row][2]==curUser[0]:
                  refuseBtn = QPushButton('拒绝')
                  refuseBtn.clicked.connect(partial(on_clicked_diag_refused, diags_viewInfo[row],paitentNamesDict.get(diags_viewInfo[row][0])))
                  refuseBtn.setStyleSheet('height : 50px;width:60px;font : 18px;color:blue')
                  refuseBtn.setCursor(Qt.PointingHandCursor)
                  layout.addWidget(refuseBtn)

              manualBtn = QPushButton('选择脑电文件...')
              manualBtn.clicked.connect(partial(on_clicked_manual_query, diags_viewInfo[row],paitentNamesDict.get(diags_viewInfo[row][0])))
              manualBtn.setStyleSheet('height : 50px;width:140px;font : 18px;color:blue')
              manualBtn.setCursor(Qt.PointingHandCursor)
              manualBtn.setToolTip("脑电会诊:选择脑电数据文件")
              layout.addWidget(manualBtn)

              btnSignInfo = QPushButton('填写诊断信息')
              btnSignInfo.clicked.connect(partial(on_clicked_diag_query,diags_viewInfo[row],paitentNamesDict.get(diags_viewInfo[row][0])))
              btnSignInfo.setStyleSheet('height : 50px;width:140px;font : 18px;color:blue')
              btnSignInfo.setCursor(Qt.PointingHandCursor)
              layout.addWidget(btnSignInfo)
              # if diags_viewInfo[row][3] == 'diagnosed':
              #    diagBtn = QPushButton('查看诊断信息')
              #    diagBtn.clicked.connect(partial(on_clicked_diag_query, diags_viewInfo[row]))
              #    diagBtn.setStyleSheet('height : 50px;width:140px;font : 18px;color:blue')
              #    diagBtn.setCursor(Qt.PointingHandCursor)
              #    layout.addWidget(diagBtn)


              self.ui.tableWidget.cellWidget(row, col_num ).setLayout(layout)
            self.ui.tableWidget.setColumnWidth(5, 150)
        except Exception as e:
            print('initTable', e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = DiagListView()
    view.show()
    sys.exit(app.exec_())
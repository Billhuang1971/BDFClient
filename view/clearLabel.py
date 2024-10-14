import sys


from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QBrush

from view.clearLabel_form.form import Ui_ClearLabelForm
from PyQt5.QtWidgets import *

class clearLabelView(QWidget):
    page_control_signal = pyqtSignal(list)

    def __init__(self, parent=None,):
        super().__init__(parent)
        self.ui = Ui_ClearLabelForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.__home_page)
        self.ui.pushButton_2.clicked.connect(self.__pre_page)
        self.ui.pushButton_3.clicked.connect(self.__next_page)
        self.ui.pushButton_4.clicked.connect(self.__final_page)
        self.ui.pushButton_5.clicked.connect(self.__confirm_skip)

    def initView(self, init_info, itemName):
        try:
            self.ui.tableWidget.clear()
            col_num = 5
            self.ui.tableWidget.setColumnCount(col_num)
            for i in range(col_num):
                header_item = QTableWidgetItem(itemName[i])
                font = header_item.font()
                font.setPointSize(12)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                self.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
            self.ui.tableWidget.horizontalHeader().setHighlightSections(False)
            self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            row_num = len(init_info)
            self.ui.tableWidget.setRowCount(row_num)
            for r in range(row_num):
                for c in range(col_num):
                    item = QTableWidgetItem(str(init_info[r][c]))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.ui.tableWidget.setItem(r, c, item)
            # self.view.ui.tableWidget.verticalHeader().setVisible(False)
        except Exception as e:
            print('initView', e)

    def __home_page(self):
        """点击首页信号"""
        self.page_control_signal.emit(["home", self.ui.label_2.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.page_control_signal.emit(["pre", self.ui.label_2.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.page_control_signal.emit(["next", self.ui.label_2.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.page_control_signal.emit(["final", self.ui.label_2.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.page_control_signal.emit(["confirm", self.ui.lineEdit.text()])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = clearLabelView()
    view.show()
    sys.exit(app.exec_())
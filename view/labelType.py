import sys
from view.labelType_form.form import Ui_LabelTypeForm
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt5.QtGui import QBrush
import sys

class LabelTypeView(QWidget):
    def __init__(self, parent=None,):
        super().__init__(parent)
        self.ui = Ui_LabelTypeForm()
        self.ui.setupUi(self)

        # header表格头 field数据库表属性
        self.header = ['标注类型名称', '描述', '类别']
        self.field = ['type_name', 'description', 'category']
        self.category = ['正常波形', '异常波形', '伪迹波形', '正常状态', '异常状态', '伪迹状态']

    def initTable(self, data):
        col_num = len(self.header)
        row_num = len(data)
        self.ui.tableWidget.setColumnCount(col_num)
        self.ui.tableWidget.setRowCount(row_num)
        for i in range(col_num):
            header_item = QTableWidgetItem(self.header[i])
            font = header_item.font()
            font.setPointSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, self.field[i])
            self.ui.tableWidget.setHorizontalHeaderItem(i, header_item)

        for r in range(row_num):
            for c in range(col_num):
                self.item = QTableWidgetItem(str(data[r][c + 1]))
                self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                font = self.item.font()
                font.setPointSize(10)
                self.item.setFont(font)
                self.ui.tableWidget.setItem(r, c, self.item)
        self.initCombocond()
        self.ui.tableWidget.horizontalHeader().setHighlightSections(False)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 增加和查询的时候列数会改变，所以需要保存原来的列数
        self.col = self.ui.tableWidget.columnCount()

    def initCombocond(self):
        self.ui.comboCond.clear()
        for i in range(len(self.field)):
            self.ui.comboCond.addItem(self.header[i],self.field[i])
            self.ui.comboCond.adjustSize()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = LabelTypeView()
    view.show()
    sys.exit(app.exec_())
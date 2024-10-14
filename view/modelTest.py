import sys
import weakref

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QHeaderView, QTableWidgetItem, QAbstractItemView

from view.testmodel_form.test import Ui_Testing


class modelTestView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Testing()
        self.ui.setupUi(self)
        self.classifier_header = ['分类器名称', '数据集名称', '算法名称', '参数']
        self.testOutput = weakref.proxy(self.ui.editTrainOutput)


    # 渲染分类器信息列表
    def updateClassifierTable(self, data, page, pageNum):
        try:
            if data is None:
                data = []
            self.updateClassifierLabel('无', '')
            self.ui.now_page.setText('第' + str(page) + '页')
            self.ui.all_page.setText('共' + str(pageNum) + '页')
            col_num = len(self.classifier_header)
            row_num = len(data)
            self.ui.algorithm_tableWidget.setColumnCount(col_num)
            self.ui.algorithm_tableWidget.setRowCount(row_num)
            # 设置表格高度
            for i in range(row_num):
                self.ui.algorithm_tableWidget.setRowHeight(i, 55)
            for i in range(col_num - 1):
                self.ui.algorithm_tableWidget.setColumnWidth(i, 200)
            self.ui.algorithm_tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.ui.algorithm_tableWidget.setHorizontalHeaderLabels(self.classifier_header)
            # 设置表头格式
            self.ui.algorithm_tableWidget.horizontalHeader().setStyleSheet(
                '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
            # 使表格填满整个widget
            self.ui.algorithm_tableWidget.horizontalHeader().setStretchLastSection(True)

            for r in range(row_num):
                for c in range(col_num):
                    item = QTableWidgetItem(str(data[r][c + 1]))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    font = item.font()
                    font.setPointSize(10)
                    item.setFont(font)
                    self.ui.algorithm_tableWidget.setItem(r, c, item)

            self.ui.algorithm_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.ui.algorithm_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        except Exception as e:
            print('initClassifierTable', e)

    # 渲染具体分类器信息和测试情况
    def updateClassifierLabel(self, classifier_name, classifier_state):
        self.ui.label_model_state.setText('当前模型状态：' + str(classifier_state))
        self.ui.label_algname.setText('当前被选中的分类器：' + str(classifier_name))


    # 渲染数据到输出窗口
    def output_info(self, msg):
        try:
            self.testOutput.appendPlainText(str(msg))
            QApplication.processEvents()
        except Exception as e:
            print('output_info', e)


    # 隐藏按钮
    def hidden_btn(self):
        try:
            self.ui.first_page.setEnabled(False)
            self.ui.next_page.setEnabled(False)
            self.ui.last_page.setEnabled(False)
            self.ui.end_page.setEnabled(False)
            self.ui.search.setEnabled(False)
        except Exception as e:
            print('hidden_btn', e)


    # 显示按钮
    def show_btn(self):
        try:
            self.ui.first_page.setEnabled(True)
            self.ui.next_page.setEnabled(True)
            self.ui.last_page.setEnabled(True)
            self.ui.end_page.setEnabled(True)
            self.ui.search.setEnabled(True)
        except Exception as e:
            print('show_btn', e)


    # 页面锁定
    def view_lock(self):
        try:
            self.ui.pushButton_test.setText("测试中")
            self.ui.algorithm_tableWidget.setEnabled(False)
            self.ui.pushButton_test.setEnabled(False)
            self.ui.reset.setEnabled(False)
            self.hidden_btn()
        except Exception as e:
            print('view_lock', e)

    # 页面解锁
    def view_unlock(self):
        try:
            self.ui.pushButton_test.setText("测试")
            self.ui.algorithm_tableWidget.setEnabled(True)
            self.ui.pushButton_test.setEnabled(True)
            self.show_btn()
            self.ui.reset.setEnabled(True)
        except Exception as e:
            print('view_unlock', e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = modelTestView()
    view.show()
    sys.exit(app.exec_())
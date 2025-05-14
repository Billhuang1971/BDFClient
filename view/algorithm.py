import sys
from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
import re

from view.algorithm_form.train_parameter import Ui_train
from view.algorithm_form.parameter_1 import Ui_Parameter_1
from view.algorithm_form.form import Ui_AlogrithmForm
from view.algorithm_form.parameter import Ui_Parameter
from view.algorithm_form.file_upload import Ui_FileUpload
from PyQt5.QtWidgets import *


class algorithmView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AlogrithmForm()
        self.ui.setupUi(self)
        self.header = ['算法名称', '训练文件状态', '测试文件状态', '预测文件状态', '算法类型', '操作']
        self.select_row = None

    # 初始化算法管理主页面
    # def initTable(self, algorithm_info, on_train_alg_upload_btn_clicked, on_test_alg_upload_btn_clicked,
    #               on_predict_alg_upload_btn_clicked, show_parameter_setting):
    #     try:
    #         data = algorithm_info
    #         col_num = len(self.header)
    #         row_num = len(data)
    #         self.ui.tableWidget.setColumnCount(col_num)
    #         self.ui.tableWidget.setRowCount(row_num)
    #         # 设置表格高度
    #         for i in range(row_num):
    #             self.ui.tableWidget.setRowHeight(i, 55)
    #         for j in range(col_num - 1):
    #             self.ui.tableWidget.setColumnWidth(j, 200)
    #         self.ui.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
    #         self.ui.tableWidget.setHorizontalHeaderLabels(self.header)
    #         # 设置表头格式
    #         self.ui.tableWidget.horizontalHeader().setStyleSheet(
    #             '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
    #         # 使表格填满整个widget
    #         self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
    #
    #         for r in range(row_num):
    #             for c in range(col_num - 1):
    #                 if c == 0:
    #                     self.item = QTableWidgetItem(str(data[r][1]))
    #                     self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #                     font = self.item.font()
    #                     font.setPointSize(10)
    #                     self.item.setFont(font)
    #                     self.ui.tableWidget.setItem(r, c, self.item)
    #                 elif c == 1:
    #                     if data[r][4] == 'uploaded':
    #                         self.item = QTableWidgetItem('已上传')
    #                         self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #                         font = self.item.font()
    #                         font.setPointSize(10)
    #                         self.item.setFont(font)
    #                         self.ui.tableWidget.setItem(r, c, self.item)
    #                     else:
    #                         layout = QHBoxLayout()
    #                         self.ui.tableWidget.setCellWidget(r, c, QWidget())
    #                         uploadAlgorithmBtn = QPushButton('上传文件')
    #                         uploadAlgorithmBtn.clicked.connect(partial(on_train_alg_upload_btn_clicked, r))
    #                         uploadAlgorithmBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
    #                         uploadAlgorithmBtn.setCursor(Qt.PointingHandCursor)
    #                         layout.addWidget(uploadAlgorithmBtn)
    #                         layout.setStretch(0, 1)
    #                         self.ui.tableWidget.cellWidget(r, c).setLayout(layout)
    #                 elif c == 2:
    #                     if data[r][9] == 'uploaded':
    #                         self.item = QTableWidgetItem('已上传')
    #                         self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #                         font = self.item.font()
    #                         font.setPointSize(10)
    #                         self.item.setFont(font)
    #                         self.ui.tableWidget.setItem(r, c, self.item)
    #                     else:
    #                         layout = QHBoxLayout()
    #                         self.ui.tableWidget.setCellWidget(r, c, QWidget())
    #                         uploadAlgorithmBtn = QPushButton('上传文件')
    #                         uploadAlgorithmBtn.clicked.connect(partial(on_test_alg_upload_btn_clicked, r))
    #                         uploadAlgorithmBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
    #                         uploadAlgorithmBtn.setCursor(Qt.PointingHandCursor)
    #                         layout.addWidget(uploadAlgorithmBtn)
    #                         layout.setStretch(0, 1)
    #                         self.ui.tableWidget.cellWidget(r, c).setLayout(layout)
    #                 elif c == 3:
    #                     if data[r][14] == 'uploaded':
    #                         self.item = QTableWidgetItem('已上传')
    #                         self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #                         font = self.item.font()
    #                         font.setPointSize(10)
    #                         self.item.setFont(font)
    #                         self.ui.tableWidget.setItem(r, c, self.item)
    #                     else:
    #                         layout = QHBoxLayout()
    #                         self.ui.tableWidget.setCellWidget(r, c, QWidget())
    #                         uploadAlgorithmBtn = QPushButton('上传文件')
    #                         uploadAlgorithmBtn.clicked.connect(partial(on_predict_alg_upload_btn_clicked, r))
    #                         uploadAlgorithmBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
    #                         uploadAlgorithmBtn.setCursor(Qt.PointingHandCursor)
    #                         layout.addWidget(uploadAlgorithmBtn)
    #                         layout.setStretch(0, 1)
    #                         self.ui.tableWidget.cellWidget(r, c).setLayout(layout)
    #                 elif c == 4:
    #                     cur_algorithm_type = data[r][17]
    #                     if cur_algorithm_type == 'waveform':
    #                         self.item = QTableWidgetItem('波形标注算法')
    #                         self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #                         font = self.item.font()
    #                         font.setPointSize(10)
    #                         self.item.setFont(font)
    #                         self.ui.tableWidget.setItem(r, c, self.item)
    #                     else:
    #                         self.item = QTableWidgetItem('状态标注算法')
    #                         self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #                         font = self.item.font()
    #                         font.setPointSize(10)
    #                         self.item.setFont(font)
    #                         self.ui.tableWidget.setItem(r, c, self.item)
    #             layout = QHBoxLayout()
    #             self.ui.tableWidget.setCellWidget(r, col_num - 1, QWidget())
    #             showSettingBtn = QPushButton('查看参数设置')
    #             showSettingBtn.clicked.connect(partial(show_parameter_setting, r))
    #             showSettingBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
    #             showSettingBtn.setCursor(Qt.PointingHandCursor)
    #             layout.addWidget(showSettingBtn)
    #             layout.setStretch(0, 1)
    #             self.ui.tableWidget.cellWidget(r, col_num - 1).setLayout(layout)
    #         self.ui.tableWidget.horizontalHeader().setHighlightSections(False)
    #         # 按字段长度进行填充
    #         # self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    #         self.ui.tableWidget.itemClicked.connect(self.set_selectRow)
    #         # 只能选中一行
    #         # self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
    #         self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #     except Exception as e:
    #         print('initTable', e)

    # def set_selectRow(self, item):
    #     self.select_row = item.row()

    def reject(self):
        pass

class Parameter_view(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Parameter_1()
        self.ui.setupUi(self)

class train_parameter_view(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_train()
        self.ui.setupUi(self)

class FileUploadView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_FileUpload()
        self.ui.setupUi(self)

class ParameterView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Parameter()
        self.ui.setupUi(self)

class TableWidget(QWidget):
    control_signal = pyqtSignal(list)

    def __init__(self, algorithm_info, current_page,
                 on_train_alg_upload_btn_clicked, on_test_alg_upload_btn_clicked,
                 on_predict_alg_upload_btn_clicked, show_parameter_setting, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        self.header = ['算法名称', '训练文件状态', '测试文件状态', '预测文件状态', '算法类型', '操作']
        self.cur_page = current_page
        self.table = QTableWidget()
        self.select_row = None
        self.init_table(algorithm_info, on_train_alg_upload_btn_clicked, on_test_alg_upload_btn_clicked,
                        on_predict_alg_upload_btn_clicked, show_parameter_setting)

    def init_table(self, algorithm_info, on_train_alg_upload_btn_clicked, on_test_alg_upload_btn_clicked,
                  on_predict_alg_upload_btn_clicked, show_parameter_setting):
        style_sheet = """
            QTableWidget {
                border: 1px solid blue;
                background-color:rgb(255,255,255)
            }
            QPushButton{
                max-width: 30ex;
                max-height: 12ex;
                font-size: 14px;
            }
            QLineEdit{
                max-width: 30px
            }
        """
        try:
            data = algorithm_info
            col_num = len(self.header)
            row_num = len(data)
            self.table.setColumnCount(col_num)
            self.table.setRowCount(row_num)
            # 设置表格高度
            for i in range(row_num):
                self.table.setRowHeight(i, 55)
            for j in range(col_num - 1):
                self.table.setColumnWidth(j, 200)
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.table.setHorizontalHeaderLabels(self.header)
            # 设置表头格式
            self.table.horizontalHeader().setStyleSheet(
                '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
            # 使表格填满整个widget
            self.table.horizontalHeader().setStretchLastSection(True)

            for r in range(row_num):
                for c in range(col_num - 1):
                    if c == 0:
                        self.item = QTableWidgetItem(str(data[r][1]))
                        self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        font = self.item.font()
                        font.setPointSize(10)
                        self.item.setFont(font)
                        self.table.setItem(r, c, self.item)
                    elif c == 1:
                        if data[r][4] == 'uploaded':
                            self.item = QTableWidgetItem('已上传')
                            self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = self.item.font()
                            font.setPointSize(10)
                            self.item.setFont(font)
                            self.table.setItem(r, c, self.item)
                        else:
                            layout = QHBoxLayout()
                            self.table.setCellWidget(r, c, QWidget())
                            uploadAlgorithmBtn = QPushButton('上传文件')
                            uploadAlgorithmBtn.clicked.connect(partial(on_train_alg_upload_btn_clicked, r))
                            uploadAlgorithmBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                            uploadAlgorithmBtn.setCursor(Qt.PointingHandCursor)
                            layout.addWidget(uploadAlgorithmBtn)
                            layout.setStretch(0, 1)
                            self.table.cellWidget(r, c).setLayout(layout)
                    elif c == 2:
                        if data[r][9] == 'uploaded':
                            self.item = QTableWidgetItem('已上传')
                            self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = self.item.font()
                            font.setPointSize(10)
                            self.item.setFont(font)
                            self.table.setItem(r, c, self.item)
                        else:
                            layout = QHBoxLayout()
                            self.table.setCellWidget(r, c, QWidget())
                            uploadAlgorithmBtn = QPushButton('上传文件')
                            uploadAlgorithmBtn.clicked.connect(partial(on_test_alg_upload_btn_clicked, r))
                            uploadAlgorithmBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                            uploadAlgorithmBtn.setCursor(Qt.PointingHandCursor)
                            layout.addWidget(uploadAlgorithmBtn)
                            layout.setStretch(0, 1)
                            self.table.cellWidget(r, c).setLayout(layout)
                    elif c == 3:
                        if data[r][14] == 'uploaded':
                            self.item = QTableWidgetItem('已上传')
                            self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = self.item.font()
                            font.setPointSize(10)
                            self.item.setFont(font)
                            self.table.setItem(r, c, self.item)
                        else:
                            layout = QHBoxLayout()
                            self.table.setCellWidget(r, c, QWidget())
                            uploadAlgorithmBtn = QPushButton('上传文件')
                            uploadAlgorithmBtn.clicked.connect(partial(on_predict_alg_upload_btn_clicked, r))
                            uploadAlgorithmBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                            uploadAlgorithmBtn.setCursor(Qt.PointingHandCursor)
                            layout.addWidget(uploadAlgorithmBtn)
                            layout.setStretch(0, 1)
                            self.table.cellWidget(r, c).setLayout(layout)
                    elif c == 4:
                        cur_algorithm_type = data[r][17]
                        if cur_algorithm_type == 'waveform':
                            self.item = QTableWidgetItem('波形标注算法')
                            self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = self.item.font()
                            font.setPointSize(10)
                            self.item.setFont(font)
                            self.table.setItem(r, c, self.item)
                        else:
                            self.item = QTableWidgetItem('状态标注算法')
                            self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            font = self.item.font()
                            font.setPointSize(10)
                            self.item.setFont(font)
                            self.table.setItem(r, c, self.item)
                layout = QHBoxLayout()
                self.table.setCellWidget(r, col_num - 1, QWidget())
                showSettingBtn = QPushButton('查看参数设置')
                showSettingBtn.clicked.connect(partial(show_parameter_setting, r))
                showSettingBtn.setStyleSheet('height : 50px;font : 18px;color:blue')
                showSettingBtn.setCursor(Qt.PointingHandCursor)
                layout.addWidget(showSettingBtn)
                layout.setStretch(0, 1)
                self.table.cellWidget(r, col_num - 1).setLayout(layout)
            self.table.horizontalHeader().setHighlightSections(False)
            # 按字段长度进行填充
            # self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.table.itemClicked.connect(self.set_selectRow)
            # 只能选中一行
            # self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.__layout = QVBoxLayout()
            self.__layout.addWidget(self.table)
            self.setLayout(self.__layout)
            self.setStyleSheet(style_sheet)
        except Exception as e:
            print('initTable', e)


    def setPageController(self, page):
        """自定义页码控制器"""
        control_layout = QHBoxLayout()
        homePage = QPushButton("首页")
        prePage = QPushButton("<上一页")
        self.curPage = QLabel(str(self.cur_page))
        nextPage = QPushButton("下一页>")
        finalPage = QPushButton("尾页")
        self.totalPage = QLabel("共" + str(page) + "页")
        skipLable_0 = QLabel("跳到")
        self.skipPage = QLineEdit()
        skipLabel_1 = QLabel("页")
        confirmSkip = QPushButton("确定")
        homePage.clicked.connect(self.__home_page)
        prePage.clicked.connect(self.__pre_page)
        nextPage.clicked.connect(self.__next_page)
        finalPage.clicked.connect(self.__final_page)
        confirmSkip.clicked.connect(self.__confirm_skip)
        control_layout.addStretch(1)
        control_layout.addWidget(homePage)
        control_layout.addWidget(prePage)
        control_layout.addWidget(self.curPage)
        control_layout.addWidget(nextPage)
        control_layout.addWidget(finalPage)
        control_layout.addWidget(self.totalPage)
        control_layout.addWidget(skipLable_0)
        control_layout.addWidget(self.skipPage)
        control_layout.addWidget(skipLabel_1)
        control_layout.addWidget(confirmSkip)
        control_layout.addStretch(1)
        self.__layout.addLayout(control_layout)
        # self.__layout.setStretch(0, 12)
        # self.__layout.setStretch(1, 1)

    def __home_page(self):
        """点击首页信号"""
        self.control_signal.emit(["home", self.curPage.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.control_signal.emit(["pre", self.curPage.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.control_signal.emit(["next", self.curPage.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.control_signal.emit(["final", self.curPage.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.control_signal.emit(["confirm", self.skipPage.text()])

    def showTotalPage(self):
        """返回当前总页数"""
        return int(self.totalPage.text()[1:-1])

    def set_selectRow(self, item):
        self.select_row = item.row()

# 语法高亮器
class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # 关键字
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'None', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
            'True', 'try', 'while', 'with', 'yield'
        ]

        self.highlighting_rules = [(re.compile(r'\b' + kw + r'\b'), keyword_format) for kw in keywords]

        # 字符串
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        self.highlighting_rules.append((re.compile(r'".*?"'), string_format))
        self.highlighting_rules.append((re.compile(r"'.*?'"), string_format))

        # 注释
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((re.compile(r'#.*'), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.start(), match.end()
                self.setFormat(start, end - start, fmt)

class AlgTemplate(QDialog):
    def __init__(self, download_template):
        super().__init__()
        self.setWindowTitle("算法模板")
        self.resize(1200, 1000)

        self.main_layout = QVBoxLayout()

        # 顶部布局：右上角放复制按钮
        top_layout = QHBoxLayout()
        top_layout.addStretch()  # 左边留空
        self.copy_button = QPushButton("复制")
        self.copy_button.clicked.connect(self.copy_current_tab)
        self.download_button = QPushButton("下载")
        self.download_button.clicked.connect(download_template)
        top_layout.addWidget(self.copy_button)
        top_layout.addWidget(self.download_button)


        self.tabs = QTabWidget()

        # 页面1
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout()
        self.editor1 = QPlainTextEdit()
        self.editor1.setReadOnly(True)
        self.editor1.setFont(QFont("Consolas", 11))
        self.tab1_layout.addWidget(self.editor1)
        self.tab1.setLayout(self.tab1_layout)

        # 页面2
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout()
        self.editor2 = QPlainTextEdit()
        self.editor2.setReadOnly(True)
        self.editor2.setFont(QFont("Consolas", 11))
        self.tab2_layout.addWidget(self.editor2)
        self.tab2.setLayout(self.tab2_layout)

        # 页面3
        self.tab3 = QWidget()
        self.tab3_layout = QVBoxLayout()
        self.editor3 = QPlainTextEdit()
        self.editor3.setReadOnly(True)
        self.editor3.setFont(QFont("Consolas", 11))
        self.tab3_layout.addWidget(self.editor3)
        self.tab3.setLayout(self.tab3_layout)

        self.highlighter1 = PythonHighlighter(self.editor1.document())
        self.highlighter2 = PythonHighlighter(self.editor2.document())
        self.highlighter3 = PythonHighlighter(self.editor3.document())

        self.tabs.addTab(self.tab1, "训练算法")
        self.tabs.addTab(self.tab2, "测试算法")
        self.tabs.addTab(self.tab3, "预测算法")

        self.main_layout.addLayout(top_layout)
        self.main_layout.addWidget(self.tabs)
        self.setLayout(self.main_layout)

    def setContents(self, train_alg, test_alg, predict_alg):
        self.editor1.setPlainText(train_alg)
        self.editor2.setPlainText(test_alg)
        self.editor3.setPlainText(predict_alg)

    def copy_current_tab(self):
        current_index = self.tabs.currentIndex()
        if current_index == 0:
            text = self.editor1.toPlainText()
        elif current_index == 1:
            text = self.editor2.toPlainText()
        elif current_index == 2:
            text = self.editor3.toPlainText()
        else:
            text = ""

        clipboard = QApplication.clipboard()
        clipboard.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = algorithmView()
    view.show()
    sys.exit(app.exec_())

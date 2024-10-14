from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt
from view.classifer_form.form import Ui_ClassifierForm
from view.classifer_form.Parameter import Ui_model_import
from view.classifer_form.algorithm_table import Ui_algorithm_table
from view.classifer_form.label_select import Ui_label_select
from view.classifer_form.prentry import Ui_Prentry
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal


class ClassifierView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ClassifierForm()
        self.ui.setupUi(self)
        self.header = ['分类器模型名称', '算法名称', '数据集名称', '训练性能', '测试性能']
        self.field = ['classifier_name', 'alg_name', 'set_name', 'train_performance', 'test_performance']

    # def initTable(self, data):
    #     col_num = len(self.header)
    #     row_num = len(data)
    #     self.ui.tableWidget.setColumnCount(col_num)
    #     self.ui.tableWidget.setRowCount(row_num)
    #     for i in range(col_num):
    #         header_item = QTableWidgetItem(self.header[i])
    #         font = header_item.font()
    #         font.setPointSize(16)
    #         header_item.setFont(font)
    #         header_item.setForeground(QBrush(Qt.black))
    #         header_item.setData(Qt.UserRole, self.field[i])
    #         self.ui.tableWidget.setHorizontalHeaderItem(i, header_item)
    #         # 拉伸表格列项，使其铺满
    #         self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
    #
    #     for r in range(row_num):
    #         for c in range(col_num):
    #             self.item = QTableWidgetItem(str(data[r][c]))
    #             self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #             font = self.item.font()
    #             font.setPointSize(10)
    #             self.item.setFont(font)
    #             self.ui.tableWidget.setItem(r, c, self.item)
    #     self.ui.tableWidget.horizontalHeader().setHighlightSections(False)
    #     #   按字段长度进行填充
    #     self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    #     # 增加和查询的时候列数会改变，所以需要保存原来的列数
    #     self.col = self.ui.tableWidget.columnCount()

    def reject(self):
        pass
class TableWidget(QWidget):
    control_signal=pyqtSignal(list)
    def __init__(self,data,current_page,*args,**kwargs):
        super(TableWidget,self).__init__(*args,**kwargs)
        self.header = ['分类器模型名称', '算法名称', '数据集名称', '训练性能', '测试性能']
        self.field = ['classifier_name', 'alg_name', 'set_name', 'train_performance', 'test_performance']
        self.cur_page=current_page
        self.table=QTableWidget()
        self.init_table(data)
    def init_table(self, data):
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
            col_num = len(self.header)
            row_num = len(data)
            self.table.setColumnCount(col_num)
            self.table.setRowCount(row_num)
            self.table.setInputMethodHints(Qt.ImhHiddenText)
            # 设置表格高度
            for i in range(row_num):
                self.table.setRowHeight(i, 45)
            # 设置除最后一列之外的列的宽度
            for i in range(0, col_num - 1):
                self.table.setColumnWidth(i, 150)

            for i in range(col_num):
                header_item = QTableWidgetItem(self.header[i])
                font = header_item.font()
                font.setPointSize(16)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                header_item.setData(Qt.UserRole, self.field[i])
                self.table.setHorizontalHeaderItem(i, header_item)
                # 拉伸表格列项，使其铺满
                self.table.horizontalHeader().setStretchLastSection(True)


            for r in range(row_num):
                for c in range(col_num):
                    self.item = QTableWidgetItem(str(data[r][c]))
                    self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    font = self.item.font()
                    font.setPointSize(10)
                    self.item.setFont(font)

                    self.table.setItem(r, c, self.item)
            self.table.horizontalHeader().setHighlightSections(False)
            #   按字段长度进行填充
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

            # 增加和查询的时候列数会改变，所以需要保存原来的列数
            self.col = self.table.columnCount()
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




class ImportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_model_import()
        self.ui.setupUi(self)
        self.saved_EEG_names = []
        self.ui.pushButton_label_select.setEnabled(False)
        self.ui.checkbox1.stateChanged.connect(self.handle_checkbox_state_change)
    def handle_checkbox_state_change(self, state):
        self.ui.pushButton_label_select.setEnabled(state)

class AlgorithmSelectView(QWidget):
    control_signal_al = pyqtSignal(list)
    def __init__(self,current_page, parent=None):
        super().__init__(parent)
        self.ui = Ui_algorithm_table()
        self.ui.setupUi(self)
        self.cur_page=current_page
        self.control_layout_tempt=None
    def updatepage(self,current_page):
        self.cur_page=current_page
    def setPageController_al(self, page):
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
        homePage.clicked.connect(self.__home_page_al)
        prePage.clicked.connect(self.__pre_page_al)
        nextPage.clicked.connect(self.__next_page_al)
        finalPage.clicked.connect(self.__final_page_al)
        confirmSkip.clicked.connect(self.__confirm_skip_al)
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
        self.control_layout_tempt=control_layout
        self.ui.verticalLayout.addLayout(control_layout)
        # self.__layout.setStretch(0, 12)
        # self.__layout.setStretch(1, 1)

    def __home_page_al(self):
        """点击首页信号"""
        self.control_signal_al.emit(["home", self.curPage.text()])

    def __pre_page_al(self):
        """点击上一页信号"""
        self.control_signal_al.emit(["pre", self.curPage.text()])

    def __next_page_al(self):
        """点击下一页信号"""
        self.control_signal_al.emit(["next", self.curPage.text()])

    def __final_page_al(self):
        """尾页点击信号"""
        self.control_signal_al.emit(["final", self.curPage.text()])

    def __confirm_skip_al(self):
        """跳转页码确定"""
        self.control_signal_al.emit(["confirm", self.skipPage.text()])

    def showTotalPage_al(self):
        """返回当前总页数"""
        return int(self.totalPage.text()[1:-1])

class LabelSelectVew(QWidget):
    signal_save_label_names = pyqtSignal(list)
    def __init__(self, EEG_lead, saved_EEG_names,parent=None):
        super().__init__(parent)
        self.ui = Ui_label_select()
        self.ui.setupUi(self)
        # 用户点击保存时，已经选中的分类标签
        self.saved_EEG_names = saved_EEG_names
        self.EEG_lead = EEG_lead
        self.EEG_names = []
        for name in EEG_lead:
            self.EEG_names.append(name)
        self.init_view()
        self.ui.pushButton_save.clicked.connect(self.onClicked_pushButton_save)
        self.ui.labelType_listWidget.itemDoubleClicked.connect(self.itemDoubleClicked_EEG_listWidget)
        self.ui.selected_listWidget.itemDoubleClicked.connect(self.itemDoubleClicked_selected_listWidget)
        self.show()

    def init_view(self):
        # 第一次开启
        self.init_labelType_listWidget(self.EEG_names)
        self.init_selected_listWidget()

    # 初始化标注信息列表
    def init_labelType_listWidget(self, EEG_names):
        self.ui.labelType_listWidget.clear()
        if len(EEG_names) > 0:
            for names in EEG_names:
                item = QListWidgetItem(names)
                self.ui.labelType_listWidget.addItem(item)

    # 初始化被选中标注信息列表
    def init_selected_listWidget(self):
        self.ui.selected_listWidget.clear()
        if len(self.saved_EEG_names) > 0:
            for names in self.saved_EEG_names:
                item = QListWidgetItem(names)
                self.ui.selected_listWidget.addItem(item)
    # 获得选中标签
    def get_classifier_label_types(self):
        return self.saved_EEG_names

    def itemDoubleClicked_selected_listWidget(self, item):
        selected_EEG_names = []
        item_count = self.ui.selected_listWidget.count()
        # 按顺序获取每个选项
        for i in range(item_count):
            a = self.ui.selected_listWidget.item(i)
            selected_EEG_names.append(a.text())
        if item.text() in selected_EEG_names:
            self.ui.selected_listWidget.takeItem(self.ui.selected_listWidget.row(item))
            return

    def itemDoubleClicked_EEG_listWidget(self, item):
        selected_EEG_names = []
        item_count = self.ui.selected_listWidget.count()
        # 按顺序获取每个选项
        for i in range(item_count):
            a = self.ui.selected_listWidget.item(i)
            selected_EEG_names.append(a.text())
        text = item.text()
        if text in selected_EEG_names:
            return
        item_clone = QListWidgetItem(item.text())
        # self.ui.selected_listWidget.takeItem(self.ui.selected_listWidget.row(item))
        self.ui.selected_listWidget.addItem(item_clone)

    def onClicked_pushButton_save(self):
        # 获取选项的数量
        item_count = self.ui.selected_listWidget.count()
        selected_EEG_names = []
        # 按顺序获取每个选项
        for i in range(item_count):
            item = self.ui.selected_listWidget.item(i)
            selected_EEG_names.append(item.text())
        self.saved_EEG_names = selected_EEG_names
        self.signal_save_label_names.emit(selected_EEG_names)
        self.close()
class PrentryView(QWidget):
    signal_save_configID_names = pyqtSignal(str)
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_Prentry()
        self.ui.setupUi(self)


if __name__ == '__main__':
    pass


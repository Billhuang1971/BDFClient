from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from view.classifer_form.Ui_classifier import Ui_ClassifierForm
from view.classifer_form.Ui_clsimport import Ui_clsimportForm
from view.classifer_form.Ui_algorithmSelect import Ui_algorithmSelectForm
from view.classifer_form.Ui_labelSelect import Ui_labelSelectForm
from view.classifer_form.Ui_clsPrentry import Ui_clsPrentryForm
from view.classifer_form.Ui_setselect import Ui_setselectForm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
import json
import os
class CustomDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(message)
        font =QFont()
        font.setPointSize(16)
        label.setFont(font)
        layout.addWidget(label)
        self.setWindowTitle("更多信息")
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        self.resize(200, 100)
        self.setLayout(layout)

class ClassifierView(QWidget):
    control_signal = pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ClassifierForm()
        self.ui.setupUi(self)
        self.header = ['分类器模型名称', '算法名称', '数据集名称','扫描段长','数据单位','分类任务','更多信息']
        self.field = ['classifier_name', 'alg_name', 'set_name', 'epoch_lenth','classifierUnit','type','more']
        self.table = QTableWidget()
        self.cur_page=0
        self.state_select_name=None
        self.ui.btngroup1.buttonClicked.connect(self.single_select)
    def single_select(self):
        state_select=self.ui.btngroup1.checkedButton()
        self.state_select_name=state_select.text()
        print(self.state_select_name)
    def clear_select(self):
        self.ui.btngroup1.setExclusive(False)
        self.ui.built_btn.setChecked(False)
        self.ui.ready_btn.setChecked(False)
        self.ui.uploaded_btn.setChecked(False)
        self.ui.btngroup1.setExclusive(True)

    def initTable(self, data,curPageIndex):
        self.cur_page = curPageIndex
        self.style_sheet = """
                           QTableWidget {
                               border: 1px solid blue;
                               background-color:rgb(255,255,255)
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
                self.table.setRowHeight(i, 50)
            # 设置除最后一列之外的列的宽度
            for i in range(0, col_num-1):
                self.table.setColumnWidth(i, 170)
            for i in range(col_num):
                header_item = QTableWidgetItem(self.header[i])
                font = header_item.font()
                font.setPixelSize(18)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                header_item.setData(Qt.UserRole, self.field[i])
                self.table.setHorizontalHeaderItem(i, header_item)
                # 拉伸表格列项，使其铺满
                self.table.horizontalHeader().setStretchLastSection(True)

            for r in range(row_num):
                for c in range(col_num):
                    if c < col_num-2:
                        self.item = QTableWidgetItem(str(data[r][c]))
                        self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        font = self.item.font()
                        font.setPixelSize(16)
                        self.item.setFont(font)
                        self.table.setItem(r, c, self.item)
                    elif c ==col_num-1:
                        button = QPushButton("查看更多参数")
                        font = button.font()
                        font.setPixelSize(18)
                        button.setFont(font)
                        button.setStyleSheet("color: blue;")
                        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                        button.clicked.connect(lambda _, para_channels=data[r][c],para_train=data[r][c+1],para_test=data[r][c+2]: self.show_custom_message(para_channels,para_train, para_test))
                        button_widget = QWidget()
                        button_layout = QHBoxLayout(button_widget)
                        button_layout.addWidget(button)
                        button_layout.setContentsMargins(0, 0, 0, 0)  # 移除按钮与单元格边框的间距
                        button_layout.setSpacing(0)  # 去除子部件之间的间距
                        # 设置 QWidget 为单元格内容
                        self.table.setCellWidget(r, c, button_widget)
                        #self.table.setCellWidget(r, c, button)

            self.table.horizontalHeader().setHighlightSections(False)
            #   按字段长度进行填充
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

            self.table.setSelectionBehavior(QTableWidget.SelectRows)#设置选中一行

            # 增加和查询的时候列数会改变，所以需要保存原来的列数
            self.col = self.table.columnCount()
            self.ui.verticalLayout_2.addWidget(self.table)
            self.setStyleSheet(self.style_sheet)
        except Exception as e:
            print('initTable', e)

    def show_custom_message(self, para_channels,para_train, para_test):
        custom_message = (f"训练性能参数： {para_train}, 测试性能参数:{para_test}\n"
                          f"通道列表：{para_channels}")
        dialog = CustomDialog(custom_message)
        dialog.exec_()
    def update_table(self,data,curPageIndex,curpagemax=''):

        self.cur_page = curPageIndex
        self.curPage.setText(str(curPageIndex))
        if curpagemax !='':
            self.totalPage.setText("共" + str(curpagemax) + "页")
        col_num = len(self.header)
        row_num = len(data)
        row_max=12
        for r in range(row_max):
            self.table.removeRow(r)
        self.table.setColumnCount(col_num)
        self.table.setRowCount(row_num)
        self.table.setInputMethodHints(Qt.ImhHiddenText)
        for i in range(row_num):
            self.table.setRowHeight(i, 45)
        # 设置除最后一列之外的列的宽度
        for i in range(0, col_num - 1):
            self.table.setColumnWidth(i, 150)

        for i in range(col_num):
            header_item = QTableWidgetItem(self.header[i])
            font = header_item.font()
            font.setPixelSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, self.field[i])
            self.table.setHorizontalHeaderItem(i, header_item)
            # 拉伸表格列项，使其铺满
            self.table.horizontalHeader().setStretchLastSection(True)

        for r in range(row_num):
            for c in range(col_num):
                if c < col_num - 1:
                    self.item = QTableWidgetItem(str(data[r][c]))
                    self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    font = self.item.font()
                    font.setPixelSize(12)
                    self.item.setFont(font)
                    self.table.setItem(r, c, self.item)
                else:
                    button = QPushButton("查看更多参数")
                    font = button.font()
                    font.setPixelSize(20)
                    button.setFont(font)
                    button.setStyleSheet("color: blue;")
                    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    button.clicked.connect(lambda _, para_channels=data[r][c], para_train=data[r][c + 1],
                                                  para_test=data[r][c + 2]: self.show_custom_message(para_channels,
                                                                                                     para_train,
                                                                                                     para_test))
                    button_widget = QWidget()
                    button_layout = QHBoxLayout(button_widget)
                    button_layout.addWidget(button)
                    button_layout.setContentsMargins(0, 0, 0, 0)  # 移除按钮与单元格边框的间距
                    button_layout.setSpacing(0)  # 去除子部件之间的间距
                    self.table.setCellWidget(r, c, button_widget)

        self.table.horizontalHeader().setHighlightSections(False)

        #   按字段长度进行填充
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.setStyleSheet(self.style_sheet)
    def reject(self):
        pass
    def setPageController(self, page):
        """自定义页码控制器"""
        control_layout = QHBoxLayout()
        font = QFont()
        font.setFamily("Arial")
        font.setPixelSize(16)
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
        homePage.setFont(font)
        prePage.setFont(font)
        self.curPage.setFont(font)
        nextPage.setFont(font)
        finalPage.setFont(font)
        self.totalPage.setFont(font)
        skipLable_0.setFont(font)
        skipLabel_1.setFont(font)
        confirmSkip.setFont(font)
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
        self.ui.verticalLayout.addLayout(control_layout)
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
class clsimportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_clsimportForm()
        self.ui.setupUi(self)
        self.saved_EEG_names = []
        self.ui.pushButton_label_select.setEnabled(False)
        self.ui.checkbox1.stateChanged.connect(self.handle_checkbox_state_change)
        self.algorithm=None
        self.set=None
    def handle_checkbox_state_change(self, state):
        self.ui.pushButton_label_select.setEnabled(state)
    def init_algorithm(self,data,curPageIndex_al,curPageMax_al):
        self.algorithm=AlgorithmSelectView(curPageIndex_al)
        self.algorithm.initTable(data,curPageIndex_al)
        self.algorithm.setPageController_al(curPageMax_al)
    def init_set(self,data,curPageIndex_set,curPageMax_set):
        self.set = SetSelectView(curPageIndex_set)
        self.set.initTable(data, curPageIndex_set)
        self.set.setPageController_set(curPageMax_set)
class AlgorithmSelectView(QWidget):
    control_signal_al = pyqtSignal(list)
    def __init__(self,current_page,parent=None):
        super().__init__(parent)
        self.ui = Ui_algorithmSelectForm()
        self.ui.setupUi(self)
        self.header = ['算法名称']
        self.field = [ 'alg_name']
        self.cur_page = 0
        # self.header = [ '算法名称']
        # self.field = ['alg_name']
        # self.table = QTableWidget()
        # self.init_table(data)
    def initTable(self, data,curPageIndex):
        self.cur_page = curPageIndex
        try:
            col_num = len(self.header)
            row_num = len(data)
            self.ui.tableWidget_algorithm.setColumnCount(col_num)
            self.ui.tableWidget_algorithm.setRowCount(row_num)
            self.ui.tableWidget_algorithm.setInputMethodHints(Qt.ImhHiddenText)
            # 设置表格高度
            for i in range(row_num):
                self.ui.tableWidget_algorithm.setRowHeight(i, 45)
            # 设置除最后一列之外的列的宽度
            for i in range(0, col_num - 1):
                self.ui.tableWidget_algorithm.setColumnWidth(i, 150)

            for i in range(col_num):
                header_item = QTableWidgetItem(self.header[i])
                font = header_item.font()
                font.setPointSize(16)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                header_item.setData(Qt.UserRole, self.field[i])
                self.ui.tableWidget_algorithm.setHorizontalHeaderItem(i, header_item)
                # 拉伸表格列项，使其铺满
                self.ui.tableWidget_algorithm.horizontalHeader().setStretchLastSection(True)

            for r in range(row_num):
                for c in range(col_num):
                    self.item = QTableWidgetItem(str(data[r][c+1]))
                    self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    font = self.item.font()
                    font.setPointSize(10)
                    self.item.setFont(font)

                    self.ui.tableWidget_algorithm.setItem(r, c, self.item)
            self.ui.tableWidget_algorithm.horizontalHeader().setHighlightSections(False)
            #   按字段长度进行填充
            self.ui.tableWidget_algorithm.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.tableWidget_algorithm.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

            # 增加和查询的时候列数会改变，所以需要保存原来的列数
            self.col = self.ui.tableWidget_algorithm.columnCount()
        except Exception as e:
            print('initTable', e)
    def update_table(self,data,curPageIndex,curpagemax=''):

        self.cur_page = curPageIndex
        self.curPage.setText(str(curPageIndex))
        if curpagemax !='':
            self.totalPage.setText("共" + str(curpagemax) + "页")
        col_num = len(self.header)
        row_num = len(data)
        row_max=12
        for r in range(row_max):
            self.ui.tableWidget_algorithm.removeRow(r)
        self.ui.tableWidget_algorithm.setColumnCount(col_num)
        self.ui.tableWidget_algorithm.setRowCount(row_num)
        self.ui.tableWidget_algorithm.setInputMethodHints(Qt.ImhHiddenText)
        for i in range(row_num):
            self.ui.tableWidget_algorithm.setRowHeight(i, 45)
        # 设置除最后一列之外的列的宽度
        for i in range(0, col_num - 1):
            self.ui.tableWidget_algorithm.setColumnWidth(i, 150)

        for i in range(col_num):
            header_item = QTableWidgetItem(self.header[i])
            font = header_item.font()
            font.setPointSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, self.field[i])
            self.ui.tableWidget_algorithm.setHorizontalHeaderItem(i, header_item)
            # 拉伸表格列项，使其铺满
            self.ui.tableWidget_algorithm.horizontalHeader().setStretchLastSection(True)

        for r in range(row_num):
            for c in range(col_num):
                self.item = QTableWidgetItem(str(data[r][c+1]))
                self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                font = self.item.font()
                font.setPointSize(10)
                self.item.setFont(font)

                self.ui.tableWidget_algorithm.setItem(r, c, self.item)
        self.ui.tableWidget_algorithm.horizontalHeader().setHighlightSections(False)

        #   按字段长度进行填充
        self.ui.tableWidget_algorithm.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableWidget_algorithm.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
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
    signal_config_save=pyqtSignal(list)
    def __init__(self, EEG_lead, saved_EEG_names,parent=None):
        super().__init__(parent)
        self.ui = Ui_labelSelectForm()
        self.ui.setupUi(self)
        # 用户点击保存时，已经选中的分类标签
        self.saved_EEG_names = saved_EEG_names
        self.EEG_lead = EEG_lead
        self.EEG_names = []
        self.REF_channel=None #存储当前参考通道
        for name in EEG_lead:
            self.EEG_names.append(name)
        self.init_view()
        self.ui.pushButton_save.clicked.connect(self.onClicked_pushButton_save)
        self.ui.labelType_listWidget.itemDoubleClicked.connect(self.itemDoubleClicked_EEG_listWidget)  # 标签列表
        self.ui.REF_listWidget.itemClicked.connect(self.itemclicked_REF_listWidget)
        self.ui.selected_listWidget.itemDoubleClicked.connect(self.itemDoubleClicked_selected_listWidget)  # 选中表格
        self.ui.save_config.clicked.connect(self.save_configs)
        self.ui.load_config.clicked.connect(self.load_configs)
        self.ui.delete_config.clicked.connect(self.delete_config)
        self.ui.clear_select.clicked.connect(self.ui.selected_listWidget.clear)
        self.init_config()
        self.show()

    def init_view(self):
        # 第一次开启
        self.init_labelType_listWidget(self.EEG_names)
        self.init_selected_listWidget()

    # 初始化标注信息列表
    def init_labelType_listWidget(self, EEG_names):
        self.ui.REF_listWidget.clear()
        self.ui.labelType_listWidget.clear()
        if len(EEG_names) > 0:
            for names in EEG_names:
                item = QListWidgetItem(names)
                self.ui.labelType_listWidget.addItem(item)

        if len(EEG_names) >0:
            tempt = QListWidgetItem('-REF')
            self.ui.REF_listWidget.addItem(tempt)
            for names in EEG_names:
                item = QListWidgetItem('-'+names)
                self.ui.REF_listWidget.addItem(item) #初始化参考通道



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
    def init_config(self):
        """
            读取JSON配置文件并填充到下拉框
            """
        # 获取当前脚本的绝对路径，并定位上一级目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)  # 上一级目录
        config_path = os.path.join(parent_dir, "model", "uploadmodel_config.json")
        try:
            # 1. 检查文件是否存在
            if not os.path.exists(config_path):
                # 创建空配置文件
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)
                return  # 新创建空文件，无需填充下拉框
            # 2. 读取JSON文件
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            # 3. 获取配置名称并填充下拉框
            config_names = list(config_data.keys())
            # 4. 清空现有下拉框选项
            self.ui.config_combo.clear()
            # 5. 添加配置名称到下拉框
            if config_names:
                self.ui.config_combo.addItems(config_names)
            else:
                QMessageBox.information(self, "提示", "配置文件中没有保存的配置")
        except json.JSONDecodeError:
            QMessageBox.warning(self, "错误", "配置文件格式错误，请检查文件内容")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载配置失败: {str(e)}")
    def save_configs(self):
        config_name, ok = QInputDialog.getText(
            self,  # 父窗口
            "保存配置",  # 对话框标题
            "请输入配置名称："  # 提示文本
        )
        # 2. 检查用户是否确认输入
        if not ok or not config_name.strip():
            return  # 用户取消或输入为空时退出
        # 获取选项的数量
        item_count = self.ui.selected_listWidget.count()
        selected_EEG_names = []
        # 按顺序获取每个选项
        for i in range(item_count):
            item = self.ui.selected_listWidget.item(i)
            selected_EEG_names.append(item.text())
        # 3. 设置存储路径（相对路径）
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)  # 上一级目录
        config_path = os.path.join(parent_dir, "model", "uploadmodel_config.json")
        config_data = {}
        if os.path.exists(config_path):
            try:
                # 文件存在时加载现有配置
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            except json.JSONDecodeError:
                # 处理空文件或格式错误
                QMessageBox.warning(self, "警告", "配置文件格式错误，将创建新配置")
            except Exception as e:
                QMessageBox.warning(self, "警告", f"配置文件读取错误: {str(e)}")
        else:
            try:
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"创建配置文件失败: {str(e)}")
                return
            # 5. 检查配置名称是否已存在
        if config_name in config_data:
            reply = QMessageBox.question(
                self, "配置已存在",
                f"配置名称 '{config_name}' 已存在，是否覆盖？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return  # 用户选择不覆盖

         # 6. 更新配置数据
        config_data[config_name] = selected_EEG_names
        # 7. 保存到JSON文件[5](@ref)
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "成功", "配置保存成功！")
            self.init_config()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存配置失败: {str(e)}")
    def load_configs(self):
        # 1. 获取当前选中的配置名称
        config_name = self.ui.config_combo.currentText()
        if not config_name:
            QMessageBox.warning(self, "警告", "请选择有效的配置")
            return
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)  # 上一级目录
        config_path = os.path.join(parent_dir, "model", "uploadmodel_config.json")
        try:
            # 3. 检查文件是否存在
            if not os.path.exists(config_path):
                QMessageBox.warning(self, "错误", "配置文件不存在")
                return
            # 4. 读取JSON文件
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            # 5. 检查配置名称是否存在
            if config_name not in config_data:
                QMessageBox.warning(self, "错误", f"配置 '{config_name}' 不存在")
                return
            # 6. 获取该配置的EEG列表
            eeg_list = config_data[config_name]
            # 7. 清空当前已选列表
            self.ui.selected_listWidget.clear()
            # 8. 逐项添加到列表控件
            for eeg_name in eeg_list:
                self.ui.selected_listWidget.addItem(eeg_name)
        except json.JSONDecodeError:
            QMessageBox.critical(self, "错误", "配置文件格式错误，无法解析")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载配置时出错: {str(e)}")
    def delete_config(self):
        """
            根据下拉框选中的配置名称删除JSON文件中的配置项
            """
        # 1. 获取选中的配置名称
        config_name = self.ui.config_combo.currentText()
        if not config_name:
            QMessageBox.warning(self, "警告", "请选择要删除的配置")
            return
        # 2. 确认删除操作
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除配置 '{config_name}' 吗?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)  # 上一级目录
        config_path = os.path.join(parent_dir, "model", "uploadmodel_config.json")
        try:
            # 3. 检查文件是否存在
            if not os.path.exists(config_path):
                QMessageBox.warning(self, "错误", "配置文件不存在")
                return
            # 4. 读取JSON文件
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            # 5. 检查配置是否存在
            if config_name not in config_data:
                QMessageBox.warning(self, "错误", f"配置 '{config_name}' 不存在")
                return
            # 6. 删除配置项
            del config_data[config_name]
            # 7. 保存更新后的JSON
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            # 8. 更新下拉框
            self.init_config()
            # 9. 清空列表控件
            self.ui.selected_listWidget.clear()
            QMessageBox.information(self, "成功", f"配置 '{config_name}' 已删除")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "错误", "配置文件格式错误，无法解析")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"删除配置时出错: {str(e)}")
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
    def itemclicked_REF_listWidget(self,item):
        self.REF_channel=item.text()
    def itemDoubleClicked_EEG_listWidget(self, item):
        if self.REF_channel==None:
            QMessageBox.information(self, '提示','未选择参考通道',QMessageBox.Yes)
            return
        else:
            selected_EEG_names = []
            item_count = self.ui.selected_listWidget.count()
            # 按顺序获取每个选项
            for i in range(item_count): #用于识别是否重复选中
                a = self.ui.selected_listWidget.item(i)
                selected_EEG_names.append(a.text())
            text = item.text()+self.REF_channel
            if text in selected_EEG_names:
                reply=QMessageBox.information(self, '提示', '出现重复选择，是否确认加入？', QMessageBox.Yes | QMessageBox.No)
                if reply!=16384:
                    return
            # text=text+self.REF_channel
            item_clone = QListWidgetItem(text)
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
class clsPrentryView(QWidget):
    signal_save_configID_names = pyqtSignal(str)
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.ui = Ui_clsPrentryForm()
        self.ui.setupUi(self)
class SetSelectView(QWidget):
    control_signal_set = pyqtSignal(list)
    def __init__(self,current_page, parent=None):
        super().__init__(parent)
        self.ui = Ui_setselectForm()
        self.ui.setupUi(self)
        self.header = ['数据集名称']
        self.field = ['set_name']
        self.cur_page = 0
    def initTable(self, data,curPageIndex):
        self.cur_page = curPageIndex
        try:
            col_num = len(self.header)
            row_num = len(data)
            self.ui.tableWidget_set.setColumnCount(col_num)
            self.ui.tableWidget_set.setRowCount(row_num)
            self.ui.tableWidget_set.setInputMethodHints(Qt.ImhHiddenText)
            # 设置表格高度
            for i in range(row_num):
                self.ui.tableWidget_set.setRowHeight(i, 45)
            # 设置除最后一列之外的列的宽度
            for i in range(0, col_num - 1):
                self.ui.tableWidget_set.setColumnWidth(i, 150)

            for i in range(col_num):
                header_item = QTableWidgetItem(self.header[i])
                font = header_item.font()
                font.setPointSize(16)
                header_item.setFont(font)
                header_item.setForeground(QBrush(Qt.black))
                header_item.setData(Qt.UserRole, self.field[i])
                self.ui.tableWidget_set.setHorizontalHeaderItem(i, header_item)
                # 拉伸表格列项，使其铺满
                self.ui.tableWidget_set.horizontalHeader().setStretchLastSection(True)

            for r in range(row_num):
                for c in range(col_num):
                    self.item = QTableWidgetItem(str(data[r][c+1]))
                    self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    font = self.item.font()
                    font.setPointSize(10)
                    self.item.setFont(font)

                    self.ui.tableWidget_set.setItem(r, c, self.item)
            self.ui.tableWidget_set.horizontalHeader().setHighlightSections(False)
            #   按字段长度进行填充
            self.ui.tableWidget_set.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.tableWidget_set.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

            # 增加和查询的时候列数会改变，所以需要保存原来的列数
            self.col = self.ui.tableWidget_set.columnCount()
        except Exception as e:
            print('initTable', e)
    def update_table(self,data,curPageIndex,curpagemax=''):

        self.cur_page = curPageIndex
        self.curPage.setText(str(curPageIndex))
        if curpagemax !='':
            self.totalPage.setText("共" + str(curpagemax) + "页")
        col_num = len(self.header)
        row_num = len(data)
        row_max=12
        for r in range(row_max):
            self.ui.tableWidget_set.removeRow(r)
        self.ui.tableWidget_set.setColumnCount(col_num)
        self.ui.tableWidget_set.setRowCount(row_num)
        self.ui.tableWidget_set.setInputMethodHints(Qt.ImhHiddenText)
        for i in range(row_num):
            self.ui.tableWidget_set.setRowHeight(i, 45)
        # 设置除最后一列之外的列的宽度
        for i in range(0, col_num - 1):
            self.ui.tableWidget_set.setColumnWidth(i, 150)

        for i in range(col_num):
            header_item = QTableWidgetItem(self.header[i])
            font = header_item.font()
            font.setPointSize(16)
            header_item.setFont(font)
            header_item.setForeground(QBrush(Qt.black))
            header_item.setData(Qt.UserRole, self.field[i])
            self.ui.tableWidget_set.setHorizontalHeaderItem(i, header_item)
            # 拉伸表格列项，使其铺满
            self.ui.tableWidget_set.horizontalHeader().setStretchLastSection(True)

        for r in range(row_num):
            for c in range(col_num):
                self.item = QTableWidgetItem(str(data[r][c+1]))
                self.item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                font = self.item.font()
                font.setPointSize(10)
                self.item.setFont(font)

                self.ui.tableWidget_set.setItem(r, c, self.item)
        self.ui.tableWidget_set.horizontalHeader().setHighlightSections(False)

        #   按字段长度进行填充
        self.ui.tableWidget_set.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableWidget_set.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
    def setPageController_set(self, page):
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
        homePage.clicked.connect(self.__home_page_set)
        prePage.clicked.connect(self.__pre_page_set)
        nextPage.clicked.connect(self.__next_page_set)
        finalPage.clicked.connect(self.__final_page_set)
        confirmSkip.clicked.connect(self.__confirm_skip_set)
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
    def __home_page_set(self):
        """点击首页信号"""
        self.control_signal_set.emit(["home", self.curPage.text()])
    def __pre_page_set(self):
        """点击上一页信号"""
        self.control_signal_set.emit(["pre", self.curPage.text()])
    def __next_page_set(self):
        """点击下一页信号"""
        self.control_signal_set.emit(["next", self.curPage.text()])
    def __final_page_set(self):
        """尾页点击信号"""
        self.control_signal_set.emit(["final", self.curPage.text()])
    def __confirm_skip_set(self):
        """跳转页码确定"""
        self.control_signal_set.emit(["confirm", self.skipPage.text()])
    def showTotalPage_set(self):
        """返回当前总页数"""
        return int(self.totalPage.text()[1:-1])

if __name__ == '__main__':
    pass


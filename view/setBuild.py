import sys

from PyQt5.QtGui import *
from PyQt5.uic.properties import QtCore

from view.setBulid_form.form import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from view.sampleState import QComboCheckBox


class setBulidView(QWidget):
    set_page_control_signal = pyqtSignal(list)

    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.controller = controller
        self.ui.setupUi(self)
        self.signal_connect()
        # self.ui.re_scheme.currentTextChanged.connect(self.set_re_scheme_tool_tip)

    def init_reverse_scheme(self, rs_list, neg_desc_list):

        list_view_model = QStandardItemModel()
        self.ui.re_scheme.setModel(list_view_model)
        self.ui.re_scheme.clear()
        item = QStandardItem()
        item.setText("Random Select")
        list_view_model.appendRow(item)
        item = QStandardItem()
        item.setText("State Neg Model 1")
        list_view_model.appendRow(item)

        # TODO 这边先注释掉
        for rs in rs_list:
            item = QStandardItem()
            item.setText(rs)
            list_view_model.appendRow(item)
            # self.ui.re_scheme.addItem(rs)
        i = 1
        for nd in neg_desc_list:
            list_view_model.item(i).setToolTip(nd)
            i += 1


    def signal_connect(self):
        # self.controller.re_scheme_signal.connect(self.model_import_show)
        # self.controller.set_reverse_scheme_null.connect(self.set_current_scheme_null)
        self.ui.re_scheme.currentTextChanged.connect(self.controller.on_reverse_scheme_changed)
        self.controller.init_reverse_scheme.connect(self.init_reverse_scheme)
        self.ui.homePage.clicked.connect(self.home_page)
        self.ui.prePage.clicked.connect(self.pre_page)
        self.ui.nextPage.clicked.connect(self.next_page)
        self.ui.finalPage.clicked.connect(self.final_page)
        self.ui.confirmSkip.clicked.connect(self.confirm_skip)

    def fltTable(self, content):
        try:
            col_num = 4
            row_num = len(content)
            self.ui.tableWidget_2.setRowCount(row_num)
            self.ui.tableWidget_2.setColumnCount(col_num)
            # 设置表格高度
            for i in range(row_num):
                self.ui.tableWidget_2.setRowHeight(i, 55)

            # 设置列头
            col_label = ['类型', '标注用户', '病人名称', '文件单号']
            # col_label = ['Type', 'Label User', 'Patient Name', 'File ID']

            self.ui.tableWidget_2.setHorizontalHeaderLabels(col_label)
            self.ui.tableWidget_2.horizontalHeader().setStyleSheet(
                '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
            # 使表格填满整个widget
            self.ui.tableWidget_2.horizontalHeader().setStretchLastSection(True)
            self.ui.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)

            # 设置各列的宽度
            column_widths = [150, 200, 200, 200]
            # 设置每列的宽度
            for i, width in enumerate(column_widths):
                self.ui.tableWidget_2.setColumnWidth(i, width)

            for row in range(0, row_num):
                for col in range(0, col_num):
                    if isinstance(content[row][col], int):
                        text_item = QTableWidgetItem(str(content[row][col]))
                    else:
                        if content[row][col] == '全部':
                            text_item = QTableWidgetItem('-')
                        else:
                            text_item = QTableWidgetItem(content[row][col])
                    text_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    text_item.setFont(QFont('', 12))
                    self.ui.tableWidget_2.setItem(row, col, text_item)
        except Exception as e:
            print('fltTable', e)

    def init_setTable(self, table):
        col_num = 4
        row_num = len(table)
        self.ui.tableWidget.setRowCount(row_num)
        self.ui.tableWidget.setColumnCount(col_num)
        # 设置表格高度
        for i in range(row_num):
            self.ui.tableWidget.setRowHeight(i, 55)

        # 各列均分
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 设置列头
        col_label = ['数据集名称', '类型', '训练集文件名', '测试集文件名']
        # col_label = ['Dataset Name', 'Type', 'Training Set', 'Test Set']

        self.ui.tableWidget.setHorizontalHeaderLabels(col_label)
        self.ui.tableWidget.horizontalHeader().setStyleSheet(
            '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
        # 使表格填满整个widget
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for row in range(0, row_num):
            for col in range(1, col_num + 1):
                if isinstance(table[row][col], int):
                    text_item = QTableWidgetItem(str(table[row][col]))
                else:
                    text_item = QTableWidgetItem(table[row][col])
                text_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                text_item.setFont(QFont('', 12))
                self.ui.tableWidget.setItem(row, col - 1, text_item)

    # 训练集测试集比率设置
    def set_train_test_ratio(self):
        if self.ui.lineEdit.text() == '':
            return
        ratio = int(self.ui.lineEdit.text())
        self.ui.label_4.setText('测试集比率:{}%'.format(str(100 - ratio)))

    def set_check_search(self, checkBox, line_edit, items):
        completer = QCompleter(items, self)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        line_edit.setFont(QFont("Arial", 9))
        line_edit.setPlaceholderText("点击可搜索,移动至此有提示")
        line_edit.setCompleter(completer)
        checkBox.setLineEdit(line_edit)
        checkBox.setCompleter(completer)
        checkBox.setFixedWidth(180)
        checkBox.setMinimumHeight(28)
        checkBox.setInsertPolicy(QComboBox.NoInsert)

    # 设置复选框选项提示
    def set_check_tooltip(self, checkBox, items):
        n = 0
        for i in items:
            checkBox.setItemData(n, i, Qt.ToolTipRole)
            n += 1

        # 响应参考方案选择框

    # 清理布局
    def clear(self, layout, num=0, count=-1):
        item_list = list(range(layout.count()))
        item_list.reverse()
        # print(item_list)
        j = 0
        for i in item_list:
            if num == 0 and count == -1:
                item = layout.itemAt(i)
                layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
            elif num != 0 and count == -1:
                item = layout.itemAt(i)
                layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
                j += 1
                if j == num:
                    return
            elif num == 0 and count != -1:
                if j == count:
                    item = layout.itemAt(i)
                    layout.removeItem(item)
                    if item.widget():
                        item.widget().deleteLater()
                    return
                j += 1

    # 设置已添加的项目提示
    def set_add_tip(self, comboBox, lineEdit, addItem, allItem):
        # 选中的数量
        l = len(addItem)
        # 总数量
        l_ = len(allItem)
        set_tip = "(全选)" if l == l_ else "(无选择)" if l == 0 else "已添加：\n\t" + "\n\t".join(
            (comboBox.itemText(int(item)) for item in addItem))
        lineEdit.setToolTip(set_tip)

    def init_view(self, type_info, state_info, montage_name, set_data, themeInfo):
        try:
            self.font = QFont()
            # combox内的字体大小
            self.font1 = QFont()
            self.font.setPointSize(12)
            self.font1.setPointSize(9)
            self.spaceItemWidth1 = 33
            self.spaceItemWidth2 = 56
            self.spaceItemWidth3 = 89
            self.spaceItemWidth4 = 112
            self.spaceItemWidth5 = 145
            self.fileComboBoxWidth = 150
            self.typeDelWidth = 755
            self.typeDelbtnWidth = 30

            self.DataSourceBox_1 = QComboCheckBox(['诊断标注', '科研标注'], default_check=False)
            self.DataSourceBox_1.setVisible(False)

            self.spaceItem_1 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.dataSourceLabel = QLabel()
            self.ui.horizontalLayout_2.addWidget(self.DataSourceBox_1)
            self.ui.horizontalLayout_2.addWidget(self.dataSourceLabel)

            self.ui.horizontalLayout_2.addItem(self.spaceItem_1)
            self.ui.horizontalLayout_2.setStretch(3, 1)
            self.spaceItem_2 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.ui.comboBox_2.addItems(type_info)
            self.ui.comboBox_2.setInsertPolicy(QComboBox.NoInsert)
            self.line_edit = QLineEdit()
            self.line_edit.setToolTip("(无选择)")
            self.set_check_search(self.ui.comboBox_2, self.line_edit, type_info)
            self.set_check_tooltip(self.ui.comboBox_2, type_info)
            self.ui.comboBox.setCurrentIndex(-1)
            self.ui.comboBox_2.setCurrentText("")

            themeNames = [item[1] for item in themeInfo]
            print(f'themeNames: {themeNames}')
            self.ui.themeBox.clear_items()
            self.ui.themeBox.add_items(themeNames)

            self.ui.comboBox_3.addItems(state_info)
            self.ui.comboBox_3.setInsertPolicy(QComboBox.NoInsert)
            self.line_edit_1 = QLineEdit()
            self.line_edit_1.setToolTip("(无选择)")
            self.set_check_search(self.ui.comboBox_3, self.line_edit_1, state_info)
            self.set_check_tooltip(self.ui.comboBox_3, state_info)
            self.ui.comboBox_3.setCurrentText("")

            intValidator = QIntValidator(self)
            intValidator.setRange(1, 99)
            self.ui.lineEdit.setValidator(intValidator)
            self.ui.lineEdit.textChanged.connect(self.set_train_test_ratio)
            montage_lineEdit = QLineEdit()
            self.ui.comboBox_5.addItems(montage_name)
            self.set_check_search(self.ui.comboBox_5, montage_lineEdit, montage_name)
            self.set_check_tooltip(self.ui.comboBox_5, montage_name)

            self.ui.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
            self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.ui.comboBox.setCurrentText("中心延拓")
            self.ui.comboBox.setCurrentIndex(-1)

        except Exception as e:
            print('init_view', e)

    def home_page(self):
        self.set_page_control_signal.emit(["home"])

    def pre_page(self):
        self.set_page_control_signal.emit(["pre"])

    def next_page(self):
        self.set_page_control_signal.emit(["next"])

    def final_page(self):
        self.set_page_control_signal.emit(["final"])

    def confirm_skip(self):
        self.set_page_control_signal.emit(["confirm"])

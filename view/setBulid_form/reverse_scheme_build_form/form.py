from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt
from functools import partial

from PyQt5.uic.uiparser import QtCore
from pyqt5_plugins.examplebuttonplugin import QtGui
# from util.TableWidget import TableWidget


class reverse_scheme_build_view(QDialog):
    import_done = pyqtSignal(str, bool)
    show_scheme_edit = pyqtSignal(str, str, bool, bool)
    show_alg_register = pyqtSignal(str)
    scheme_del_signal = pyqtSignal(str)

    def __init__(self, controller=None):
        super().__init__()
        self.sub_model_dict = dict()
        self.controller = controller
        self.controller.init_reverse_scheme_detail.connect(self.get_reverse_scheme_data)
        self.last_cls_layout_num = 0
        self.init_view()

    def init_view(self):
        self.setWindowTitle("反例方案配置")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.center_layout = QVBoxLayout()
        self.setLayout(self.center_layout)
        self.horizontalLayout_4 = QHBoxLayout()
        add_reverse_button = QPushButton("添加反例方案")
        add_reverse_button.clicked.connect(lambda: self.show_scheme_edit.emit('', '', True, True))
        spacerItem_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_4.addWidget(add_reverse_button)
        self.horizontalLayout_4.addItem(spacerItem_5)
        self.horizontalLayout_4.setStretch(1, 1)
        self.center_layout.addLayout(self.horizontalLayout_4)

        # scheme_table = TableWidget(col_label=["方案名称", "算法绑定", '是否需要导入模型'], )
        self.tableWidget = QTableWidget()
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.menu_select)
        self.center_layout.addWidget(self.tableWidget)

        #
        font = QFont("Arial", 10)

        """
            提示
        """
        self.horizontalLayout_5 = QHBoxLayout()
        self.note_tip = QLabel("提示：仅支持pytorch框架")
        self.note_tip.setFont(font)
        self.note_tip.setStyleSheet("color:red")
        spacerItem_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_5.addWidget(self.note_tip)
        self.horizontalLayout_5.addItem(spacerItem_6)
        self.horizontalLayout_5.setStretch(-1, 1)

        self.center_layout.addLayout(self.horizontalLayout_5)

    def get_reverse_scheme_data(self, reverse_scheme):
        self.reverse_scheme = reverse_scheme
        reverse_scheme_data = [[rs['name'], rs['describe'], rs['is_load_model'], rs['alg_address']] for rs in
                               self.reverse_scheme]
        self.init_scheme_table(reverse_scheme_data)

    def menu_select(self, pos):
        row_num = -1
        for i in self.tableWidget.selectionModel().selection().indexes():
            row_num = i.row()
        if row_num == -1:
            return
        scheme_name = self.tableWidget.item(row_num, 0).text()
        scheme_desc = self.tableWidget.item(row_num, 1).text()
        is_import_model = self.tableWidget.item(row_num, 2).text()
        if is_import_model == '是':
            is_import_model = True
        else:
            is_import_model = False

        menu = QMenu()
        item1 = menu.addAction(u"编辑方案")
        item2 = menu.addAction(u"绑定算法")
        item3 = menu.addAction(u"删除方案")
        action = menu.exec_(self.tableWidget.mapToGlobal(pos))
        if action == item1:
            self.show_scheme_edit.emit(scheme_name, scheme_desc, is_import_model, False)
        elif action == item2:
            self.show_alg_register.emit(scheme_name)
        elif action == item3:
            reply = QMessageBox.information(self, '提示', '是否删除该方案？', QMessageBox.Yes | QMessageBox.No)
            if reply == 16384:
                self.scheme_del_signal.emit(scheme_name)

    def init_scheme_table(self, table):
        # 设置列头
        col_label = ['方案名称', '方案描述', '是否需要导入模型', '是否绑定算法']
        col_num = len(col_label)
        row_num = len(table)
        self.tableWidget.setRowCount(row_num)
        self.tableWidget.setColumnCount(col_num)
        # 设置表格高度
        for i in range(row_num):
            self.tableWidget.setRowHeight(i, 55)

        # 各列均分
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableWidget.setHorizontalHeaderLabels(col_label)
        self.tableWidget.horizontalHeader().setStyleSheet(
            '''font: 20px;border:none;border-bottom:1px solid rgb(210, 210, 210)''')
        # 使表格填满整个widget
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for row in range(0, row_num):
            for col in range(0, col_num):
                if col == col_num - 2:
                    if table[row][col]:
                        table[row][col] = '是'
                    else:
                        table[row][col] = '否'
                if col == col_num - 1:
                    if table[row][col] != '':
                        table[row][col] = '是'
                    else:
                        table[row][col] = '否'

                if isinstance(table[row][col], int):
                    text_item = QTableWidgetItem(str(table[row][col]))
                else:
                    text_item = QTableWidgetItem(table[row][col])
                text_item.setToolTip(str(table[row][col]))
                text_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                text_item.setFont(QFont('', 12))

                self.tableWidget.setItem(row, col, text_item)

    def import_confirm(self):
        if self.spcify_address.text() == '':
            QMessageBox.information(self, "提示", "尚未导入任何方案！")
            return
        else:
            self.import_done.emit(self.spcify_address.text(), self.is_load_model_button.isChecked())
            self.close()

    def import_reset(self):
        self.spcify_address.setText('')
        self.is_load_model_button.setCheckable(True)

    def file_select(self, label: QLabel):
        filePath, ok = QFileDialog.getOpenFileName(self, "模型导入", "C:/")
        if ok:
            label.setText(str(filePath))
            self.close()
            self.show()

class scheme_edit_view(QDialog):
    edit_confirm_signal = pyqtSignal(str, list)
    add_confirm_signal = pyqtSignal(str)

    def __init__(self, controller, scheme_name=None, scheme_desc=None, is_import_model=False, is_add=True):
        super().__init__()
        self.controller = controller
        # self.controller.re_scheme_add_err_signal.connect(self.add_error_handle)
        self.scheme_name = scheme_name
        self.scheme_desc = scheme_desc
        self.is_import_model = is_import_model
        self.is_add = is_add

        self.init_view()

    def init_view(self):
        self.setWindowTitle("方案编辑")
        self.setMinimumWidth(300)
        self.setMinimumHeight(150)

        self.center_layout = QVBoxLayout()
        self.setLayout(self.center_layout)
        self.horizontalLayout_1 = QHBoxLayout()
        scheme_name = QLabel("方案名称：")
        self.scheme_name_edit = QLineEdit()
        self.scheme_name_edit.setText(self.scheme_name)
        self.horizontalLayout_1.addWidget(scheme_name)
        self.horizontalLayout_1.addWidget(self.scheme_name_edit)
        # self.center_layout.addLayout(self.horizontalLayout_1)

        self.horizontalLayout_2 = QHBoxLayout()
        scheme_desc = QLabel("方案描述：")
        self.scheme_desc_edit = QTextEdit()
        self.scheme_desc_edit.setText(self.scheme_desc)
        self.horizontalLayout_2.addWidget(scheme_desc)
        self.horizontalLayout_2.addWidget(self.scheme_desc_edit)

        self.horizontalLayout_4 = QHBoxLayout()
        is_import_model = QLabel("是否导入模型：")
        self.yes_button = QRadioButton("是")
        self.no_button = QRadioButton("否")
        if self.is_import_model:
            self.yes_button.setChecked(True)
        else:
            self.no_button.setChecked(True)
        self.horizontalLayout_4.addWidget(is_import_model)
        self.horizontalLayout_4.addWidget(self.yes_button)
        self.horizontalLayout_4.addWidget(self.no_button)

        self.horizontalLayout_3 = QHBoxLayout()
        if not self.is_add:
            self.confirm_button = QPushButton("确认修改")
            self.confirm_button.clicked.connect(self.edit_confirm)
        else:
            self.confirm_button = QPushButton("确认添加")
            self.confirm_button.clicked.connect(self.add_confirm)

        self.reset_button = QPushButton("重置")
        spacerItem_1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacerItem_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacerItem_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem_1)
        self.horizontalLayout_3.addWidget(self.confirm_button)
        self.horizontalLayout_3.addItem(spacerItem_2)
        self.horizontalLayout_3.addWidget(self.reset_button)
        self.horizontalLayout_3.addItem(spacerItem_3)

        # self.center_layout.addLayout(self.horizontalLayout_1)
        self.center_layout.addLayout(self.horizontalLayout_2)
        # self.center_layout.addLayout(self.horizontalLayout_4)
        # self.center_layout.addLayout(self.horizontalLayout_5)
        self.center_layout.addLayout(self.horizontalLayout_3)

        self.reset_button.clicked.connect(self.detail_reset)

    # 确认编辑
    def edit_confirm(self):
        if self.scheme_name_edit == '':
            QMessageBox.information(self, '提示', '方案名称尚未填写')
            return
        old_scheme_name = self.scheme_name
        scheme_name = self.scheme_name_edit.text()
        scheme_desc = 'No Describe' if self.scheme_desc_edit.toPlainText() == '' else self.scheme_desc_edit.toPlainText()
        is_import_model = self.yes_button.isChecked()
        self.edit_confirm_signal.emit(old_scheme_name, [scheme_name, scheme_desc, is_import_model])
        self.close()

    # 确认添加
    def add_confirm(self):
        # if self.scheme_name_edit == '':
        #     QMessageBox.information(self, '提示', '方案名称尚未填写')
        #     return
        # scheme_name = self.scheme_name_edit.text()
        scheme_desc = 'No Describe' if self.scheme_desc_edit.toPlainText() == '' else self.scheme_desc_edit.toPlainText()
        # is_import_model = self.yes_button.isChecked()
        # scheme_dict = {"name": scheme_name,
        #                "describe": scheme_desc,
        #                "alg_address": "",
        #                "is_load_model": is_import_model
        #                }
        # self.add_confirm_signal.emit(scheme_dict)
        self.add_confirm_signal.emit(scheme_desc)
        self.close()



    def add_error_handle(self, tag):
        QMessageBox.information(self, '提示', '方案名称重复，请重新命名方案！')

    # 内容重置
    def detail_reset(self):
        self.scheme_name_edit.setText(self.scheme_name)
        self.scheme_desc_edit.setText(self.scheme_desc)
        self.yes_button.setChecked(self.is_import_model)


class alg_register_view(QDialog):
    bind_signal = pyqtSignal(str, str)

    def __init__(self, rs_name, controller=None):
        super().__init__()
        self.rs_name = rs_name
        self.controller = controller
        self.init_view()

    def init_view(self):
        self.setWindowTitle("算法绑定")
        self.setMinimumWidth(400)
        self.setMaximumHeight(80)
        self.center_layout = QVBoxLayout()
        self.setLayout(self.center_layout)
        self.horizontalLayout_1 = QHBoxLayout()
        alg_pos = QLabel("算法位置：")
        self.alg_pos_detail = QLabel("")
        self.select_button = QPushButton("选择")
        self.horizontalLayout_1.addWidget(alg_pos)
        self.horizontalLayout_1.addWidget(self.alg_pos_detail)
        self.horizontalLayout_1.addWidget(self.select_button)
        self.horizontalLayout_1.setStretch(1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        spacerItem_1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacerItem_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.bind_button = QPushButton("绑定")

        self.horizontalLayout_2.addItem(spacerItem_1)
        self.horizontalLayout_2.addWidget(self.bind_button)
        self.horizontalLayout_2.addItem(spacerItem_2)

        self.center_layout.addLayout(self.horizontalLayout_1)
        self.center_layout.addLayout(self.horizontalLayout_2)

        self.select_button.clicked.connect(self.file_select)
        self.bind_button.clicked.connect(self.emit_bind_signal)

    # 算法文件选择
    def file_select(self):
        filePath, ok = QFileDialog.getOpenFileName(self, "模型导入", "C:/", 'py(*.py)')
        if ok:
            self.alg_pos_detail.setText(str(filePath))
            self.close()
            self.show()

    # 发送算法绑定信号给controller
    def emit_bind_signal(self):
        alg_pos = self.alg_pos_detail.text()
        if alg_pos == '':
            QMessageBox.information(self, '提示', '尚未绑定任何算法')
            return
        self.bind_signal.emit(self.rs_name, alg_pos)
        self.close()

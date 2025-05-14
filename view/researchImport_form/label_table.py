# labeltype_view.py
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidgetItem, QComboBox, QLabel, QHeaderView, QMessageBox
)

class LabelTypeTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("选择 labeltype 映射")
        self.resize(800, 400)
        self.init_ui()
        self.table.cellClicked.connect(self.on_labeltype_selected)

    def init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        # 左侧：表格输入字段名 + 提取方式
        left_layout = QVBoxLayout()
        layout.addLayout(left_layout)

        self.input_table = QTableWidget()
        self.input_table.setColumnCount(3)
        self.input_table.setHorizontalHeaderLabels(["字段名", "提取方式", "标注类型"])
        self.input_table.setRowCount(5)  # 初始行数
        self.input_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row in range(5):
            self.input_table.setItem(row, 0, QTableWidgetItem())

            combo = QComboBox()
            combo.addItems(["value_transition", "nonzero_rising"])
            self.input_table.setCellWidget(row, 1, combo)

        left_layout.addWidget(QLabel("字段配置（每行一组）:"))
        left_layout.addWidget(self.input_table)

        # ✅ 添加“添加一行”按钮
        self.add_row_btn = QPushButton("添加一行")
        self.add_row_btn.clicked.connect(self.add_input_row)
        left_layout.addWidget(self.add_row_btn)

        self.confirm_btn = QPushButton("确认添加映射")
        left_layout.addWidget(self.confirm_btn)

        # 右侧 labeltype 数据展示
        right_layout = QVBoxLayout()
        layout.addLayout(right_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["type_id", "type_name", "description", "category"])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        right_layout.addWidget(QLabel("数据库中已有 labeltype 信息："))
        right_layout.addWidget(self.table)

    def set_table_data(self, data):
        self.table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))


    def get_all_field_configs(self, check_number):
        result = {}

        for row in range(self.input_table.rowCount()):
            field_item = self.input_table.item(row, 0)
            extract_type_widget = self.input_table.cellWidget(row, 1)
            labeltype_item = self.input_table.item(row, 2)

            if field_item and field_item.text().strip():
                field = field_item.text().strip()
                extract_type = extract_type_widget.currentText()
                labeltype_text = labeltype_item.text().strip() if labeltype_item else ""
                if "-" in labeltype_text:
                    type_id, type_name = map(str.strip, labeltype_text.split("-", 1))
                else:
                    type_id, type_name = "", ""

                # 如果这个 check_number 已经存在，则添加到对应的配置列表中
                if check_number not in result:
                    result[check_number] = []

                result[check_number].append({
                    "states_field": field,
                    "extract_type": extract_type,
                    "type_id": type_id,
                    "type_name": type_name
                })

        # 转换为一个列表，便于保存为 JSON
        return [{"check_number": check_number, "configs": configs} for check_number, configs in result.items()]

    def on_labeltype_selected(self, row, column):
        selected_type_id = self.table.item(row, 0).text()
        selected_type_name = self.table.item(row, 1).text()
        full_label = f"{selected_type_id} - {selected_type_name}"

        current_row = self.input_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "提示", "请先选中左侧要填入的行", QMessageBox.Yes)
            return

        self.input_table.setItem(current_row, 2, QTableWidgetItem(full_label))


    def add_input_row(self):
        current_row = self.input_table.rowCount()
        self.input_table.insertRow(current_row)

        # 字段名输入框
        self.input_table.setItem(current_row, 0, QTableWidgetItem())

        # 提取方式下拉框
        combo = QComboBox()
        combo.addItems(["value_transition", "nonzero_rising"])
        self.input_table.setCellWidget(current_row, 1, combo)

        # 留空的标注类型单元格
        self.input_table.setItem(current_row, 2, QTableWidgetItem())



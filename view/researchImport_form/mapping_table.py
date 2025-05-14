from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView
from PyQt5.QtCore import Qt

class MappingView(QWidget):
    def __init__(self, mapping, parent=None):
        super().__init__(parent)
        self.setWindowTitle("标注配置查看")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['字段名 (states_field)', '提取方式 (extract_type)', '类型ID (type_id)', '类型名 (type_name)'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        if isinstance(mapping, list):
            self.table.setRowCount(len(mapping))
            for row, entry in enumerate(mapping):
                self.table.setItem(row, 0, QTableWidgetItem(entry.get("states_field", "")))
                self.table.setItem(row, 1, QTableWidgetItem(entry.get("extract_type", "")))
                self.table.setItem(row, 2, QTableWidgetItem(entry.get("type_id", "")))
                self.table.setItem(row, 3, QTableWidgetItem(entry.get("type_name", "")))
        else:
            # 显示错误或提示信息
            self.table.setRowCount(1)
            self.table.setColumnCount(1)
            self.table.setHorizontalHeaderLabels(['提示信息'])
            msg = next(iter(mapping.values())) if isinstance(mapping, dict) else "未知错误"
            self.table.setItem(0, 0, QTableWidgetItem(msg))

        self.btn_close = QPushButton("关闭")
        self.btn_close.clicked.connect(self.close)

        layout.addWidget(self.table)
        layout.addWidget(self.btn_close)
        self.setLayout(layout)

        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("QTableWidget::item { font-size: 14pt; }")


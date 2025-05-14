from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class LoadingDialog(QDialog):
    def __init__(self, text="正在处理中...", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setModal(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.loading_label = QLabel()
        self.loading_label.setText("🔄")  # 替代符号图标
        self.loading_label.setFont(QFont("Arial", 30))
        self.loading_label.setAlignment(Qt.AlignCenter)

        # 文本说明
        self.text_label = QLabel(text)
        self.text_label.setFont(QFont("微软雅黑", 11))
        self.text_label.setStyleSheet("color: black;")  # 更清晰
        self.text_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.loading_label)
        layout.addWidget(self.text_label)
        self.setLayout(layout)

        # 加点背景，边框可见
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 2px solid #888;
                border-radius: 10px;
            }
        """)
        self.setFixedSize(240, 180)

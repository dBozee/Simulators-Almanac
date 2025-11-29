from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QWidget


class KVPWidget(QWidget):
    def __init__(self, key: str, value: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.grid_layout = QGridLayout()
        self.key = QLabel(key)
        self.value = QLabel(value)

        self.grid_layout.addWidget(self.key, 0, 0)
        self.grid_layout.addWidget(self.value, 0, 1)
        self.grid_layout.setSpacing(5)
        self.grid_layout.setContentsMargins(0, 0, 10, 5)

        self.setLayout(self.grid_layout)
        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnMinimumWidth(0, 100)
        self.grid_layout.setColumnStretch(1, 0)
        self.key.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.value.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setSizePolicy(self.sizePolicy().Policy.MinimumExpanding, self.sizePolicy().Policy.Fixed)

    def update_key(self, key: str):
        self.key.setText(key)

    def update_value(self, value: str):
        self.value.setText(value)

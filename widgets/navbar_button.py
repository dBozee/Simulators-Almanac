from collections.abc import Callable

from PyQt6.QtWidgets import QPushButton


class NavbarButton(QPushButton):
    def __init__(self, page_name: str, callback: Callable):
        super().__init__()
        self.clicked_func: Callable = callback
        self.page_name: str = page_name
        self.setText(page_name)
        self.setFixedWidth(120)
        self.clicked.connect(self.button_clicked)

    def button_clicked(self):
        self.clicked_func(self.page_name)

from PyQt6.QtWidgets import QLabel, QVBoxLayout

from widgets.pages import BasePage


class HomePage(BasePage):
    def __init__(self, container_widget, readers):
        super().__init__(container_widget, readers)
        layout = QVBoxLayout()

        text = QLabel("This is the home page")
        layout.addWidget(text)
        layout.addStretch()

        self.setLayout(layout)

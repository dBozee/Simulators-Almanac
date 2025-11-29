from PyQt6.QtWidgets import QWidget

from readers import AllReaders


class BasePage(QWidget):
    def __init__(self, container_widget, readers: AllReaders):
        super().__init__(container_widget)
        self.data: AllReaders = readers

    def update_content(self, readers: AllReaders):
        self.data = readers

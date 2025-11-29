from PyQt6.QtWidgets import QWidget

from readers import AllReaders


class BasePage(QWidget):
    def __init__(self, container_widget, readers: AllReaders | None):
        super().__init__(container_widget)
        self.data: AllReaders | None = readers

    def update_content(self, readers: AllReaders):
        self.data = readers
        self._update_ui()

    def _update_ui(self):
        raise NotImplementedError("Subclasses of BasePage must implement an _update_ui method")

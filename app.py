import sys

from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from readers.all_readers import AllReaders
from widgets.path_browser import PathBrowser


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        QApplication.setOrganizationName("dBozee")
        QApplication.setApplicationName("SimulatorsAlmanac")

        self.readers: AllReaders | None = None

        container_widget = QWidget()
        layout = QVBoxLayout(container_widget)

        self.setWindowTitle("Simulator's Almanac")
        self.setGeometry(100, 100, 1280, 720)

        self.path_browser = PathBrowser(container_widget)
        layout.addWidget(self.path_browser)
        layout.addStretch()

        self.setCentralWidget(container_widget)

        self.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Override of the base class event. Runs this function on (safe) close of the program"""
        if self.path_browser:
            self.path_browser.save_settings()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

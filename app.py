import sys
from pathlib import Path

from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QWidget,
)

from readers.all_readers import AllReaders
from readers.base_reader import BaseReader
from readers.fields import Fields

SETTINGS_KEY_SAVE_PATH = "LastSavePath"


class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()

        QApplication.setOrganizationName("dBozee")
        QApplication.setApplicationName("Simulator's Almanac")

        self.settings = QSettings()
        self.path: Path = Path.home()
        self.layout = QGridLayout()
        self.file_line = QLineEdit()
        self.load_button: QPushButton | None = None
        self.readers: AllReaders | None = None

        container_widget = QWidget()

        self.setWindowTitle("Simulator's Almanac")
        self.setGeometry(100, 100, 1280, 720)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        container_widget.setLayout(self.layout)

        self.build_path_browser()
        self.setCentralWidget(container_widget)
        self.restore_settings()
        self.show()

    def restore_settings(self):
        if last_path := self.settings.value(SETTINGS_KEY_SAVE_PATH, ""):
            self.file_line.setText(last_path)
        else:
            self.file_line.setText(str(Path.home()))

    def closeEvent(self, event: QCloseEvent) -> None:
        """Override of the base class event. Runs this function on (safe) close of the program"""
        self.save_settings()
        event.accept()

    def save_settings(self):
        self.settings.setValue(SETTINGS_KEY_SAVE_PATH, self.file_line.text())

    def build_path_browser(self):
        self.file_line.setPlaceholderText("/Path/To/Save")  # default. Should be overridden after first run

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_clicked)
        self.load_button = QPushButton("Load")
        self.load_button.setEnabled(False)
        self.load_button.clicked.connect(self.build_readers)

        self.layout.addWidget(QLabel("Save Path:"), 0, 0)
        self.layout.addWidget(self.file_line, 0, 1)
        self.layout.addWidget(browse_button, 0, 2)
        self.layout.addWidget(self.load_button, 0, 3)
        self.file_line.textChanged.connect(self.validate_path_and_enable_button)

    def browse_clicked(self):
        if directory := QFileDialog.getExistingDirectory(self, "Select your save path"):
            self.path = Path(directory)
            self.file_line.setText(directory)

    def build_readers(self):
        readers: dict[str, BaseReader] = {"fields": Fields(self.path)}
        return readers

    def validate_path_and_enable_button(self, path: str) -> None:
        path_valid: bool = False
        if not path.strip():
            pass
        else:
            path = Path(path)
            if path.exists():
                path_valid = True
                self.path = path
        self.load_button.setEnabled(path_valid)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    sys.exit(app.exec())

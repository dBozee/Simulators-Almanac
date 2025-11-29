from pathlib import Path

from PyQt6.QtCore import QSettings, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

from readers import AllReaders

SETTINGS_KEY_SAVE_PATH = "LastSavePath"


class PathBrowser(QWidget):
    """
    Widget for loading and/or selecting the path to the save
    """

    load_request = pyqtSignal(AllReaders)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QSettings()
        self._path: Path = Path.home()
        self.layout = QGridLayout()
        self.file_line = QLineEdit()
        self.farm_id_line = QLineEdit()
        self.load_button: QPushButton | None = None
        self.data: AllReaders | None = None

        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self._build_ui()

    def _restore_settings(self):
        if last_path := self.settings.value(SETTINGS_KEY_SAVE_PATH, ""):
            self.file_line.setText(last_path)

    def startup_load(self):
        if last_path := self.settings.value(SETTINGS_KEY_SAVE_PATH, ""):
            self.file_line.setText(last_path)
            self._execute_startup_load(last_path)

    def _execute_startup_load(self, last_path: str) -> None:
        if not last_path.strip():
            return
        path = Path(last_path)

        if path.exists():
            self._path = path
            self.load_button.setEnabled(True)
            self.save_settings()
            self._update_readers()

    def save_settings(self):
        self.settings.setValue(SETTINGS_KEY_SAVE_PATH, self.file_line.text())

    def _build_ui(self):
        self.file_line.setPlaceholderText("/Path/To/Save")  # default. Should be overridden after first run
        self.farm_id_line.setText("1")
        self.farm_id_line.setFixedWidth(35)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self._browse_clicked)

        self.load_button = QPushButton("Load")
        self.load_button.setEnabled(False)
        self.load_button.clicked.connect(self._update_readers)

        self.layout.addWidget(QLabel("Save Path:"), 0, 0)
        self.layout.addWidget(self.file_line, 0, 1)
        self.layout.addWidget(QLabel("Farm ID:"), 0, 2)
        self.layout.addWidget(self.farm_id_line, 0, 3)
        self.layout.addWidget(browse_button, 0, 4)
        self.layout.addWidget(self.load_button, 0, 5)

        splitter = QFrame()
        splitter.setFrameShape(QFrame.Shape.HLine)
        splitter.setFrameShadow(QFrame.Shadow.Sunken)

        splitter_layout = QHBoxLayout()
        splitter_layout.addWidget(splitter)
        splitter_layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addLayout(splitter_layout, 1, 0, 1, self.layout.columnCount())

        self.file_line.textChanged.connect(self._validate_path_and_enable_button)

    def _browse_clicked(self):

        if directory := QFileDialog.getExistingDirectory(self, "Select your save path", str(self._path)):
            self._path = Path(directory)
            self.file_line.setText(directory)

    def _update_readers(self):
        self.data = AllReaders(self.path)
        self.load_request.emit(self.data)

    def _validate_path_and_enable_button(self, path: str) -> None:
        path_valid: bool = False
        if not path.strip():
            pass
        else:
            path = Path(path)
            if path.exists():
                path_valid = True
                self._path = path
        self.load_button.setEnabled(path_valid)
        self.save_settings()

    @property
    def path(self) -> Path:
        return self._path

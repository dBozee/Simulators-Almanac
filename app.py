import sys
from typing import Final

from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from readers.all_readers import AllReaders
from widgets import NavbarButton, PathBrowser
from widgets.pages import BasePage, HomePage

PAGE_MAP: Final[dict[str, type[BasePage]]] = {
    "Home": HomePage,
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        QApplication.setOrganizationName("dBozee")
        QApplication.setApplicationName("SimulatorsAlmanac")

        self.readers: AllReaders | None = None
        self.page_widgets: dict[str, BasePage] = {}

        self.setWindowTitle("Simulator's Almanac")
        self.setGeometry(100, 100, 1280, 720)

        # main window
        container_widget = QWidget()
        main_v_layout = QVBoxLayout(container_widget)
        main_v_layout.setContentsMargins(0, 0, 0, 0)
        main_v_layout.setSpacing(0)

        # Path browser top bar
        self.path_browser = PathBrowser(container_widget)
        self.path_browser.load_request.connect(self._handle_data_load)
        main_v_layout.addWidget(self.path_browser)

        # navbar + stacked pages
        bottom_h_layout = QHBoxLayout()
        bottom_h_layout.setContentsMargins(0, 0, 10, 0)
        self._build_navbar(bottom_h_layout)

        splitter = QFrame()
        splitter.setFrameShape(QFrame.Shape.VLine)
        splitter.setFrameShadow(QFrame.Shadow.Sunken)
        bottom_h_layout.addWidget(splitter)

        content_v_layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()
        self._build_pages()
        self._show_page("Home")
        content_v_layout.addWidget(self.stacked_widget)
        content_v_layout.addStretch()
        bottom_h_layout.addLayout(content_v_layout, 1)

        main_v_layout.addLayout(bottom_h_layout, 1)

        self.setCentralWidget(container_widget)
        self.show()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Override of the base class event. Runs this function on (safe) close of the program"""
        if self.path_browser:
            self.path_browser.save_settings()
        event.accept()

    def _build_navbar(self, main_layout: QHBoxLayout):
        nav_v_layout = QVBoxLayout()
        nav_v_layout.setSpacing(10)
        nav_v_layout.setContentsMargins(5, 0, 5, 5)

        for page_name in PAGE_MAP:
            button = NavbarButton(page_name, self._show_page)
            nav_v_layout.addWidget(button)

        main_layout.addLayout(nav_v_layout)

    def _show_page(self, page_name: str):
        page_widget = self.page_widgets.get(page_name)
        if page_widget:
            index = self.stacked_widget.indexOf(page_widget)
            self.stacked_widget.setCurrentIndex(index)

    def _build_pages(self):
        PageClass: type[BasePage]
        for name, PageClass in PAGE_MAP.items():
            page_instance = PageClass(self.stacked_widget, self.readers)
            self.stacked_widget.addWidget(page_instance)
            self.page_widgets[name] = page_instance

    def _handle_data_load(self, readers_data: AllReaders):
        self.readers = readers_data

        for page in self.page_widgets.values():
            page.update_content(self.readers)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

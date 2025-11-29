from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget

from widgets.finance_graph import FinanceGraphWidget
from widgets.pages import BasePage
from widgets.pages.kvp_widget import KVPWidget

UNKNOWN = "Unknown"


class HomePage(BasePage):
    def __init__(self, container_widget, readers):
        super().__init__(container_widget, readers)
        self.main_layout = QVBoxLayout()
        self.farm_info_grid: QGridLayout | None = None
        self.farm_name_label: KVPWidget | None = None
        self.money_amount_label: KVPWidget | None = None
        self.loan_amount_label: KVPWidget | None = None
        self.finances_graph: FinanceGraphWidget | None = None
        self.farm_info_container = QWidget()

        self.awaiting = QLabel("Awaiting Save Data...")

        if self.data:
            self._setup_farm_info()
            self._setup_graphs()
        else:
            self.main_layout.addWidget(self.awaiting)

        self.main_layout.addStretch()
        self.setLayout(self.main_layout)

        if self.data:
            self._update_ui()

    def _update_ui(self):
        if self.data and self.awaiting:
            self.main_layout.removeWidget(self.awaiting)
            self.awaiting.deleteLater()
            self.awaiting = None
            self._setup_farm_info()
            self._setup_graphs()

        if self.data:
            self._update_farm_info()
            self._update_graphs()

    def _setup_farm_info(self):
        if self.farm_info_grid:
            return  # return early because we've already built these widgets

        self.farm_info_grid = QGridLayout(self.farm_info_container)

        self.farm_name_label = KVPWidget(
            "Name:", self.data.my_farm.name if self.data else UNKNOWN, self.farm_info_container
        )
        self.money_amount_label = KVPWidget(
            "Money:", str(self.data.my_farm.money) if self.data else UNKNOWN, self.farm_info_container
        )
        self.loan_amount_label = KVPWidget(
            "Loan:", str(self.data.my_farm.loan) if self.data else UNKNOWN, self.farm_info_container
        )

        self.farm_info_grid.addWidget(self.farm_name_label, 0, 0)
        self.farm_info_grid.addWidget(self.money_amount_label, 1, 0)
        self.farm_info_grid.addWidget(self.loan_amount_label, 2, 0)

        self.main_layout.addWidget(self.farm_info_container, alignment=Qt.AlignmentFlag.AlignLeft)
        self._set_info_grid_style()

    def _update_farm_info(self):
        if not self.data or not self.farm_name_label or not self.money_amount_label:
            return
        farm_name = self.data.my_farm.name if self.data else UNKNOWN
        money_amount = f"${self.data.my_farm.money}" if self.data else UNKNOWN
        loan_amount = f"${self.data.my_farm.loan}" if self.data else UNKNOWN

        self.farm_name_label.update_value(farm_name)
        self.money_amount_label.update_value(money_amount)
        self.loan_amount_label.update_value(loan_amount)

    def _set_info_grid_style(self):
        self.farm_info_grid.setSpacing(0)
        self.farm_info_grid.setContentsMargins(0, 0, 2, 2)
        self.farm_info_grid.setColumnStretch(0, 0)
        self.farm_info_grid.setColumnStretch(1, 0)
        self.farm_info_grid.setRowStretch(0, 0)
        self.farm_info_grid.setRowStretch(1, 0)

    def _setup_graphs(self):
        if self.finances_graph:
            return

        self.finances_graph = FinanceGraphWidget(self.data)
        self.finances_graph.setMinimumHeight(200)
        self.main_layout.addWidget(self.finances_graph)

    def _update_graphs(self):
        if not self.data or not self.data.my_farm or not self.data.my_farm.statistics:
            return

        self.finances_graph.update_plot()

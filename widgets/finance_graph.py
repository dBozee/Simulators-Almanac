import numpy as np
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from pyqtgraph import PlotWidget, mkPen

from readers import AllReaders


class FinanceGraphWidget(QWidget):
    def __init__(self, data: AllReaders | None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.data: AllReaders | None = data
        self.layout = QVBoxLayout()
        self.plot_widget: PlotWidget = PlotWidget()
        self.layout.addWidget(self.plot_widget)

        self.days = np.array([])
        self.sales = np.array([])
        self.purchases = np.array([])
        self.data_ready = False

        if self.data:
            self._process_data()
            self._setup_plot()
        else:
            self.layout.addWidget(QLabel("No data to plot"))

        self.setLayout(self.layout)

    def _process_data(self) -> None:
        if not self.data or not self.data.my_farm.finances.stats:
            self.data_ready = False
            return

        farm_finances = self.data.my_farm.finances.stats

        day_numbers = []
        daily_sales = []
        daily_purchases = []

        for stats in farm_finances:
            day_numbers.append(stats.day)
            daily_sales.append(stats.total_earned)
            daily_purchases.append(abs(stats.total_spent))

        self.days = np.array(day_numbers)
        self.sales = np.array(daily_sales)
        self.purchases = np.array(daily_purchases)
        self.data_ready = True

    def _setup_plot(self) -> None:
        if not self.data_ready:
            return

        self.plot_widget.setBackground('black')
        self.plot_widget.setWindowTitle('Daily Farm Finances: Earned v. Spent')

        self.plot_widget.setLabel('left', 'Amount ($)', color="#006600", size="12pt")
        self.plot_widget.setLabel('bottom', 'Game Day', color="#333333", size="12pt")

        self.plot_widget.addLegend()
        self.plot_widget.showGrid(x=True, y=True, alpha=0.5)

        sales_pen = mkPen(color=(0, 175, 0), width=3)
        self.plot_widget.plot(
            x=self.days,
            y=self.sales,
            pen=sales_pen,
            name="Daily Sales (Income)",
            symbol='o',
            symbolSize=8,
        )

        purchases_pen = mkPen(color=(175, 0, 0), width=3)
        self.plot_widget.plot(
            x=self.days,
            y=self.purchases,
            pen=purchases_pen,
            name="Daily Purchases (Expenses)",
            symbol='o',
            symbolSize=8,
        )

        if self.days.size > 0:
            self.plot_widget.setXRange(self.days.min(), self.days.max() + 1)
            y_max = max(self.sales.max(), self.purchases.max()) * 1.1
            self.plot_widget.setYRange(0, y_max)

    def update_plot(self) -> None:
        self._process_data()
        if not self.data_ready:
            return
        self.plot_widget.clear()
        self._setup_plot()

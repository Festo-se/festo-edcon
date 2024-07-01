"""Model for the analyse tab."""

# pylint: disable=import-error, no-name-in-module
from pyqtgraph import (
    PlotWidget,
    mkPen,
)
from pyqtgraph.exporters import ImageExporter
from PyQt5.QtWidgets import QFileDialog


class AnalyseModel(PlotWidget):
    """Defines the analyse model."""

    def __init__(self):
        super().__init__()
        self.parameter_values = []
        self.time = []
        self.curve_parameter = None
        self.parameter_pnu = None
        self.time_value = 0
        self.com = None
        self.setup_styles()

    def setup_styles(self):
        self.setBackground("#f0f0f0")
        self.setLabel(
            "left",
            "Parameter Value",
        )
        self.setLabel(
            "bottom",
            "Time",
        )
        self.getAxis("left").setPen(
            mkPen(
                color="#1f77b4",
                width=2,
            )
        )
        self.getAxis("bottom").setPen(
            mkPen(
                color="#1f77b4",
                width=2,
            )
        )
        self.showGrid(x=True, y=True, alpha=0.2)

    def clear_plot_widget(self):
        """Clears the plot widget and resets its parameters."""
        self.clear()
        self.parameter_values.clear()
        self.time.clear()
        self.time_value = 0

    def plot_parameter(self, com, pnu):
        """
        Plots the parameter values on the plot widget.

        Parameters:
        com : The communication driver
        pnu(int): The parameter number to be plotted.
        """
        self.clear_plot_widget()
        self.com = com
        self.parameter_pnu = pnu
        self.curve_parameter = self.plot(
            self.time,
            self.parameter_values,
            pen=mkPen(color="#1f77b4", width=2),
        )

    def save_plot_as_image(self):
        """Opens a file dialog to save the current plot as an image file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Position Plot",
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)",
        )
        if file_path:
            exporter = ImageExporter(self.plotItem)
            exporter.export(file_path)

    def update_plot(self):
        """Updates the plot with new parameter values."""
        if self.com is not None:
            try:
                new_parameter_value = self.com.read_pnu(self.parameter_pnu, 0)
            except ValueError as e:
                print(e)
                return

            self.time_value += 0.1
            self.parameter_values.append(new_parameter_value)
            self.time.append(self.time_value)
            self.curve_parameter.setData(self.time, self.parameter_values)

            # Dynamically adjust y-axis range with a margin
            min_y = min(self.parameter_values)
            max_y = max(self.parameter_values)
            y_range = max_y - min_y
            margin = y_range * 0.1  # 10% margin
            if margin == 0:  # Avoid zero margin when all values are the same
                margin = max_y * 0.1  # 10% of the value
            self.setYRange(min_y - margin, max_y + margin)

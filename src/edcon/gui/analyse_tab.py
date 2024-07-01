"""Setup code of the analyse tab."""

from pathlib import PurePath
from importlib.resources import files

# pylint: disable=import-error, no-name-in-module
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from edcon.gui.analyse_plot_model import AnalyseModel


class AnalyseTab(QWidget):
    """Defines the analyse tab."""

    def __init__(self, get_com_func):
        super().__init__()
        loadUi(PurePath(files("edcon") / "gui" / "ui" / "analyse_tab.ui"), self)
        self.get_com_func = get_com_func
        self.plot_widget = AnalyseModel()
        self.horizontalLayout.addWidget(self.plot_widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.plot_widget.update_plot)
        self.timer.start(100)

        self.plot_button.clicked.connect(self.plot_parameter_with_pnu)
        self.save_plot_button.clicked.connect(self.plot_widget.save_plot_as_image)
        self.stop_plotting_button.clicked.connect(self.stop_plotting)

    def plot_parameter_with_pnu(self):
        """plots a parameter based on the PNU (parameter number unit) input."""
        self.timer.start(100)
        com = self.get_com_func()
        self.plot_widget.plot_parameter(com, int(self.plot_parameter_lineEdit.text()))

    def stop_plotting(self):
        """Stops the plotting process and clears the plot widget."""
        self.plot_widget.clear_plot_widget()
        self.timer.stop()

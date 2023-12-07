"""CLI tool starts the gui"""
from PyQt5.QtWidgets import QApplication
from edcon.gui.mainwindow import MainWindow

def add_gui_parser(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_gui = subparsers.add_parser('gui')
    parser_gui.set_defaults(func=gui_func)


def gui_func(args):
    """Executes subcommand based on provided arguments"""
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

"""CLI tool starts the gui"""
from edcon.utils.logging import Logging
def add_gui_parser(subparsers):
    """Adds arguments to a provided subparsers instance"""
    parser_gui = subparsers.add_parser('gui')
    parser_gui.set_defaults(func=gui_func)


def gui_func(args):
    """Executes subcommand based on provided arguments"""
    try:
        from PyQt5.QtWidgets import QApplication
        from edcon.gui.mainwindow import MainWindow
    except ImportError:
        Logging.logger.error("GUI dependency PyQt5 could not be imported.\n"
                             "Possible remedies:\n"
                             "1. Install festo-edcon with GUI support: 'pip install festo-edcon[gui]'\n"
                             "2. Install PyQt5 manually: 'pip install pyqt5'\n")
        return

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

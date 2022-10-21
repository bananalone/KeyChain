from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QSplitter

from ui.GroupFrame import GroupFrame
from ui.AccountFrame import AccountFrame
from ui.MenuBar import MenuBar
from ui.interface import Paintable
from ui.state import ui_state


class MainWindow(QMainWindow, Paintable):
    def __init__(self) -> None:
        super().__init__()
        self._current_window_stays_on_top = ui_state.windowStaysOnTop
        self._menu_bar = MenuBar(self)
        self._group_frame = GroupFrame(self)
        self._account_frame = AccountFrame(self)
        self.setMenuBar(self._menu_bar)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._group_frame)
        splitter.addWidget(self._account_frame)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        self.setCentralWidget(splitter)
        self.resize(QSize(480, 360))
        self.paint()

    def paint(self):
        if self._current_window_stays_on_top != ui_state.windowStaysOnTop:
            self._current_window_stays_on_top = ui_state.windowStaysOnTop
            if self._current_window_stays_on_top:
                self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
            else:
                self.setWindowFlags(Qt.WindowType.Window)
            self.show()
        if ui_state.saved:
            self.setWindowTitle(f'{ui_state.current_file} - KeyChain')
        else:
            self.setWindowTitle(f'*{ui_state.current_file} - KeyChain')
        self._menu_bar.paint()
        self._group_frame.paint()
        self._account_frame.paint()
    
    def repaint(self):
        self.paint()

    def closeEvent(self) -> None:
        self._menu_bar.quit_app()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self._menu_bar.quit_app()

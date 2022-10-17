from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QSplitter

from ui.GroupFrame import GroupFrame
from ui.AccountFrame import AccountFrame
from ui.MenuBar import MenuBar
from ui.interface import Paintable


class MainWindow(QMainWindow, Paintable):
    def __init__(self) -> None:
        super().__init__()
        self._menu_bar = MenuBar(self)
        self._group_frame = GroupFrame(self)
        self._group_frame.setMinimumWidth(100)
        self._group_frame.setMaximumWidth(300)
        self._account_frame = AccountFrame(self)
        self._account_frame.setMinimumWidth(360)
        self.setMenuBar(self._menu_bar)
        self.paint()

    def paint(self):
        self.setWindowTitle('KeyChain')
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._group_frame)
        splitter.addWidget(self._account_frame)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)
        self._menu_bar.paint()
        self._group_frame.paint()
        self._account_frame.paint()
    
    def repaint(self):
        self.paint()

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QSplitter

from ui.GroupFrame import GroupFrame
from ui.AccountFrame import AccountFrame
from ui.MenuBar import MenuBar
from ui.interface import Paintable


class MainWindow(QMainWindow, Paintable):
    def __init__(self) -> None:
        super().__init__()
        self.paint()
        
    def paint(self):
        self.setWindowTitle('KeyChain')
        menu_bar = MenuBar(self)
        group_frame = GroupFrame(self)
        group_frame.setMinimumWidth(100)
        group_frame.setMaximumWidth(300)
        account_frame = AccountFrame(self)
        account_frame.setMinimumWidth(360)
        self.setMenuBar(menu_bar)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(group_frame)
        splitter.addWidget(account_frame)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)
        menu_bar.paint()
        group_frame.paint()
        account_frame.paint()
    
    def repaint(self):
        self.paint()

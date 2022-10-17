import sys

from PyQt5.QtWidgets import QMenuBar, QFileDialog, qApp

from ui.interface import Paintable
from data import Manager


class MenuBar(QMenuBar, Paintable):
    def __init__(self, parent: Paintable) -> None:
        super().__init__()
        self._parent = parent
        
    def paint(self):
        self.file_menu = self.addMenu('File')
        self.edit_menu = self.addMenu('Edit')
        self.settings_menu = self.addMenu('Settings')
        self.help_menu = self.addMenu('Help')

    def repaint(self):
        self._parent.repaint()
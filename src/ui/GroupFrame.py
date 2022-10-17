from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QLineEdit, QListWidget

from ui.interface import Paintable


class GroupFrame(QFrame, Paintable):
    def __init__(self, parent: Paintable) -> None:
        super().__init__()
        self._parent = parent
        self.label_group = QLabel()
        self.line_edit_group_filter = QLineEdit()
        self.list_widget_group = QListWidget()

    def paint(self):
        vbox = QVBoxLayout()
        self.label_group.setText('Groups')
        self.label_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(self.label_group)
        self.line_edit_group_filter.setPlaceholderText('Filter group')
        vbox.addWidget(self.line_edit_group_filter)
        vbox.addWidget(self.list_widget_group)
        self.setLayout(vbox)
        self.setFrameStyle(QFrame.Shape.Box)
    
    def repaint(self):
        self._parent.repaint()
    
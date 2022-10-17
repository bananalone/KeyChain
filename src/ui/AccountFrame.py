from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTableWidget

from ui.interface import Paintable


class AccountFrame(QFrame, Paintable):
    def __init__(self, parent: Paintable) -> None:
        super().__init__()
        self._parent = parent
        self.label_account = QLabel()
        self.line_edit_account_filter = QLineEdit()
        self.table_widget_account = QTableWidget()
        
    def paint(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.label_account.setText('Accounts')
        hbox.addWidget(self.label_account)
        self.line_edit_account_filter.setPlaceholderText('Filter account')
        hbox.addWidget(self.line_edit_account_filter)
        vbox.addLayout(hbox)
        vbox.addWidget(self.table_widget_account)
        self.setLayout(vbox)
        self.setFrameStyle(QFrame.Shape.Box)
    
    def repaint(self):
        self._parent.repaint()


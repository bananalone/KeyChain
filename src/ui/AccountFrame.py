from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView)

from data import Manager
from handlers import AccountsFilter
from ui.state import state
from ui.interface import Paintable


class AccountFrame(QFrame, Paintable):
    def __init__(self, parent: Paintable) -> None:
        super().__init__()
        self._parent = parent
        self._manager = Manager()
        self._label_group = QLabel()
        self._line_edit_account_filter = QLineEdit()
        self._table_widget_account = QTableWidget()
        self._table_widget_account.setColumnCount(3)
        self._table_widget_account.setHorizontalHeaderLabels(['Username', 'Password', 'Remark'])
        self._table_widget_account.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table_widget_account.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table_widget_account.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self._label_group.setText('No group selected')
        hbox.addWidget(self._label_group)
        self._line_edit_account_filter.setPlaceholderText('Filter account')
        hbox.addWidget(self._line_edit_account_filter)
        vbox.addLayout(hbox)
        vbox.addWidget(self._table_widget_account)
        self.setLayout(vbox)
        self.setFrameStyle(QFrame.Shape.Box)

    def paint(self):
        self._table_widget_account.clear()
        if not state.current_selected_group:
            self._label_group.setText('No group selected')
            return
        self._label_group.setText(state.current_selected_group.name)
        self._table_widget_account.setRowCount(len(state.current_accounts))
        for i, account in enumerate(state.current_accounts):
            self._table_widget_account.setItem(i, 0, QTableWidgetItem(account.username))
            self._table_widget_account.setItem(i, 1, QTableWidgetItem(account.password))
            remark = account.remark if account.remark else ''
            self._table_widget_account.setItem(i, 2, QTableWidgetItem(remark))

    def repaint(self):
        self._parent.repaint()


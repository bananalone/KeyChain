from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import (QApplication, QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
                             QHeaderView, QAbstractItemView, QInputDialog, QMenu)

from data import Account, Manager
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
        self._table_widget_account.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table_widget_account.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table_widget_account.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self._table_widget_account.itemClicked.connect(self._table_widget_clicked)
        self._table_widget_account.itemDoubleClicked.connect(self._table_widget_double_clicked)
        self._table_widget_account.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._table_widget_account.customContextMenuRequested.connect(self._create_table_widget_context_menu)
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
        self._table_widget_account.setHorizontalHeaderLabels(['Username', 'Password', 'Remark'])
        if not state.current_selected_group:
            self._label_group.setText('No group selected')
            self._table_widget_account.setRowCount(0)
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

    def _table_widget_clicked(self, item: QTableWidgetItem):
        clipboard = QApplication.clipboard()
        clipboard.setText(item.text())

    def _table_widget_double_clicked(self, item: QTableWidgetItem):
        column = item.column()
        if column == 0:
            return
        account = state.current_accounts[item.row()]
        state.current_selected_account = account
        if column == 1:
            self._set_account_password()
        else:
            self._set_account_remark()
        self.repaint()
                
    def _set_account_password(self):
        account = state.current_selected_account
        text, ok = QInputDialog.getText(self, account.username, 'Input new password:')
        if ok:
            account.set_password(text)
        self.repaint()
        
    def _set_account_remark(self):
        account = state.current_selected_account
        text, ok = QInputDialog.getText(self, account.username, 'Input new remark:')
        if ok:
            account.set_remark(text)
        self.repaint()
 
    def _create_table_widget_context_menu(self, pos: QPoint):
        item = self._table_widget_account.itemAt(pos)
        menu = QMenu()
        if item:
            account = state.current_accounts[item.row()]
            state.current_selected_account = account
            add_account = menu.addAction('Add account')
            add_account.triggered.connect(self._add_account)
            menu.addSeparator()
            edit_password = menu.addAction('Edit password')
            edit_password.triggered.connect(self._set_account_password)
            rand_passwd = menu.addAction('Random password')
            rand_passwd.triggered.connect(self._random_password)
            edit_remark = menu.addAction('Edit remark')
            edit_remark.triggered.connect(self._set_account_remark)
            menu.addSeparator()
            remove_account = menu.addAction(f'Remove {account.username}')
            remove_account.triggered.connect(self._remove_account)
        else:
            add_account = menu.addAction('Add account')
            add_account.triggered.connect(self._add_account)
        h = self._table_widget_account.horizontalHeader().height()
        w = self._table_widget_account.verticalHeader().width()
        menu.exec(self._table_widget_account.mapToGlobal(QPoint(pos.x()+w, pos.y()+h)))

    def _add_account(self):
        text, ok = QInputDialog.getText(self, 'Add account', 'Input username:')
        if ok:
            if text in state.current_selected_group.username_list:
                QMessageBox.about(self, 'Add account error', f'{text} already in {state.current_selected_group.name}')
                return
            account = Account(text)
            state.current_selected_group.add_account(account)
            state.current_accounts = AccountsFilter().set_group(state.current_selected_group).accounts()
        self.repaint()
        
    def _random_password(self):
        state.current_selected_account.random_password()
        self.repaint()
        
    def _remove_account(self):
        state.current_selected_group.remove_account(state.current_selected_account.username)
        state.current_accounts = AccountsFilter().set_group(state.current_selected_group).accounts()
        state.current_selected_account = None
        self.repaint()



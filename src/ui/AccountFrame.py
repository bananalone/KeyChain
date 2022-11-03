from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint, QModelIndex
from PyQt5.QtWidgets import (QApplication, QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox,
                             QHeaderView, QAbstractItemView, QInputDialog, QMenu, QToolTip)

from data import Account, Manager
from handlers import AccountsFilter
from memory import StateRecorder
from ui.state import AppState, ui_state
from ui.interface import Paintable
from utils import find_substr


class AccountFrame(QFrame, Paintable):
    def __init__(self, parent: Paintable) -> None:
        super().__init__()
        self._current_group = ui_state.current_selected_group
        self._parent = parent
        self._manager = Manager()
        self._recorder = StateRecorder()
        self._label_group = QLabel()
        self._clip_bak = QApplication.clipboard().text()
        self._line_edit_account_filter = QLineEdit()
        self._line_edit_account_filter.textChanged.connect(self._filter_accounts)
        self._table_widget_account = QTableWidget()
        self._table_widget_account.setColumnCount(3)
        self._table_widget_account.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table_widget_account.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table_widget_account.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)
        self._table_widget_account.itemClicked.connect(self._table_widget_clicked)
        self._table_widget_account.itemDoubleClicked.connect(self._table_widget_double_clicked)
        self._table_widget_account.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._table_widget_account.customContextMenuRequested.connect(self._create_table_widget_context_menu)
        self._table_widget_account.setMouseTracking(True)
        self._table_widget_account.entered.connect(self._show_account_info_tip)
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
        if not ui_state.current_selected_group:
            self._label_group.setText('No group selected')
            self._table_widget_account.setRowCount(0)
            return
        self._label_group.setText(ui_state.current_selected_group.name)
        self._table_widget_account.setRowCount(len(ui_state.current_accounts))
        for i, account in enumerate(ui_state.current_accounts):
            self._table_widget_account.setItem(i, 0, QTableWidgetItem(account.username))
            self._table_widget_account.setItem(i, 1, QTableWidgetItem(account.password))
            if not account.remark:
                account.set_remark(account.username)
            self._table_widget_account.setItem(i, 2, QTableWidgetItem(account.remark))
        if self._current_group != ui_state.current_selected_group:
            self._line_edit_account_filter.setText('')
            self._current_group = ui_state.current_selected_group

    def repaint(self):
        self._parent.repaint()

    def _filter_accounts(self, text: str):
        if not ui_state.current_selected_group:
            return
        accounts = AccountsFilter().set_group(ui_state.current_selected_group) \
                                   .filter(lambda a: find_substr(a.remark, text)).accounts()
        accounts.sort(key = lambda a: len(a.remark))
        ui_state.current_accounts = accounts
        self.repaint()
        self._line_edit_account_filter.setFocus()

    def _table_widget_clicked(self, item: QTableWidgetItem):
        clipboard = QApplication.clipboard()
        self._clip_bak = clipboard.text()
        clipboard.setText(item.text())

    def _table_widget_double_clicked(self, item: QTableWidgetItem):
        clipboard = QApplication.clipboard()
        clipboard.setText(self._clip_bak)
        column = item.column()
        if column == 0:
            return
        account = ui_state.current_accounts[item.row()]
        ui_state.current_selected_account = account
        if column == 1:
            self._set_account_password()
        else:
            self._set_account_remark()
                
    def _set_account_password(self):
        account = ui_state.current_selected_account
        text, ok = QInputDialog.getText(self, account.username, 'Input new password:')
        if ok:
            self._recorder.record(AppState())
            account.set_password(text)
            ui_state.saved = False
            self.repaint()
        
    def _set_account_remark(self):
        account = ui_state.current_selected_account
        text, ok = QInputDialog.getText(self, account.username, 'Input new remark:')
        if ok:
            self._recorder.record(AppState())
            account.set_remark(text)
            ui_state.saved = False
            self.repaint()
 
    def _create_table_widget_context_menu(self, pos: QPoint):
        item = self._table_widget_account.itemAt(pos)
        menu = QMenu()
        if item:
            self._table_widget_account.selectRow(item.row())
            account = ui_state.current_accounts[item.row()]
            ui_state.current_selected_account = account
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
        elif ui_state.current_selected_group:
            add_account = menu.addAction('Add account')
            add_account.triggered.connect(self._add_account)
        h = self._table_widget_account.horizontalHeader().height()
        w = self._table_widget_account.verticalHeader().width()
        menu.exec(self._table_widget_account.mapToGlobal(QPoint(pos.x()+w, pos.y()+h)))

    def _show_account_info_tip(self, model_index: QModelIndex):
        QToolTip.showText(QtGui.QCursor.pos(), model_index.data())

    def _add_account(self):
        text, ok = QInputDialog.getText(self, 'Add account', 'Input username:')
        if ok:
            if len(text) > 0 and text in ui_state.current_selected_group.username_list:
                QMessageBox.about(self, 'Add account error', f'{text} already in {ui_state.current_selected_group.name}')
                return
            account = Account(text)
            self._recorder.record(AppState())
            ui_state.current_selected_group.add_account(account)
            ui_state.current_accounts = AccountsFilter().set_group(ui_state.current_selected_group).accounts()
            ui_state.saved = False
            self.repaint()
        
    def _random_password(self):
        self._recorder.record(AppState())
        ui_state.current_selected_account.random_password()
        ui_state.saved = False
        self.repaint()
        
    def _remove_account(self):
        self._recorder.record(AppState())
        ui_state.current_selected_group.remove_account(ui_state.current_selected_account.username)
        ui_state.current_accounts = AccountsFilter().set_group(ui_state.current_selected_group).accounts()
        ui_state.current_selected_account = None
        ui_state.saved = False
        self.repaint()



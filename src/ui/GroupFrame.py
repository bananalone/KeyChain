from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, QLineEdit, QListWidget, QMenu,
                             QMessageBox, QInputDialog)
from memory import StateRecorder

from ui.state import AppState, ui_state
from ui.interface import Paintable
from data import Group, Manager
from handlers import AccountsFilter, GroupCleaner, GroupExpander, GroupsFilter, ManagerExpander, ManagerCleaner
from utils import find_substr


class GroupFrame(QFrame, Paintable):
    def __init__(self, parent: Paintable) -> None:
        super().__init__()
        self._parent = parent
        self._manager = Manager()
        self._recorder = StateRecorder()
        self._label_group = QLabel()
        self._line_edit_group_filter = QLineEdit()
        self._line_edit_group_filter.textChanged.connect(self._filter_groups)
        self._list_widget_group = QListWidget()
        self._list_widget_group.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._list_widget_group.customContextMenuRequested.connect(self._create_list_widget_context_menu)
        ui_state.current_groups = GroupsFilter().set_manager().groups()
        vbox = QVBoxLayout()
        self._label_group.setText('Groups')
        self._label_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(self._label_group)
        self._line_edit_group_filter.setPlaceholderText('Filter group')
        vbox.addWidget(self._line_edit_group_filter)
        vbox.addWidget(self._list_widget_group)
        self.setLayout(vbox)
        self.setFrameStyle(QFrame.Shape.Box)
        self._list_widget_group.itemClicked.connect(self._list_widget_item_clicked)

    def paint(self):
        self._list_groups()
    
    def repaint(self):
        self._parent.repaint()

    def _filter_groups(self, text: str):
        groups = GroupsFilter().set_manager().filter(lambda g: find_substr(g.name, text)).groups()
        groups.sort(key = lambda g: len(g.name))
        ui_state.current_groups = groups
        self.repaint()
        self._line_edit_group_filter.setFocus()

    def _list_groups(self):
        self._list_widget_group.clear()
        for group in ui_state.current_groups:
            self._list_widget_group.addItem(group.name)
        
    def _list_widget_item_clicked(self, item):
        group_name = item.text()
        ui_state.current_selected_group = self._manager.get_group(group_name)
        ui_state.current_accounts = AccountsFilter().set_group(ui_state.current_selected_group).accounts()
        self.repaint()

    def _create_list_widget_context_menu(self, pos: QPoint):
        item = self._list_widget_group.itemAt(pos)
        menu = QMenu()
        if item:
            group = self._manager.get_group(item.text())
            add_group = menu.addAction('Add group')
            add_group.triggered.connect(self._add_group)
            menu.addSeparator()
            rename_group = menu.addAction(f'Rename {group.name}')
            rename_group.triggered.connect(self._rename_group)
            menu.addSeparator()
            remove_group = menu.addAction(f'Remove {group.name}')
            remove_group.triggered.connect(self._remove_group)
            ui_state.current_selected_group = group
        else:
            add_group = menu.addAction('Add group')
            add_group.triggered.connect(self._add_group)
        menu.exec(self._list_widget_group.mapToGlobal(pos))

    def _add_group(self):
        text, ok = QInputDialog.getText(self, 'Add group', 'Input group name:')
        if ok:
            if len(text) > 0 and text in GroupsFilter().set_manager().group_name_list():
                QMessageBox.about(self, 'Add group error', f'{text} already exists')
                return
            group = Group(text)
            self._recorder.record(AppState())
            self._manager.add_group(group)
            ui_state.current_selected_account = None
            ui_state.current_accounts = []
            ui_state.current_selected_group = group
            ui_state.current_groups = GroupsFilter().set_manager().groups()
            ui_state.saved = False
            self.repaint()

    def _rename_group(self):
        text, ok = QInputDialog.getText(self, 'Rename group', 'Input new group name:')
        if ok:
            if text in GroupsFilter().set_manager().group_name_list():
                QMessageBox.about(self, 'Rename group error', f'{text} already exists')
                return
            group = Group(text)
            GroupExpander(group).expand_accounts_in_group(ui_state.current_selected_group)
            self._recorder.record(AppState())
            self._manager.remove_group(ui_state.current_selected_group.name)
            self._manager.add_group(group)
            ui_state.current_selected_group = group
            ui_state.current_groups = GroupsFilter().set_manager().groups()
            ui_state.saved = False
            self.repaint()

    def _remove_group(self):
        self._recorder.record(AppState())
        self._manager.remove_group(ui_state.current_selected_group.name)
        ui_state.current_selected_group = None
        ui_state.current_selected_account = None
        ui_state.current_accounts = []
        ui_state.current_groups = GroupsFilter().set_manager().groups()
        ui_state.saved = False
        self.repaint()

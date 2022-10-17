from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QLineEdit, QListWidget

from ui.state import state
from ui.interface import Paintable
from data import Group, Manager
from handlers import AccountsFilter, GroupsFilter, ManagerExpander, ManagerCleaner


class GroupFrame(QFrame, Paintable):
    def __init__(self, parent: Paintable) -> None:
        super().__init__()
        self._parent = parent
        self._manager = Manager()
        self._label_group = QLabel()
        self._line_edit_group_filter = QLineEdit()
        self._list_widget_group = QListWidget()
        state.current_groups = GroupsFilter().set_manager().groups()
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

    def _list_groups(self):
        self._list_widget_group.clear()
        for group in state.current_groups:
            self._list_widget_group.addItem(group.name)
        
    def _list_widget_item_clicked(self, item):
        group_name = item.text()
        state.current_selected_group = self._manager.get_group(group_name)
        state.current_accounts = AccountsFilter().set_group(state.current_selected_group).accounts()
        self.repaint()
